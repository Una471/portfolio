"""Case-study dashboard and tenant-aware student support SaaS API."""
from datetime import date
from io import BytesIO
from pathlib import Path
import json
import sqlite3
import uuid

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "student_saas.db"
app = Flask(__name__, static_folder=str(ROOT), static_url_path="")

# This dataset belongs only to the portfolio case-study dashboard.
case_study_df = pd.read_csv(ROOT / "student_data_scored.csv")
model = joblib.load(ROOT / "model.pkl")
encoders = {k: joblib.load(ROOT / filename) for k, filename in {
    "campus": "le_campus.pkl", "program": "le_program.pkl",
    "source": "le_source.pkl", "parent": "le_parent.pkl", "gender": "le_gender.pkl",
}.items()}
FEATURES = json.loads((ROOT / "features.json").read_text())


def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with db() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS schools (
          id TEXT PRIMARY KEY, name TEXT NOT NULL, campuses TEXT NOT NULL,
          programs TEXT NOT NULL, sources TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
          school_id TEXT NOT NULL, student_id TEXT NOT NULL, data TEXT NOT NULL,
          PRIMARY KEY (school_id, student_id)
        );
        CREATE TABLE IF NOT EXISTS registrations (
          id INTEGER PRIMARY KEY AUTOINCREMENT, school_id TEXT NOT NULL,
          reg_id TEXT NOT NULL, data TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS interventions (
          id INTEGER PRIMARY KEY AUTOINCREMENT, school_id TEXT NOT NULL, data TEXT NOT NULL
        );
        """)


init_db()


@app.after_request
def allow_local_frontends(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-School-ID"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
    return response


def school_id():
    return request.headers.get("X-School-ID") or request.args.get("school_id")


def school_or_error():
    sid = school_id()
    if not sid:
        return None, (jsonify({"error": "School setup is required."}), 401)
    with db() as con:
        school = con.execute("SELECT * FROM schools WHERE id=?", (sid,)).fetchone()
    if not school:
        return None, (jsonify({"error": "School account was not found."}), 404)
    return school, None


def unpack(row):
    return json.loads(row["data"])


def normalise_student(raw):
    item = {str(k).strip(): v for k, v in raw.items()}
    aliases = {"id": "student_id", "student id": "student_id", "student_name": "name",
               "attendance": "attendance_rate_pct", "grade": "grade_average_pct"}
    for old, new in aliases.items():
        if old in item and new not in item: item[new] = item[old]
    item["student_id"] = str(item.get("student_id") or f"STU-{uuid.uuid4().hex[:8].upper()}")
    for key in ("age", "year_enrolled", "courses_failed", "warnings_issued", "at_risk"):
        try: item[key] = int(float(item.get(key, 0) or 0))
        except (ValueError, TypeError): item[key] = 0
    for key in ("attendance_rate_pct", "grade_average_pct", "distance_from_campus_km", "dropout_probability"):
        try: item[key] = float(item.get(key, 0) or 0)
        except (ValueError, TypeError): item[key] = 0.0
    item.setdefault("status", "Active")
    item.setdefault("program", "Not assigned")
    item.setdefault("campus", "Not assigned")
    item.setdefault("gender", "Not recorded")
    item.setdefault("semester_enrolled", "Not recorded")
    item.setdefault("enrollment_source", "Not recorded")
    if not item.get("risk_level"):
        if item["attendance_rate_pct"] < 60 or item["grade_average_pct"] < 40: item["risk_level"] = "Critical"
        elif item["at_risk"]: item["risk_level"] = "High Risk"
        elif item["warnings_issued"] or item["courses_failed"]: item["risk_level"] = "Medium Risk"
        else: item["risk_level"] = "Low Risk"
    return item


@app.get("/")
def home(): return send_from_directory(ROOT, "software.html")


@app.get("/<path:name>")
def assets(name): return send_from_directory(ROOT, name)


@app.get("/api/dashboard")
def dashboard_data():
    clean = case_study_df.replace({np.nan: None})
    return jsonify({"students": clean.to_dict(orient="records")})


@app.post("/api/schools")
def create_school():
    p = request.get_json(force=True)
    name = str(p.get("name", "")).strip()
    if not name: return jsonify({"error": "School name is required."}), 400
    sid = uuid.uuid4().hex
    values = lambda key, default: [str(x).strip() for x in p.get(key, default) if str(x).strip()]
    campuses = values("campuses", ["Main Campus"])
    programs = values("programs", ["General Programme"])
    sources = values("sources", ["Website", "Walk-In", "Referral"])
    with db() as con:
        con.execute("INSERT INTO schools VALUES (?,?,?,?,?,?)", (sid, name, json.dumps(campuses), json.dumps(programs), json.dumps(sources), str(date.today())))
    return jsonify({"id": sid, "name": name}), 201


@app.get("/api/bootstrap")
def bootstrap():
    if not school_id() and "dashboard.html" in (request.referrer or ""):
        clean = case_study_df.replace({np.nan: None})
        return jsonify({"students": clean.to_dict(orient="records")})
    school, error = school_or_error()
    if error: return error
    sid = school["id"]
    with db() as con:
        rows = con.execute("SELECT data FROM students WHERE school_id=? ORDER BY student_id", (sid,)).fetchall()
    return jsonify({
        "school": {"id": sid, "name": school["name"]},
        "students": [unpack(row) for row in rows],
        "options": {"campus": json.loads(school["campuses"]), "program": json.loads(school["programs"]),
                    "source": json.loads(school["sources"]), "parent": ["None", "Primary", "Secondary", "Tertiary"],
                    "gender": ["Female", "Male"]},
    })


@app.post("/api/import")
def import_students():
    school, error = school_or_error()
    if error: return error
    upload = request.files.get("file")
    if not upload or not upload.filename.lower().endswith(".csv"):
        return jsonify({"error": "Choose a CSV file."}), 400
    try: incoming = pd.read_csv(BytesIO(upload.read())).replace({np.nan: None})
    except Exception as exc: return jsonify({"error": f"CSV could not be read: {exc}"}), 400
    if "student_id" not in incoming.columns and "Student ID" not in incoming.columns:
        return jsonify({"error": "CSV requires a student_id column."}), 400
    items = [normalise_student(row) for row in incoming.to_dict(orient="records")]
    with db() as con:
        for item in items:
            con.execute("INSERT OR REPLACE INTO students VALUES (?,?,?)", (school["id"], item["student_id"], json.dumps(item)))
    return jsonify({"imported": len(items)})


@app.post("/api/predict")
def predict():
    school, error = school_or_error()
    if error: return error
    p = request.get_json(force=True)
    program_length = 1 if "Certificate" in p["program"] else 2
    try: encoded = [encoders[k].transform([p[k]])[0] for k in ("campus", "program", "source", "parent", "gender")]
    except (ValueError, KeyError, TypeError): encoded = [0, 0, 0, 0, 0]
    distance, age = float(p["distance"]), int(p["age"])
    row = np.array([[age, distance, int(p["transport"]), int(p["financial_aid"]), int(p["working"]),
                     80.0, 55.0, 0, 0, program_length, int(p["year"]), *encoded,
                     0, 0, 0, int(distance > 40), int(age > 30), int(p["parent"] in ("None", "Primary"))]])
    probability = float(model.predict_proba(row)[0][1] * 100)
    level = "LOW RISK" if probability < 30 else "MEDIUM RISK" if probability < 55 else "HIGH RISK"
    flags = []
    if distance > 40: flags.append(f"Lives {distance:.0f}km from campus — commute may require planning")
    if not p["transport"]: flags.append("No personal transport recorded")
    if p["working"]: flags.append("Works part-time")
    if p["parent"] in ("None", "Primary"): flags.append("Limited education support recorded at home")
    if not p["financial_aid"]: flags.append("No financial-aid application recorded")
    if age > 30: flags.append("Mature student")
    return jsonify({"probability": probability, "level": level, "flags": flags,
                    "note": "Baseline estimate; review against the school’s own policy."})


@app.route("/api/registrations", methods=["GET", "POST"])
def registration_api():
    school, error = school_or_error()
    if error: return error
    sid = school["id"]
    with db() as con:
        if request.method == "POST":
            item = request.get_json(force=True)
            number = con.execute("SELECT COUNT(*) FROM registrations WHERE school_id=?", (sid,)).fetchone()[0] + 1
            item.update(reg_id=f"REG-{number:04d}", date=str(date.today()), status="Pending Approval")
            con.execute("INSERT INTO registrations(school_id,reg_id,data) VALUES (?,?,?)", (sid, item["reg_id"], json.dumps(item)))
            return jsonify(item), 201
        rows = con.execute("SELECT id,data FROM registrations WHERE school_id=? ORDER BY id DESC", (sid,)).fetchall()
    return jsonify([{**unpack(row), "_id": row["id"]} for row in rows])


@app.patch("/api/registrations/<int:item_id>")
def registration_status(item_id):
    school, error = school_or_error()
    if error: return error
    with db() as con:
        row = con.execute("SELECT data FROM registrations WHERE id=? AND school_id=?", (item_id, school["id"])).fetchone()
        if not row: return jsonify({"error": "Registration not found."}), 404
        item = unpack(row); item["status"] = request.get_json(force=True)["status"]
        con.execute("UPDATE registrations SET data=? WHERE id=? AND school_id=?", (json.dumps(item), item_id, school["id"]))
        if item["status"] == "Approved":
            student = normalise_student({
                "student_id": item.get("omang") or item.get("reg_id"), "name": item.get("student_name"),
                "age": item.get("age"), "gender": item.get("gender"), "campus": item.get("campus"),
                "program": item.get("program"), "year_enrolled": item.get("year"),
                "semester_enrolled": item.get("semester"), "enrollment_source": item.get("source"),
                "status": "Active", "risk_level": item.get("risk_level"),
                "dropout_probability": str(item.get("risk_score", "0")).replace("%", ""),
                "at_risk": int(item.get("risk_level") in ("MEDIUM RISK", "HIGH RISK")),
            })
            con.execute("INSERT OR REPLACE INTO students VALUES (?,?,?)", (school["id"], student["student_id"], json.dumps(student)))
    return jsonify(item)


@app.route("/api/interventions", methods=["GET", "POST"])
def intervention_api():
    school, error = school_or_error()
    if error: return error
    sid = school["id"]
    with db() as con:
        if request.method == "POST":
            item = request.get_json(force=True); item["date"] = str(date.today())
            con.execute("INSERT INTO interventions(school_id,data) VALUES (?,?)", (sid, json.dumps(item)))
            return jsonify(item), 201
        rows = con.execute("SELECT data FROM interventions WHERE school_id=? ORDER BY id DESC", (sid,)).fetchall()
    return jsonify([unpack(row) for row in rows])


if __name__ == "__main__": app.run(debug=True, port=8000)
