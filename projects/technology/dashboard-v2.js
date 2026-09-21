const $ = (s) => document.querySelector(s);

const ICONS = {
  people:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="9" cy="8" r="3"/><path d="M3.5 18c.5-3.4 2.4-5 5.5-5s5 1.6 5.5 5"/><circle cx="17" cy="9" r="2.3"/><path d="M15.5 13.8c2.9-.4 4.6 1 5 4.2"/></svg>',
  calendar:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>',
  bars:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 20V11M12 20V5M19 20v-7"/></svg>',
  checkdoc:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 3h9l4 4v14H6z"/><path d="M15 3v5h5M9 14l2 2 4-5"/></svg>',
  smile:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M8.5 10h.01M15.5 10h.01M8.5 14.5c1.7 2 5.3 2 7 0"/></svg>',
  cap:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M2.5 9 12 4l9.5 5L12 14z"/><path d="M6 11.5V16c3.3 2.4 8.7 2.4 12 0v-4.5M21.5 9v6"/></svg>',
  female:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="5"/><path d="M12 13v8M8.5 18h7"/></svg>',
  male:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="10" cy="14" r="5"/><path d="m14 10 6-6M15 4h5v5"/></svg>',
  truck:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/></svg>',
  clock:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/></svg>',
  stopwatch:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="13" r="8"/><path d="M9 2h6M12 5V2M18 7l2-2M12 9v5"/></svg>',
  fuel:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 3h9v18H5zM7 6h5v4H7zM14 8h3l2 2v7c0 2 3 2 3 0v-6l-2-2"/></svg>',
  utilization:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 20v-4M9 20v-8M14 20V9M19 20V4"/></svg>',
  alert:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m12 3 9 17H3z"/><path d="M12 9v5M12 17h.01"/></svg>',
  check:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="m8 12 2.5 2.5L16 9"/></svg>',
  coins:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v4c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 10v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4M5 14v4c0 1.7 3.1 3 7 3s7-1.3 7-3v-4"/></svg>',
  trenddown:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m4 7 6 6 4-4 6 6M20 10v5h-5"/></svg>',
  trendup:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m4 17 6-6 4 4 6-6M15 9h5v5"/></svg>',
  sparkle:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3l1.4 4.6L18 9l-4.6 1.4L12 15l-1.4-4.6L6 9l4.6-1.4zM19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/></svg>',
  headset:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><path d="M4 14h3v6H4zM17 14h3v4c0 2-2 3-5 3"/></svg>',
  heart:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20.8 5.8c-2-2-5.1-1.8-6.8.4L12 8.8l-2-2.6C8.3 4 5.2 3.8 3.2 5.8 1.1 7.9 1.4 11 3.4 13l8.6 8 8.6-8c2-2 2.3-5.1.2-7.2Z"/></svg>',
  trophy:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M8 4h8v4c0 3-1.8 5-4 5s-4-2-4-5zM10 13v4M14 13v4M8 20h8M10 17h4"/><path d="M8 6H4v2c0 2 1.5 3 4 3M16 6h4v2c0 2-1.5 3-4 3"/></svg>',
  building:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 21V7l8-4 8 4v14M2 21h20M8 10h2M14 10h2M8 14h2M14 14h2M10 21v-4h4v4"/></svg>',
  leaf:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M20 4C12 4 5 8 5 15c0 3 2 5 5 5 7 0 10-8 10-16Z"/><path d="M5 20c2-5 5-8 10-11"/></svg>',
  cloud:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 18h11a4 4 0 0 0 .4-8 7 7 0 0 0-13.1-2.3A5 5 0 0 0 7 18Z"/></svg>',
  download:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3v12M8 11l4 4 4-4M4 19h16"/></svg>'
};

function icon(name){ return ICONS[name] || ICONS.bars; }

function setTheme(t){ const r=document.documentElement.style; r.setProperty('--primary',t.primary);r.setProperty('--primary2',t.primary2);r.setProperty('--accent',t.accent);r.setProperty('--danger',t.danger||'#e75a4d');r.setProperty('--warning',t.warning||'#e8ad35'); }
function deepMerge(target, source){ for(const k in source){ if(source[k] && typeof source[k]==='object' && !Array.isArray(source[k])){ target[k]=deepMerge(target[k]||{},source[k]); } else target[k]=source[k]; } return target; }

