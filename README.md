# Portfolio Monorepo

This repository contains the portfolio site, seven static HTML projects, and five Streamlit projects.

## Structure

- `site/`: main portfolio website
- `projects/`: static HTML dashboard and software projects
- `streamlit/`: Python Streamlit projects

Every static project uses `dashboard.html` and `software.html` as its entry points.

Every Streamlit project deploys from one `app.py` entry point. The launcher switches between the existing `03_dashboard.py` and `04_software.py` views.

## Deployment model

Deploy `site/` together with `projects/` to a static host. The production output should expose the project folders at `/projects/`.

Deploy each industry from `streamlit/<industry>/app.py`. This produces five Streamlit deployments, with Software and Dashboard sharing the same URL and switching through the `view` query parameter.

## Static projects

- Construction
- Education
- Government
- Law
- Logistics
- Real Estate
- Technology

## Streamlit projects

- Loan
- Health
- Mining
- Retail
- Tourism

## Important

The original source folders outside this repository remain unchanged. This folder is the clean deployment copy.