function commonOptions(){ return {responsive:true,maintainAspectRatio:false,animation:false,plugins:{legend:{labels:{usePointStyle:true,pointStyle:'circle',boxWidth:7,boxHeight:7,padding:11,color:'#566680',font:{family:'Segoe UI',size:9,weight:'500'}}},tooltip:{backgroundColor:'#102342',padding:9,titleFont:{family:'Segoe UI',size:10,weight:'600'},bodyFont:{family:'Segoe UI',size:9},cornerRadius:7}},scales:{x:{grid:{display:false},ticks:{color:'#6d7c93',font:{family:'Segoe UI',size:8}},border:{color:'#dfe7f1'}},y:{grid:{color:'#edf2f7'},ticks:{color:'#6d7c93',font:{family:'Segoe UI',size:8}},border:{display:false}}}}; }
const centerTextPlugin={id:'centerText',afterDraw(chart,args,opts){if(!opts||!opts.text)return;const {ctx,chartArea:{left,right,top,bottom}}=chart;ctx.save();ctx.textAlign='center';ctx.fillStyle='#142846';ctx.font='700 15px Segoe UI';ctx.fillText(opts.text,(left+right)/2,(top+bottom)/2-3);if(opts.sub){ctx.fillStyle='#66768e';ctx.font='500 9px Segoe UI';ctx.fillText(opts.sub,(left+right)/2,(top+bottom)/2+12);}ctx.restore();}};
const chartsAvailable = typeof Chart !== 'undefined';
if(chartsAvailable){ if(typeof ChartDataLabels !== 'undefined') Chart.register(ChartDataLabels); Chart.register(centerTextPlugin); Chart.defaults.font.family='Segoe UI'; Chart.defaults.color='#51627d'; }

async function boot(){
 const data=await fetch('dashboard_data.json',{cache:'no-store'}).then(r=>r.json());
 setTheme(data.theme);document.title=data.pageTitle;
 $('#eyebrow').textContent=data.hero.eyebrow;$('#title').textContent=data.hero.title;$('#subtitle').textContent=data.hero.subtitle;$('#heroImage').style.backgroundImage=`url('${data.hero.image}')`;$('#motto').innerHTML=data.hero.motto;
 $('#tabs').innerHTML=data.hero.tabs.map((t,i)=>`<button class="${i===0?'active':''}">${t}</button>`).join('');
  $('#filters').innerHTML=data.filters.map((f,index)=>`<div class="filter"><label for="filter-${index}">${f.label}</label><select id="filter-${index}" data-column="${f.column}">${f.options.map(option=>`<option value="${option}">${option}</option>`).join('')}</select></div>`).join('');
 $('#promo').style.backgroundImage=`url('${data.promo.image}')`;$('#promoTitle').innerHTML=data.promo.title;$('#promoSub').textContent=data.promo.sub;
 $('#kpis').innerHTML=data.kpis.map(k=>`<article class="kpi"><div class="kpi-meta"><div class="kpi-icon">${icon(k.icon)}</div><div class="kpi-label">${k.label}</div></div><div class="kpi-value">${k.value}</div><div class="kpi-delta"><strong>${k.delta||''}</strong>${k.note?` ${k.note}`:''}</div></article>`).join('');
 data.insights.forEach(()=>{}); $('#insights').innerHTML=data.insights.map(i=>`<article class="insight"><div class="insight-icon" style="background:${i.bg};color:${i.color}">${icon(i.icon)}</div><div><div class="insight-label">${i.label}</div><div class="insight-title">${i.title}</div><div class="insight-meta">${i.meta}</div></div>${i.badge?`<span class="badge" style="background:${i.badgeBg};color:${i.badgeColor}">${i.badge}</span>`:'<span style="color:#91a0b6">›</span>'}</article>`).join('');
 $('#chartATitle').textContent=data.charts.a.title;$('#chartBTitle').textContent=data.charts.b.title;$('#chartCTitle').textContent=data.charts.c.title;$('#chartDTitle').textContent=data.charts.d.title;$('#chartETitle').textContent=data.charts.e.title;
 const chartInstances={}; if(chartsAvailable){ const make=(id,c,key)=>chartInstances[key]=new Chart($(id),{type:c.type,data:JSON.parse(JSON.stringify(c.data)),options:deepMerge(commonOptions(),c.options||{})});make('#chartA',data.charts.a,'a');make('#chartB',data.charts.b,'b');make('#chartC',data.charts.c,'c');make('#chartD',data.charts.d,'d');make('#chartE',data.charts.e,'e'); }
 $('#tableTitle').textContent=data.table.title;$('#exportIcon').innerHTML=icon('download');
 $('#tableHeader').innerHTML=data.table.columns.map(c=>`<th>${c}</th>`).join('');  let visibleRows=[...data.table.rows];
  const originalKpis=data.kpis.map(k=>({...k}));
  const originalCharts=Object.fromEntries(Object.entries(chartInstances).map(([key,chart])=>[key,{labels:[...(chart.data.labels||[])],datasets:chart.data.datasets.map(dataset=>[...(dataset.data||[])])}]));
  const cellText=cell=>cell&&typeof cell==='object'?cell.label:String(cell??'');
  const numberFrom=value=>Number(String(cellText(value)).replace(/[^0-9.-]/g,''))||0;
  const weighted=(rows,valueIndex,weightIndex=1)=>{const total=rows.reduce((sum,row)=>sum+numberFrom(row[weightIndex]),0);return total?rows.reduce((sum,row)=>sum+numberFrom(row[valueIndex])*numberFrom(row[weightIndex]),0)/total:0;};
  const formatNumber=value=>Math.round(value).toLocaleString('en-US');
  const setKpi=(index,value)=>{const el=document.querySelectorAll('#kpis .kpi-value')[index];if(el)el.textContent=value;};
  const updateKpis=rows=>{
    document.querySelectorAll('#kpis .kpi-value').forEach((el,index)=>el.textContent=originalKpis[index]?.value||'');
    const usable=rows.filter(row=>cellText(row[0]).toLowerCase()!=='total');
    if(!usable.length)return;
    if(/RouteIQ/i.test(data.pageTitle)){
      const deliveries=usable.reduce((sum,row)=>sum+numberFrom(row[1]),0);
      setKpi(0,formatNumber(deliveries));setKpi(1,weighted(usable,3).toFixed(1)+'%');setKpi(2,weighted(usable,2).toFixed(1)+' hrs');setKpi(3,'P'+formatNumber(weighted(usable,4)));setKpi(4,weighted(usable,6).toFixed(0)+'%');setKpi(5,formatNumber(usable.reduce((sum,row)=>sum+numberFrom(row[1])*numberFrom(row[5])/100,0)));
    }else if(/Student|Education/i.test(data.pageTitle)){
      setKpi(0,formatNumber(usable.reduce((sum,row)=>sum+numberFrom(row[1]),0)));setKpi(1,weighted(usable,4).toFixed(1)+'%');setKpi(2,weighted(usable,2).toFixed(2));setKpi(3,weighted(usable,3).toFixed(1)+'%');setKpi(4,weighted(usable,5).toFixed(1)+' / 5');
    }else{
      const accounts=usable.reduce((sum,row)=>sum+numberFrom(row[1]),0);
      const revenue=usable.reduce((sum,row)=>sum+numberFrom(row[1])*numberFrom(row[2]),0)/1000;
      setKpi(0,formatNumber(accounts));setKpi(1,'P'+formatNumber(revenue)+'K');setKpi(2,weighted(usable,3).toFixed(1)+'%');setKpi(4,weighted(usable,4).toFixed(0));setKpi(5,weighted(usable,6).toFixed(1));setKpi(7,weighted(usable,5).toFixed(0));
    }
  };
  const updateCharts=rows=>{
    const allowed=new Set(rows.map(row=>cellText(row[0])).filter(label=>label.toLowerCase()!=='total'));
    Object.entries(chartInstances).forEach(([key,chart])=>{
      const original=originalCharts[key];if(!original)return;
      const matching=original.labels.map((label,index)=>allowed.has(String(label))?index:-1).filter(index=>index>=0);
      if(matching.length){chart.data.labels=matching.map(index=>original.labels[index]);chart.data.datasets.forEach((dataset,datasetIndex)=>dataset.data=matching.map(index=>original.datasets[datasetIndex][index]));}
      else{chart.data.labels=[...original.labels];chart.data.datasets.forEach((dataset,datasetIndex)=>dataset.data=[...original.datasets[datasetIndex]]);}
      chart.update();
    });
  };
  const renderTable=rows=>{
    visibleRows=rows;
    $('#tableBody').innerHTML=rows.map(row=>`<tr>${row.map(cell=>{if(cell&&typeof cell==='object'){if(cell.type==='status')return `<td><span class="status-dot" style="background:${cell.color}"></span>${cell.label}</td>`;if(cell.type==='pill')return `<td><span class="risk-pill" style="background:${cell.bg};color:${cell.color}">${cell.label}</span></td>`;}return `<td>${cell}</td>`;}).join('')}</tr>`).join('');
    const count=$('#filterCount');if(count)count.textContent=`${rows.length} of ${data.table.rows.length} rows shown`;
  };
  const applyFilters=()=>{
    const selections=[...document.querySelectorAll('#filters select')];
    const rows=data.table.rows.filter(row=>selections.every(select=>select.selectedIndex===0||cellText(row[Number(select.dataset.column)])===select.value));
    renderTable(rows);updateKpis(rows);updateCharts(rows);
  };
  document.querySelectorAll('#filters select').forEach(select=>select.addEventListener('change',applyFilters));
  $('#resetFilters')?.addEventListener('click',()=>{document.querySelectorAll('#filters select').forEach(select=>select.selectedIndex=0);applyFilters();});
  renderTable(data.table.rows);updateKpis(data.table.rows);
  const tabButtons=[...document.querySelectorAll('#tabs button')];
 tabButtons.forEach((button,index)=>button.addEventListener('click',()=>{
   tabButtons.forEach(item=>item.classList.toggle('active',item===button));
   const target=index===0?document.querySelector('#kpis'):document.querySelector(index===1?'#insights':'.table-card');
   target?.scrollIntoView({behavior:'smooth',block:'start'});
 }));
 document.querySelectorAll('[data-expand]').forEach(button=>button.addEventListener('click',()=>{
   const card=button.closest('.chart-card');
   const expanded=card.classList.toggle('expanded');
   button.innerHTML=expanded?'Close details <span>&uarr;</span>':'View details <span>&rarr;</span>';
   setTimeout(()=>Object.values(chartInstances).forEach(chart=>chart.resize()),40);
 }));
 const rangeSelect=$('#rangeSelect');
 if(rangeSelect && chartInstances.d){
   const fullLabels=[...chartInstances.d.data.labels];
   const fullData=chartInstances.d.data.datasets.map(dataset=>[...dataset.data]);
   rangeSelect.addEventListener('change',()=>{
     const start=rangeSelect.value==='recent'?Math.max(0,fullLabels.length-6):0;
     chartInstances.d.data.labels=fullLabels.slice(start);
     chartInstances.d.data.datasets.forEach((dataset,index)=>dataset.data=fullData[index].slice(start));
     chartInstances.d.update();
   });
 }
 $('#exportBtn')?.addEventListener('click',()=>{
   const escape=value=>'"'+String(value??'').replaceAll('"','""')+'"';
   const rows=[data.table.columns,...visibleRows.map(row=>row.map(cell=>cell&&typeof cell==='object'?cell.label:cell))];
   const blob=new Blob(['\ufeff'+rows.map(row=>row.map(escape).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'});
   const link=document.createElement('a');
   link.href=URL.createObjectURL(blob);
   link.download=data.table.title.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'.csv';
   link.click();
   URL.revokeObjectURL(link.href);
 });
}
boot().catch(e=>{document.body.innerHTML=`<pre style="padding:30px;font:14px monospace">${e.stack||e}</pre>`});
