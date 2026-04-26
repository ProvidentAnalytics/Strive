"""
build_clean.py
Generates strive_ctm_clean.html — the complete, clean dashboard.
Run after process_data.py has produced the data files.
"""
import json, os

def load(fname):
    with open(fname) as f:
        return f.read()

def build():
    # Load all data
    SD    = load('data_split.json')
    DAILY = load('data_daily_full.json')
    RECS  = load('data_recordings.json')
    LOG   = load('data_log.json')
    FORMS = load('data_forms.json')
    MKT   = load('data_marketing.json')

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Strive Recovery — CTM Analytics</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* ── VARIABLES ── */
:root {{
  --navy:#0a3d5c; --teal:#3dffc0; --teal-dim:rgba(61,255,192,0.12);
  --bg:#f4f6f9; --white:#fff; --border:#e1e7ef;
  --text:#0f1923; --muted:#6b7e96;
  --red:#ef4444; --amber:#f59e0b; --blue:#3b82f6; --green:#10b981; --purple:#8b5cf6;
  --shadow:0 1px 3px rgba(10,61,92,.07),0 4px 14px rgba(10,61,92,.04);
  --shadow-h:0 4px 12px rgba(10,61,92,.11),0 8px 28px rgba(10,61,92,.07);
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;min-height:100vh}}

/* ── TOPBAR ── */
.topbar{{background:var(--navy);height:58px;padding:0 28px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:200;box-shadow:0 2px 16px rgba(10,61,92,.25)}}
.tb-left{{display:flex;align-items:center;gap:16px}}
.tb-logo{{background:var(--teal);color:var(--navy);font-family:'Space Mono',monospace;font-size:11px;font-weight:700;letter-spacing:.08em;padding:5px 10px;border-radius:4px}}
.tb-title{{color:#fff;font-size:15px;font-weight:600}}
.tb-sub{{color:rgba(255,255,255,.4);font-size:11px;font-family:'Space Mono',monospace}}
.tb-right{{display:flex;align-items:center;gap:12px}}
.live-pill{{display:flex;align-items:center;gap:6px;background:rgba(61,255,192,.1);border:1px solid rgba(61,255,192,.25);border-radius:20px;padding:5px 12px;font-family:'Space Mono',monospace;font-size:10px;color:var(--teal)}}
.live-dot{{width:6px;height:6px;border-radius:50%;background:var(--teal);box-shadow:0 0 7px var(--teal);animation:blink 2s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}
.sync-lbl{{font-family:'Space Mono',monospace;font-size:10px;color:rgba(255,255,255,.35)}}
.btn-refresh{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.13);border-radius:6px;padding:6px 14px;color:#fff;font-family:'DM Sans',sans-serif;font-size:12px;font-weight:500;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all .2s}}
.btn-refresh:hover{{background:rgba(255,255,255,.13)}}
.spin{{display:inline-block}}.spin.go{{animation:rot 1s linear infinite}}
@keyframes rot{{to{{transform:rotate(360deg)}}}}

/* ── TAB NAV ── */
.tab-nav{{background:var(--white);border-bottom:1px solid var(--border);padding:0 28px;display:flex;gap:0;overflow-x:auto;position:sticky;top:58px;z-index:190;box-shadow:0 2px 8px rgba(10,61,92,.05)}}
.tab-nav::-webkit-scrollbar{{height:3px}}.tab-nav::-webkit-scrollbar-thumb{{background:var(--border)}}
.tnav{{padding:14px 18px;border:none;border-bottom:3px solid transparent;background:none;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;white-space:nowrap;transition:all .2s;margin-bottom:-1px}}
.tnav:hover{{color:var(--navy)}}
.tnav.active{{color:var(--navy);border-bottom-color:var(--teal);font-weight:700}}
.tab-badge{{display:inline-flex;align-items:center;justify-content:center;background:var(--teal-dim);color:var(--navy);font-family:'Space Mono',monospace;font-size:9px;font-weight:700;padding:1px 6px;border-radius:10px;margin-left:6px}}

/* ── LAYOUT ── */
.wrap{{max-width:1380px;margin:0 auto;padding:24px 24px 60px}}
.tab-panel{{display:none}}.tab-panel.active{{display:block}}
.g1{{display:grid;grid-template-columns:1fr;gap:16px;margin-bottom:16px}}
.g2{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.g3{{display:grid;grid-template-columns:2fr 1fr;gap:16px;margin-bottom:16px}}
.g3r{{display:grid;grid-template-columns:1fr 2fr;gap:16px;margin-bottom:16px}}
@media(max-width:900px){{.g2,.g3,.g3r{{grid-template-columns:1fr}}}}

/* ── CONTROL BAR ── */
.ctrl-bar{{display:flex;align-items:center;gap:10px;margin-bottom:20px;flex-wrap:wrap}}
.ctrl-group{{display:flex;gap:3px;background:var(--white);border:1px solid var(--border);border-radius:8px;padding:3px}}
.ctrl-btn{{padding:5px 13px;border-radius:5px;border:none;background:none;font-family:'Space Mono',monospace;font-size:10px;font-weight:700;color:var(--muted);cursor:pointer;transition:all .15s;letter-spacing:.04em;white-space:nowrap}}
.ctrl-btn.active{{background:var(--navy);color:#fff}}
.ctrl-btn:hover:not(.active){{background:rgba(10,61,92,.07);color:var(--navy)}}
.ctrl-sep{{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);padding:0 4px;display:flex;align-items:center}}

/* ── KPI ── */
.kpi-row{{display:grid;gap:12px;margin-bottom:20px}}
.kpi{{background:var(--white);border:1px solid var(--border);border-radius:12px;padding:16px 18px;box-shadow:var(--shadow);position:relative;overflow:hidden;transition:box-shadow .2s}}
.kpi:hover{{box-shadow:var(--shadow-h)}}
.kpi::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:12px 12px 0 0}}
.kpi.navy::before{{background:var(--navy)}}.kpi.teal::before{{background:var(--teal)}}
.kpi.red::before{{background:var(--red)}}.kpi.amber::before{{background:var(--amber)}}
.kpi.blue::before{{background:var(--blue)}}.kpi.green::before{{background:var(--green)}}
.kpi.purple::before{{background:var(--purple)}}
.kpi-lbl{{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:7px}}
.kpi-val{{font-size:28px;font-weight:700;color:var(--navy);line-height:1;letter-spacing:-.03em;margin-bottom:4px}}
.kpi-sub{{font-size:11px;color:var(--muted)}}

/* ── CARD ── */
.card{{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:20px 22px;box-shadow:var(--shadow);transition:box-shadow .2s}}
.card:hover{{box-shadow:var(--shadow-h)}}
.card-h{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:16px;gap:8px}}
.card-title{{font-size:13px;font-weight:700;color:var(--navy)}}
.card-sub{{font-size:11px;color:var(--muted);margin-top:2px}}
.chip{{font-family:'Space Mono',monospace;font-size:9px;padding:3px 8px;border-radius:4px;background:var(--teal-dim);color:var(--navy);font-weight:700;letter-spacing:.05em;white-space:nowrap}}

/* ── SCROLLABLE CHART ── */
.scroll-chart{{overflow-x:auto;overflow-y:hidden;width:100%;cursor:grab}}
.scroll-chart:active{{cursor:grabbing}}
.scroll-chart::-webkit-scrollbar{{height:4px}}
.scroll-chart::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}

/* ── HEATMAP ── */
.hm-outer{{overflow-x:auto}}
.hm-grid{{display:grid;gap:3px;min-width:520px}}
.hm-hrow{{display:grid;grid-template-columns:72px repeat(7,1fr);gap:3px;margin-bottom:3px}}
.hm-dlbl{{font-size:9px;color:var(--muted);text-align:center;letter-spacing:.04em;text-transform:uppercase;font-family:'Space Mono',monospace}}
.hm-row{{display:grid;grid-template-columns:72px repeat(7,1fr);gap:3px}}
.hm-hlbl{{font-size:9px;color:var(--muted);display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-family:'Space Mono',monospace}}
.hm-cell{{border-radius:4px;height:22px;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:700;cursor:default;transition:transform .1s;font-family:'Space Mono',monospace}}
.hm-cell:hover{{transform:scale(1.18);z-index:2;position:relative}}

/* ── AGENT TABLE ── */
.agt{{width:100%;border-collapse:collapse}}
.agt th{{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);padding:0 10px 9px 0;text-align:left;border-bottom:1px solid var(--border);white-space:nowrap}}
.agt td{{padding:9px 10px 9px 0;font-size:13px;border-bottom:1px solid rgba(225,231,239,.5);vertical-align:middle}}
.agt tr:last-child td{{border-bottom:none}}
.agt tr:hover td{{background:rgba(244,246,249,.7)}}
.av{{width:26px;height:26px;border-radius:50%;background:var(--navy);color:var(--teal);font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-family:'Space Mono',monospace}}
.aname{{display:flex;align-items:center;gap:8px;font-weight:600;color:var(--navy)}}
.bar-track{{flex:1;height:6px;background:var(--bg);border-radius:3px;overflow:hidden;min-width:50px}}
.bar-fill{{height:100%;border-radius:3px;background:var(--navy)}}
.bar-row{{display:flex;align-items:center;gap:7px}}
.rbadge{{font-size:11px;font-weight:700;padding:2px 7px;border-radius:8px;white-space:nowrap}}
.rhi{{background:rgba(16,185,129,.1);color:var(--green)}}
.rmd{{background:rgba(245,158,11,.1);color:var(--amber)}}
.rlo{{background:rgba(239,68,68,.1);color:var(--red)}}

/* ── SOURCE LEGEND ── */
.src-leg{{display:flex;flex-direction:column;gap:9px}}
.src-row{{display:flex;align-items:center;gap:9px}}
.src-dot{{width:10px;height:10px;border-radius:2px;flex-shrink:0}}
.src-name{{flex:1;font-size:12px;font-weight:500}}
.src-pct{{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);min-width:32px;text-align:right}}
.src-cnt{{font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:var(--navy);min-width:38px;text-align:right}}

/* ── DOW BARS ── */
.dow-row{{display:flex;align-items:center;gap:8px;margin-bottom:5px}}
.dow-lbl{{font-family:'Space Mono',monospace;font-size:9px;color:var(--muted);width:28px;text-align:right}}
.dow-track{{flex:1;height:8px;background:var(--bg);border-radius:4px;overflow:hidden}}
.dow-fill{{height:100%;border-radius:4px;transition:width .4s ease}}
.dow-val{{font-family:'Space Mono',monospace;font-size:9px;font-weight:700;color:var(--navy);min-width:28px}}

/* ── MISSED LIST ── */
.missed-list{{display:flex;flex-direction:column;gap:5px;max-height:360px;overflow-y:auto}}
.missed-list::-webkit-scrollbar{{width:4px}}.missed-list::-webkit-scrollbar-thumb{{background:var(--border);border-radius:2px}}
.mitem{{display:flex;align-items:center;gap:10px;padding:9px 12px;background:var(--bg);border-radius:8px;border-left:3px solid var(--red)}}
.mtime{{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);white-space:nowrap;min-width:110px}}
.mcaller{{font-size:12px;font-weight:600;color:var(--navy);flex:1}}
.msrc{{font-size:10px;color:var(--muted);background:var(--white);padding:2px 7px;border-radius:4px;border:1px solid var(--border);white-space:nowrap}}

/* ── SLA CARDS ── */
.sla-card{{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:8px}}
.sla-icon{{font-size:18px}}
.sla-title{{font-size:12px;font-weight:700;color:var(--navy)}}
.sla-sub{{font-size:11px;color:var(--muted)}}

/* ── RECORDINGS ── */
.rec-item{{background:var(--bg);border-radius:10px;padding:14px 16px;margin-bottom:8px;border:1px solid var(--border);cursor:pointer;transition:all .15s}}
.rec-item:hover{{border-color:var(--navy)}}
.rec-item.open{{border-color:var(--navy)}}
.rec-top{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}
.rec-caller{{font-weight:600;color:var(--navy);font-size:13px;flex:1}}
.rec-time{{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);white-space:nowrap}}
.rec-dur{{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);background:var(--white);padding:2px 7px;border-radius:4px;border:1px solid var(--border)}}
.rec-agent{{font-size:11px;color:var(--muted);background:rgba(10,61,92,.07);padding:2px 8px;border-radius:4px}}
.rec-body{{display:none;margin-top:12px;padding-top:12px;border-top:1px solid var(--border)}}
.rec-body.open{{display:block}}
.rec-summary{{background:rgba(10,61,92,.05);border-left:3px solid var(--navy);border-radius:0 6px 6px 0;padding:10px 14px;margin-bottom:10px;font-size:12px;color:var(--navy);line-height:1.6;font-style:italic}}
.rec-transcript{{font-size:12px;line-height:1.8;color:var(--text);max-height:180px;overflow-y:auto}}
.rec-transcript::-webkit-scrollbar{{width:3px}}.rec-transcript::-webkit-scrollbar-thumb{{background:var(--border)}}
.play-btn{{display:inline-flex;align-items:center;gap:6px;background:var(--navy);color:#fff;border:none;border-radius:6px;padding:6px 12px;font-size:11px;font-weight:600;cursor:pointer;margin-bottom:8px;text-decoration:none}}
.play-btn:hover{{background:#0d4f75}}

/* ── LOG / FORMS TABLES ── */
.tbl-filters{{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}}
.tbl-search{{flex:1;min-width:180px;background:var(--white);border:1px solid var(--border);border-radius:8px;padding:8px 13px;font-family:'DM Sans',sans-serif;font-size:12px;color:var(--text);outline:none}}
.tbl-search:focus{{border-color:var(--navy)}}
.tbl-search::placeholder{{color:var(--muted)}}
.tbl-sel{{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:8px 12px;font-family:'DM Sans',sans-serif;font-size:12px;color:var(--text);outline:none;cursor:pointer}}
.tbl-wrap{{overflow-x:auto;max-height:520px;overflow-y:auto}}
.tbl-wrap::-webkit-scrollbar{{width:5px;height:5px}}.tbl-wrap::-webkit-scrollbar-thumb{{background:var(--border);border-radius:3px}}
.ltbl{{width:100%;border-collapse:collapse;font-size:12px}}
.ltbl th{{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:0 12px 9px 0;text-align:left;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--white);white-space:nowrap}}
.ltbl td{{padding:8px 12px 8px 0;border-bottom:1px solid rgba(225,231,239,.4);vertical-align:middle;white-space:nowrap}}
.ltbl tr:hover td{{background:rgba(244,246,249,.8)}}
.ltbl tr:last-child td{{border-bottom:none}}
.dir-in{{color:var(--green);font-weight:700;font-size:10px;font-family:'Space Mono',monospace}}
.dir-out{{color:var(--blue);font-weight:700;font-size:10px;font-family:'Space Mono',monospace}}
.dir-form{{color:var(--purple);font-weight:700;font-size:10px;font-family:'Space Mono',monospace}}
.dir-sms{{color:var(--amber);font-weight:700;font-size:10px;font-family:'Space Mono',monospace}}
.st-ans{{color:var(--green)}}.st-mis{{color:var(--red)}}.st-oth{{color:var(--muted)}}
.new-badge{{background:rgba(61,255,192,.2);color:var(--navy);font-size:9px;font-family:'Space Mono',monospace;font-weight:700;padding:1px 5px;border-radius:3px;margin-left:4px}}
.fac-fw{{background:rgba(10,61,92,.1);color:var(--navy);font-size:10px;font-family:'Space Mono',monospace;font-weight:700;padding:2px 7px;border-radius:4px}}
.fac-wl{{background:rgba(61,255,192,.2);color:#0a5c3d;font-size:10px;font-family:'Space Mono',monospace;font-weight:700;padding:2px 7px;border-radius:4px}}
.new-pill{{background:rgba(16,185,129,.1);color:var(--green);font-size:10px;font-family:'Space Mono',monospace;font-weight:700;padding:2px 7px;border-radius:4px}}
.ret-pill{{background:rgba(107,126,150,.1);color:var(--muted);font-size:10px;font-family:'Space Mono',monospace;font-weight:700;padding:2px 7px;border-radius:4px}}
.t-badge{{font-family:'Space Mono',monospace;font-size:9px;background:rgba(59,130,246,.1);color:var(--blue);padding:1px 5px;border-radius:3px}}

/* ── PAGER ── */
.pager{{display:flex;align-items:center;justify-content:center;gap:8px;margin-top:14px;font-family:'Space Mono',monospace;font-size:11px}}
.pager-btn{{padding:5px 14px;border:1px solid var(--border);border-radius:6px;background:var(--white);cursor:pointer;color:var(--navy);font-weight:700;font-family:'Space Mono',monospace;font-size:11px}}
.pager-btn:hover{{background:var(--navy);color:#fff;border-color:var(--navy)}}
.pager-info{{color:var(--muted)}}

/* ── FACILITY SPLIT ── */
.fac-split{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px}}
.fac-big{{background:var(--white);border:1px solid var(--border);border-radius:14px;padding:22px 24px;box-shadow:var(--shadow)}}
.fac-name{{font-family:'Space Mono',monospace;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);margin-bottom:10px}}
.fac-num{{font-size:44px;font-weight:700;color:var(--navy);letter-spacing:-.04em;line-height:1}}
.fac-pct{{font-size:13px;color:var(--muted);margin-top:4px}}
.fac-stat{{display:flex;justify-content:space-between;font-size:12px;padding:5px 0;border-top:1px solid var(--border)}}
.fac-stat-lbl{{color:var(--muted)}}
.fac-stat-val{{font-weight:700;color:var(--navy);font-family:'Space Mono',monospace;font-size:11px}}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="tb-left">
    <div class="tb-logo">STRIVE</div>
    <div>
      <div class="tb-title">CTM Call Analytics</div>
      <div class="tb-sub">Provident Healthcare Consulting</div>
    </div>
  </div>
  <div class="tb-right">
    <div class="live-pill"><div class="live-dot"></div>LIVE</div>
    <div class="sync-lbl" id="syncLbl">—</div>
    <button class="btn-refresh" onclick="doRefresh()"><span class="spin" id="spinEl">↻</span> Refresh</button>
  </div>
</div>

<!-- TAB NAV -->
<div class="tab-nav">
  <button class="tnav active" onclick="showTab('overview',this)">Overview</button>
  <button class="tnav" onclick="showTab('agents',this)">Agent Performance</button>
  <button class="tnav" onclick="showTab('sources',this)">Sources &amp; Attribution</button>
  <button class="tnav" onclick="showTab('heatmap',this)">Heatmap &amp; Peak Hours</button>
  <button class="tnav" onclick="showTab('missed',this)">Missed Calls &amp; Recovery</button>
  <button class="tnav" onclick="showTab('facility',this)">Facility Split</button>
  <button class="tnav" onclick="showTab('newcallers',this)">New Callers / Leads</button>
  <button class="tnav" onclick="showTab('recordings',this)">Recordings &amp; Transcripts</button>
  <button class="tnav" onclick="showTab('calllog',this)">Live Call Log<span class="tab-badge">1,774</span></button>
  <button class="tnav" onclick="showTab('forms',this)">Contact Forms<span class="tab-badge">152</span></button>
  <button class="tnav" onclick="showTab('marketing',this)">Marketing &amp; Trends</button>
</div>

<div class="wrap">

<!-- OVERVIEW -->
<div id="tab-overview" class="tab-panel active">
  <div id="cb-overview"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(6,1fr)" id="ov-kpis"></div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Daily Call Volume</div><div class="card-sub">Inbound · Outbound · Missed</div></div><span class="chip" id="ov-period-chip">31 DAYS</span></div><div id="ov-daily-wrap"></div></div></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">New Callers vs Missed</div><div class="card-sub">Daily lead inflow vs miss risk</div></div></div><div id="ov-newmiss-wrap"></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Call Sources</div><div class="card-sub">Inbound attribution</div></div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;align-items:center"><div style="height:160px"><canvas id="ov-source"></canvas></div><div class="src-leg" id="ov-src-leg"></div></div></div>
  </div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Day of Week Volume</div><div class="card-sub">Total calls by weekday</div></div></div><div id="ov-dow"></div></div></div>
</div>

<!-- AGENTS -->
<div id="tab-agents" class="tab-panel">
  <div id="cb-agents"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="ag-kpis"></div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Agent Performance Detail</div><div class="card-sub">Named agents · Calls · Answer rate · Avg duration</div></div></div><table class="agt" id="agt-table"></table></div></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Calls by Agent</div></div></div><div style="height:220px"><canvas id="agt-bar"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Inbound vs Outbound Mix</div></div></div><div style="height:220px"><canvas id="agt-mix"></canvas></div></div>
  </div>
</div>

<!-- SOURCES -->
<div id="tab-sources" class="tab-panel">
  <div id="cb-sources"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="src-kpis"></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Source Share</div><div class="card-sub">Inbound by attribution · Numbers + %</div></div></div><div style="height:280px"><canvas id="src-donut"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Daily Volume by Source</div></div></div><div id="src-daily-wrap"></div></div>
  </div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Tracking Numbers</div></div></div><table class="ltbl" id="tn-table"></table></div></div>
</div>

<!-- HEATMAP -->
<div id="tab-heatmap" class="tab-panel">
  <div id="cb-heatmap"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="hm-kpis"></div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Inbound Call Heatmap</div><div class="card-sub">Calls per day × hour — deeper red = higher volume</div></div><span class="chip">INBOUND ONLY</span></div><div class="hm-outer" id="hm-container"></div></div></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Hourly Distribution</div></div></div><div style="height:220px"><canvas id="hm-hourly"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Weekday vs Weekend</div></div></div><div style="height:220px"><canvas id="hm-wknd"></canvas></div></div>
  </div>
</div>

<!-- MISSED -->
<div id="tab-missed" class="tab-panel">
  <div id="cb-missed"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="ms-kpis"></div>
  <div class="g2">
    <div class="card">
      <div class="card-h"><div><div class="card-title">Missed Calls Log</div><div class="card-sub">Most recent first</div></div><span class="chip" id="ms-chip">— TOTAL</span></div>
      <div class="missed-list" id="missed-list"></div>
    </div>
    <div class="card">
      <div class="card-h"><div><div class="card-title">Daily Missed Trend</div></div></div>
      <div id="miss-daily-wrap"></div>
      <div style="margin-top:16px;display:flex;flex-direction:column;gap:8px">
        <div class="sla-card" style="background:rgba(16,185,129,.06);border-left:3px solid var(--green)"><div class="sla-icon">⚡</div><div><div class="sla-title">15-min callback SLA</div><div class="sla-sub">Call back within 15 min of missed call</div></div></div>
        <div class="sla-card" style="background:rgba(245,158,11,.06);border-left:3px solid var(--amber)"><div class="sla-icon">📞</div><div><div class="sla-title">2 follow-up attempts</div><div class="sla-sub">Minimum 2 outbound attempts per missed call</div></div></div>
        <div class="sla-card" style="background:rgba(59,130,246,.06);border-left:3px solid var(--blue)"><div class="sla-icon">📱</div><div><div class="sla-title">Voicemail on attempt 1</div><div class="sla-sub">Leave VM on at least one outbound attempt</div></div></div>
      </div>
    </div>
  </div>
</div>

<!-- FACILITY -->
<div id="tab-facility" class="tab-panel">
  <div class="fac-split">
    <div class="fac-big"><div class="fac-name">🏢 Fort Wayne</div><div class="fac-num">1,616</div><div class="fac-pct">91.1% of all calls</div><div style="margin-top:14px;display:flex;flex-direction:column;gap:0"><div class="fac-stat"><span class="fac-stat-lbl">Google Biz (static)</span><span class="fac-stat-val">(260) 261-2663</span></div><div class="fac-stat"><span class="fac-stat-lbl">Primary IVR</span><span class="fac-stat-val">(260) 308-6324</span></div><div class="fac-stat"><span class="fac-stat-lbl">Google Organic</span><span class="fac-stat-val">(260) 544-2260</span></div><div class="fac-stat"><span class="fac-stat-lbl">Google Ads</span><span class="fac-stat-val">(260) 544-6060</span></div></div></div>
    <div class="fac-big"><div class="fac-name">🏢 Waterloo</div><div class="fac-num">158</div><div class="fac-pct">8.9% of all calls</div><div style="margin-top:14px;display:flex;flex-direction:column;gap:0"><div class="fac-stat"><span class="fac-stat-lbl">Waterloo #1</span><span class="fac-stat-val">(319) 319-6661</span></div><div class="fac-stat"><span class="fac-stat-lbl">Waterloo #2</span><span class="fac-stat-val">(319) 323-1119</span></div><div class="fac-stat"><span class="fac-stat-lbl">Form submissions</span><span class="fac-stat-val">61 of 152</span></div></div></div>
  </div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Volume by Facility</div></div></div><div style="height:250px"><canvas id="fac-donut"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Daily Volume by Facility</div></div></div><div style="height:250px"><canvas id="fac-daily"></canvas></div></div>
  </div>
  <div class="g1"><div class="card"><div class="card-h"><div><div class="card-title">Day of Week — Both Facilities</div></div></div><div id="fac-dow"></div></div></div>
</div>

<!-- NEW CALLERS -->
<div id="tab-newcallers" class="tab-panel">
  <div id="cb-newcallers"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="nc-kpis"></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">New Callers Daily Trend</div></div></div><div id="nc-daily-wrap"></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">New Callers by Day of Week</div></div></div><div style="height:220px"><canvas id="nc-dow"></canvas></div></div>
  </div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">New Callers by Hour</div></div></div><div style="height:220px"><canvas id="nc-hour"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">New Callers by Source</div></div></div><div style="height:220px"><canvas id="nc-source"></canvas></div></div>
  </div>
</div>

<!-- RECORDINGS -->
<div id="tab-recordings" class="tab-panel">
  <div id="cb-recordings"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="rec-kpis"></div>
  <div class="tbl-filters">
    <input type="text" class="tbl-search" id="rec-search" placeholder="Search name, summary, transcript..." oninput="renderRecs(1)">
    <select class="tbl-sel" id="rec-agent-sel" onchange="renderRecs(1)">
      <option value="">All Agents</option>
      <option>Shreenda Johnson</option><option>Gabrielle Joyce</option>
      <option>Louisse Cordero</option><option>Irvin Araos</option>
      <option>Brittney Collins</option><option>Heath Terhune</option>
    </select>
  </div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-bottom:10px" id="rec-count"></div>
  <div id="rec-list"></div>
  <div class="pager" id="rec-pager"></div>
</div>

<!-- CALL LOG -->
<div id="tab-calllog" class="tab-panel">
  <div id="cb-calllog"></div>
  <div class="tbl-filters">
    <input type="text" class="tbl-search" id="log-search" placeholder="Search name, number, city, agent..." oninput="renderLog(1)">
    <select class="tbl-sel" id="log-dir" onchange="renderLog(1)"><option value="">All Directions</option><option value="inbound">Inbound</option><option value="outbound">Outbound</option><option value="form">Form</option><option value="msg_inbound">SMS</option></select>
    <select class="tbl-sel" id="log-status" onchange="renderLog(1)"><option value="">All Statuses</option><option value="answered">Answered</option><option value="no-answer">No Answer</option><option value="busy">Busy</option><option value="completed">Completed</option></select>
    <select class="tbl-sel" id="log-new" onchange="renderLog(1)"><option value="">All Callers</option><option value="new">New Callers Only</option></select>
  </div>
  <div style="font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);margin-bottom:8px" id="log-count"></div>
  <div class="tbl-wrap">
    <table class="ltbl"><thead><tr><th>Date/Time</th><th>Dir</th><th>Number</th><th>Name</th><th>City</th><th>Source</th><th>Agent</th><th>Duration</th><th>Status</th><th>Fac</th><th>T</th></tr></thead><tbody id="log-body"></tbody></table>
  </div>
  <div class="pager" id="log-pager"></div>
</div>

<!-- FORMS -->
<div id="tab-forms" class="tab-panel">
  <div id="cb-forms"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(4,1fr)" id="fm-kpis"></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Form Submissions Over Time</div></div></div><div id="form-daily-wrap"></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Forms by Facility</div></div></div><div style="height:200px"><canvas id="form-fac"></canvas></div></div>
  </div>
  <div class="g1"><div class="card">
    <div class="card-h"><div><div class="card-title">All Form Submissions</div><div class="card-sub">All time — 152 leads</div></div><span class="chip" id="fm-chip">152</span></div>
    <div class="tbl-filters"><input type="text" class="tbl-search" id="form-search" placeholder="Search name, email, message..." oninput="renderForms()"></div>
    <div class="tbl-wrap" style="max-height:480px">
      <table class="ltbl"><thead><tr><th>Date</th><th>Name</th><th>How Can We Help?</th><th>Phone</th><th>Email</th><th>Location</th><th>Source</th><th>Facility</th><th>Type</th></tr></thead><tbody id="forms-tbody"></tbody></table>
    </div>
  </div></div>
</div>

<!-- MARKETING -->
<div id="tab-marketing" class="tab-panel">
  <div id="cb-marketing"></div>
  <div class="kpi-row" style="grid-template-columns:repeat(5,1fr)" id="mkt-kpis"></div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Call Volume Trend</div><div class="card-sub">Total · Inbound · New Callers · Missed</div></div></div><div id="mkt-trend-wrap"></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Lead Score: Yes / No</div><div class="card-sub">CTM AI-scored call outcomes</div></div></div><div id="mkt-yesno-wrap"></div></div>
  </div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Call Disposition</div><div class="card-sub">disposition_save_to_contact</div></div></div><div style="height:240px"><canvas id="mkt-disp"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Daily Lead Score Trend</div><div class="card-sub">Yes / No / Lead scored calls per day</div></div></div><div id="mkt-score-wrap"></div></div>
  </div>
  <div class="g2">
    <div class="card"><div class="card-h"><div><div class="card-title">Top Landing Pages</div><div class="card-sub">Page caller was on when they called</div></div></div><div style="height:240px"><canvas id="mkt-pages"></canvas></div></div>
    <div class="card"><div class="card-h"><div><div class="card-title">Referrer Domains</div><div class="card-sub">Where callers came from before your site</div></div></div><div style="height:240px"><canvas id="mkt-refs"></canvas></div></div>
  </div>
  <div class="g1"><div class="card">
    <div class="card-h"><div><div class="card-title">Agent Call Notes</div><div class="card-sub">Calls with agent notes — most recent first</div></div><span class="chip" id="notes-chip">101 NOTES</span></div>
    <div class="tbl-filters"><input type="text" class="tbl-search" id="notes-search" placeholder="Search notes, agent name..." oninput="renderNotes()"></div>
    <div class="tbl-wrap" style="max-height:400px">
      <table class="ltbl"><thead><tr><th>Date</th><th>Agent</th><th>Facility</th><th>Note</th></tr></thead><tbody id="notes-tbody"></tbody></table>
    </div>
  </div></div>
</div>

</div><!-- end wrap -->

<script>
// ═══════════════════════════════════════════════════════
// DATA — injected from CTM API via nightly build script
// ═══════════════════════════════════════════════════════
const SD    = {SD};
const DAILY = {DAILY};
const RECS  = {RECS};
const LOG   = {LOG};
const FORMS = {FORMS};
const MKT   = {MKT};

// ═══════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════
const DAYS_ORD  = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
const HOURS_ORD = ['07AM','08AM','09AM','10AM','11AM','12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM','08PM'];
const SRC_COLORS = {{
  'Google Business Profile - Static Number': '#0a3d5c',
  'Direct':          '#10b981',
  'Google Organic':  '#3b82f6',
  'Google Ads':      '#f59e0b',
  'Unknown':         '#8b5cf6'
}};
const SRC_BG = {{
  'Google Business Profile - Static Number': 'rgba(10,61,92,0.08)',
  'Direct':          'rgba(16,185,129,0.08)',
  'Google Organic':  'rgba(59,130,246,0.08)',
  'Google Ads':      'rgba(245,158,11,0.08)',
  'Unknown':         'rgba(139,92,246,0.08)'
}};
const SRC_BORDER = {{
  'Google Business Profile - Static Number': 'rgba(10,61,92,0.7)',
  'Direct':          'rgba(16,185,129,0.8)',
  'Google Organic':  'rgba(59,130,246,0.7)',
  'Google Ads':      'rgba(245,158,11,0.7)',
  'Unknown':         'rgba(139,92,246,0.7)'
}};

Chart.defaults.font.family = 'DM Sans';
Chart.defaults.color = '#6b7e96';
const CHARTS = {{}};

// ═══════════════════════════════════════════════════════
// STATE — single source of truth
// ═══════════════════════════════════════════════════════
let FAC    = 'all';  // 'all' | 'fw' | 'wl'
let PERIOD = '30d';  // '7d' | '30d' | 'all'
let GRAN   = 'day';  // 'day' | 'week' | 'month'

// ═══════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════
function mkChart(id, cfg) {{
  if (CHARTS[id]) CHARTS[id].destroy();
  const el = document.getElementById(id);
  if (!el) return null;
  CHARTS[id] = new Chart(el, cfg);
  return CHARTS[id];
}}

function kpiHTML(label, val, sub, cls) {{
  return `<div class="kpi ${{cls}}"><div class="kpi-lbl">${{label}}</div><div class="kpi-val">${{val}}</div><div class="kpi-sub">${{sub}}</div></div>`;
}}

function facLabel() {{
  return FAC === 'fw' ? 'Fort Wayne' : FAC === 'wl' ? 'Waterloo' : 'All Facilities';
}}

function shortSrc(s) {{
  return s.replace('Google Business Profile - Static Number','Google Business');
}}

function fmtDur(s) {{
  if (!s) return '—';
  return Math.floor(s/60) + 'm ' + (s%60) + 's';
}}

// ═══════════════════════════════════════════════════════
// PERIOD & GRANULARITY
// ═══════════════════════════════════════════════════════
function getPeriodDates() {{
  const all = Object.keys(DAILY).sort();
  if (PERIOD === 'all') return all;
  const days = PERIOD === '7d' ? 7 : 30;
  const latest = new Date(all[all.length - 1] + 'T12:00:00');
  const cutoff = new Date(latest);
  cutoff.setDate(cutoff.getDate() - days + 1);
  const cut = cutoff.toISOString().slice(0,10);
  return all.filter(d => d >= cut);
}}

function aggregateDates(dates) {{
  if (GRAN === 'day') return dates.map(d => ({{ label: fmtLabel(d), dates: [d] }}));

  if (GRAN === 'week') {{
    const weeks = {{}};
    dates.forEach(d => {{
      const dt = new Date(d + 'T12:00:00');
      const mon = new Date(dt);
      mon.setDate(dt.getDate() - ((dt.getDay()+6)%7));
      const wk = mon.toISOString().slice(0,10);
      if (!weeks[wk]) weeks[wk] = [];
      weeks[wk].push(d);
    }});
    return Object.entries(weeks).sort().map(([k,ds]) => ({{ label:'W/'+fmtLabel(k), dates:ds }}));
  }}

  if (GRAN === 'month') {{
    const months = {{}};
    dates.forEach(d => {{
      const mk = d.slice(0,7);
      if (!months[mk]) months[mk] = [];
      months[mk].push(d);
    }});
    const mn = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return Object.entries(months).sort().map(([k,ds]) => ({{ label: mn[parseInt(k.slice(5))-1]+' '+k.slice(2,4), dates:ds }}));
  }}

  return dates.map(d => ({{ label: fmtLabel(d), dates: [d] }}));
}}

function fmtLabel(d) {{
  const [,m,day] = d.split('-');
  return `${{parseInt(m)}}/${{parseInt(day)}}`;
}}

// Get aggregated metric value for a bucket, respecting FAC
function agg(dateBucket, key) {{
  const fkey = FAC === 'fw' ? 'fw_'+key : FAC === 'wl' ? 'wl_'+key : key;
  return dateBucket.reduce((s,d) => {{
    const row = DAILY[d];
    if (!row) return s;
    // For fw/wl use the prefixed key; fall back to unprefixed
    return s + (row[fkey] !== undefined ? row[fkey] : row[key] || 0);
  }}, 0);
}}

// Get source totals for selected period + facility
function getSrcTotals(dates) {{
  const totals = {{}};
  dates.forEach(d => {{
    const row = DAILY[d];
    if (!row || !row.src) return;
    const totalIb = row.inbound || 1;
    const facIb = FAC==='fw' ? (row.fw_inbound||0) : FAC==='wl' ? (row.wl_inbound||0) : totalIb;
    const ratio = FAC === 'all' ? 1 : (totalIb > 0 ? facIb / totalIb : 0);
    Object.entries(row.src).forEach(([k,v]) => {{
      totals[k] = (totals[k]||0) + Math.round(v * ratio);
    }});
  }});
  return Object.entries(totals).sort((a,b) => b[1]-a[1]);
}}

// Scrollable chart wrapper
function scrollWrap(canvasId, height, numPoints) {{
  const minW = Math.max(600, numPoints * 28);
  return `<div class="scroll-chart"><div style="min-width:${{minW}}px;height:${{height}}px"><canvas id="${{canvasId}}"></canvas></div></div>`;
}}

// DOW bars
function dowBars(elId, data) {{
  const max = Math.max(...Object.values(data).filter(v=>v>0), 1);
  document.getElementById(elId).innerHTML = DAYS_ORD.map(d => {{
    const v = data[d]||0, pct = v/max*100;
    const col = pct>80?'#0a3d5c':pct>50?'#3b82f6':'rgba(61,255,192,.8)';
    return `<div class="dow-row"><div class="dow-lbl">${{d.slice(0,3).toUpperCase()}}</div><div class="dow-track"><div class="dow-fill" style="width:${{pct}}%;background:${{col}}"></div></div><div class="dow-val">${{v}}</div></div>`;
  }}).join('');
}}

// ═══════════════════════════════════════════════════════
// CONTROL BAR — rendered on every tab
// ═══════════════════════════════════════════════════════
function buildCtrlBars() {{
  const tabs = ['overview','agents','sources','heatmap','missed','newcallers','recordings','calllog','forms','marketing'];
  tabs.forEach(tab => {{
    const el = document.getElementById('cb-'+tab);
    if (!el) return;
    el.innerHTML = `<div class="ctrl-bar">
      <div class="ctrl-group">
        <button class="ctrl-btn ${{FAC==='all'?'active':''}}" onclick="setFac('all','${{tab}}')">All Facilities</button>
        <button class="ctrl-btn ${{FAC==='fw'?'active':''}}"  onclick="setFac('fw','${{tab}}')">Fort Wayne</button>
        <button class="ctrl-btn ${{FAC==='wl'?'active':''}}"  onclick="setFac('wl','${{tab}}')">Waterloo</button>
      </div>
      <div class="ctrl-sep">|</div>
      <div class="ctrl-group">
        <button class="ctrl-btn ${{PERIOD==='7d'?'active':''}}"  onclick="setPeriod('7d','${{tab}}')">7D</button>
        <button class="ctrl-btn ${{PERIOD==='30d'?'active':''}}" onclick="setPeriod('30d','${{tab}}')">30D</button>
        <button class="ctrl-btn ${{PERIOD==='all'?'active':''}}" onclick="setPeriod('all','${{tab}}')">ALL</button>
      </div>
      <div class="ctrl-sep">|</div>
      <div class="ctrl-group">
        <button class="ctrl-btn ${{GRAN==='day'?'active':''}}"   onclick="setGran('day','${{tab}}')">DAY</button>
        <button class="ctrl-btn ${{GRAN==='week'?'active':''}}"  onclick="setGran('week','${{tab}}')">WEEK</button>
        <button class="ctrl-btn ${{GRAN==='month'?'active':''}}" onclick="setGran('month','${{tab}}')">MONTH</button>
      </div>
    </div>`;
  }});
}}

function setFac(fac, tab)    {{ FAC=fac;    buildCtrlBars(); rebuildTab(tab); }}
function setPeriod(p, tab)   {{ PERIOD=p;   buildCtrlBars(); rebuildTab(tab); }}
function setGran(g, tab)     {{ GRAN=g;     buildCtrlBars(); rebuildTab(tab); }}

function rebuildTab(tab) {{
  CHARTS['built_'+tab] = false;
  showTab(tab, document.querySelector(`.tnav[onclick*="'${{tab}}'"]`));
}}

// ═══════════════════════════════════════════════════════
// TAB SWITCHING
// ═══════════════════════════════════════════════════════
function showTab(name, btn) {{
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tnav').forEach(b => b.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  if (btn) btn.classList.add('active');
  window.scrollTo({{top:0, behavior:'smooth'}});
  if (!CHARTS['built_'+name]) {{
    CHARTS['built_'+name] = true;
    buildTab(name);
  }}
}}

function buildTab(n) {{
  if      (n==='overview')   buildOverview();
  else if (n==='agents')     buildAgents();
  else if (n==='sources')    buildSources();
  else if (n==='heatmap')    buildHeatmap();
  else if (n==='missed')     buildMissed();
  else if (n==='facility')   buildFacility();
  else if (n==='newcallers') buildNewCallers();
  else if (n==='recordings') {{ updateRecKPIs(); renderRecs(1); }}
  else if (n==='calllog')    renderLog(1);
  else if (n==='forms')      {{ buildFormCharts(); renderForms(); }}
  else if (n==='marketing')  buildMarketing();
}}

// ═══════════════════════════════════════════════════════
// OVERVIEW
// ═══════════════════════════════════════════════════════
function buildOverview() {{
  const dates   = getPeriodDates();
  const buckets = aggregateDates(dates);
  const labels  = buckets.map(b => b.label);

  const total  = dates.reduce((s,d) => s + (agg([d],'total')),   0);
  const ib     = dates.reduce((s,d) => s + (agg([d],'inbound')), 0);
  const missed = dates.reduce((s,d) => s + (agg([d],'missed')),  0);
  const nw     = dates.reduce((s,d) => s + (agg([d],'new')),     0);
  const ob     = total - ib;

  document.getElementById('ov-kpis').innerHTML =
    kpiHTML('Total Calls',  total.toLocaleString(),           facLabel(),                                          'kpi navy') +
    kpiHTML('Inbound',      ib.toLocaleString(),              `${{total>0?(ib/total*100).toFixed(1):0}}% of total`, 'kpi teal') +
    kpiHTML('Answer Rate',  total>0?((total-missed)/total*100).toFixed(1)+'%':'—', `${{(total-missed).toLocaleString()}} answered`, 'kpi blue') +
    kpiHTML('Missed',       missed.toLocaleString(),          `${{total>0?(missed/total*100).toFixed(1):0}}% miss rate`, 'kpi red') +
    kpiHTML('Outbound',     ob.toLocaleString(),              'Outbound calls',                                     'kpi amber') +
    kpiHTML('New Callers',  nw.toLocaleString(),              `${{ib>0?(nw/ib*100).toFixed(1):0}}% of inbound`,     'kpi green');

  // Daily volume — scrollable
  document.getElementById('ov-daily-wrap').innerHTML = scrollWrap('ov-daily', 220, buckets.length);
  mkChart('ov-daily', {{type:'bar', data:{{labels, datasets:[
    {{label:'Inbound',  data:buckets.map(b=>agg(b.dates,'inbound')),  backgroundColor:'rgba(10,61,92,.75)',   borderRadius:3, borderSkipped:false}},
    {{label:'Outbound', data:buckets.map(b=>agg(b.dates,'outbound')), backgroundColor:'rgba(61,255,192,.45)', borderRadius:3, borderSkipped:false}},
    {{label:'Missed', type:'line', data:buckets.map(b=>agg(b.dates,'missed')), borderColor:'#ef4444', backgroundColor:'rgba(239,68,68,.08)', borderWidth:2, pointRadius:2, tension:.3, fill:false, yAxisID:'y2'}}
  ]}}, options:{{responsive:true, maintainAspectRatio:false,
    plugins:{{legend:{{position:'bottom', labels:{{font:{{size:11}}, boxWidth:10, padding:10}}}}}},
    scales:{{
      x:{{stacked:true, grid:{{display:false}}, ticks:{{font:{{family:'Space Mono',size:8}}, maxRotation:45}}}},
      y:{{stacked:true, grid:{{color:'rgba(225,231,239,.6)'}}, ticks:{{font:{{family:'Space Mono',size:9}}}}}},
      y2:{{position:'right', grid:{{display:false}}, ticks:{{font:{{family:'Space Mono',size:9}}, color:'#ef4444'}}, max:15}}
    }}
  }}}});

  // New callers vs missed — scrollable
  document.getElementById('ov-newmiss-wrap').innerHTML = scrollWrap('ov-newmiss', 200, buckets.length);
  mkChart('ov-newmiss', {{type:'line', data:{{labels, datasets:[
    {{label:'New Callers', data:buckets.map(b=>agg(b.dates,'new')),    borderColor:'#0a3d5c', backgroundColor:'rgba(10,61,92,.07)',   borderWidth:2, pointRadius:2.5, tension:.3, fill:true}},
    {{label:'Missed',      data:buckets.map(b=>agg(b.dates,'missed')), borderColor:'#ef4444', backgroundColor:'rgba(239,68,68,.05)', borderWidth:2, pointRadius:2.5, tension:.3, fill:true}}
  ]}}, options:{{responsive:true, maintainAspectRatio:false,
    plugins:{{legend:{{position:'bottom', labels:{{font:{{size:11}}, boxWidth:10, padding:10}}}}}},
    scales:{{x:{{grid:{{display:false}}, ticks:{{font:{{family:'Space Mono',size:8}}, maxRotation:45}}}}, y:{{grid:{{color:'rgba(225,231,239,.6)'}}, ticks:{{font:{{family:'Space Mono',size:9}}}}, beginAtZero:true}}}}
  }}}});

  // Source donut (overview version — uses full period)
  const srcArr = getSrcTotals(dates);
  const srcTotal = srcArr.reduce((s,[,v]) => s+v, 0);
  mkChart('ov-source', {{type:'doughnut', data:{{
    labels: srcArr.map(([k]) => shortSrc(k)),
    datasets:[{{data:srcArr.map(([,v])=>v), backgroundColor:srcArr.map(([k])=>SRC_COLORS[k]||'#8b5cf6'), borderWidth:2, borderColor:'#fff'}}]
  }}, options:{{responsive:true, maintainAspectRatio:false, cutout:'65%',
    plugins:{{legend:{{display:false}}, tooltip:{{callbacks:{{label:c=>` ${{c.label}}: ${{c.raw.toLocaleString()}} (${{(c.raw/srcTotal*100).toFixed(1)}}%)`}}}}}}
  }}}});
  document.getElementById('ov-src-leg').innerHTML = srcArr.slice(0,4).map(([k,v]) =>
    `<div class="src-row"><div class="src-dot" style="background:${{SRC_COLORS[k]||'#8b5cf6'}}"></div><div class="src-name">${{shortSrc(k)}}</div><div class="src-pct">${{srcTotal>0?(v/srcTotal*100).toFixed(0):0}}%</div><div class="src-cnt">${{v.toLocaleString()}}</div></div>`
  ).join('');

  // DOW bars
  const dow = FAC==='fw'?SD.dow_fw:FAC==='wl'?SD.dow_wl:SD.dow_all;
  dowBars('ov-dow', dow);
}}

// ═══════════════════════════════════════════════════════
// AGENTS
// ═══════════════════════════════════════════════════════
function buildAgents() {{
  const agents = Object.entries(SD.agents).map(([name,s]) => {{
    const facTotal = FAC==='fw'?s.fw : FAC==='wl'?s.wl : s.total;
    return {{name, ...s, facTotal}};
  }}).filter(a => a.facTotal > 0).sort((a,b) => b.facTotal - a.facTotal);

  const maxT  = Math.max(...agents.map(a=>a.facTotal), 1);
  const total = agents.reduce((s,a) => s+a.facTotal, 0);
  const top   = agents[0]?.name.split(' ')[0] || '—';

  document.getElementById('ag-kpis').innerHTML =
    kpiHTML('Named Agents',    agents.length,               'Active in period',          'kpi navy') +
    kpiHTML('Agent Calls',     total.toLocaleString(),      facLabel(),                  'kpi blue') +
    kpiHTML('Avg Answer Rate', agents.length>0?Math.round(agents.reduce((s,a)=>s+(a.answered/Math.max(a.total,1)*100),0)/agents.length)+'%':'—', 'Named agents', 'kpi green') +
    kpiHTML('Top Agent',       `<span style="font-size:18px">${{top}}</span>`, `${{agents[0]?.facTotal||0}} calls`, 'kpi amber');

  document.getElementById('agt-table').innerHTML =
    `<thead><tr><th>Agent</th><th>Total</th><th>In / Out</th><th>Answer Rate</th><th>Avg Duration</th><th>Missed</th></tr></thead><tbody>` +
    agents.map(a => {{
      const init = a.name.split(' ').map(x=>x[0]).join('').slice(0,2);
      const rate = Math.round(a.answered / Math.max(a.total,1) * 100);
      const rc   = rate>=98?'rhi':rate>=90?'rmd':'rlo';
      const avg  = a.dur_n>0 ? a.dur/a.dur_n : 0;
      const ds   = avg>=60 ? `${{Math.floor(avg/60)}}m ${{Math.round(avg%60)}}s` : `${{Math.round(avg)}}s`;
      return `<tr>
        <td><div class="aname"><div class="av">${{init}}</div>${{a.name}}</div></td>
        <td><div class="bar-row"><div class="bar-track"><div class="bar-fill" style="width:${{a.facTotal/maxT*100}}%"></div></div><span style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#0a3d5c">${{a.facTotal}}</span></div></td>
        <td style="font-family:'Space Mono',monospace;font-size:11px;color:#6b7e96">${{a.inbound}}↓ ${{a.outbound}}↑</td>
        <td><span class="rbadge ${{rc}}">${{rate}}%</span></td>
        <td style="font-family:'Space Mono',monospace;font-size:11px;color:#6b7e96">${{ds}}</td>
        <td style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:${{a.missed>0?'#ef4444':'#10b981'}}">${{a.missed}}</td>
      </tr>`;
    }}).join('') + '</tbody>';

  const names = agents.map(a => a.name.split(' ')[0]);
  mkChart('agt-bar', {{type:'bar', data:{{labels:names, datasets:[{{label:'Total', data:agents.map(a=>a.facTotal), backgroundColor:'rgba(10,61,92,.75)', borderRadius:6, borderSkipped:false}}]}},
    options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{display:false}}}}, scales:{{x:{{grid:{{display:false}}, ticks:{{font:{{size:11}}}}}}, y:{{grid:{{color:'rgba(225,231,239,.6)'}}, ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});
  mkChart('agt-mix', {{type:'bar', data:{{labels:names, datasets:[
    {{label:'Inbound',  data:agents.map(a=>a.inbound),  backgroundColor:'rgba(10,61,92,.7)',   borderRadius:4, borderSkipped:false}},
    {{label:'Outbound', data:agents.map(a=>a.outbound), backgroundColor:'rgba(61,255,192,.6)', borderRadius:4, borderSkipped:false}}
  ]}}, options:{{responsive:true, maintainAspectRatio:false, plugins:{{legend:{{position:'bottom', labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}}, scales:{{x:{{stacked:true,grid:{{display:false}},ticks:{{font:{{size:11}}}}}}, y:{{stacked:true, grid:{{color:'rgba(225,231,239,.6)'}}, ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});
}}

// ═══════════════════════════════════════════════════════
// SOURCES
// ═══════════════════════════════════════════════════════
function buildSources() {{
  const dates  = getPeriodDates();
  const srcArr = getSrcTotals(dates);
  const total  = srcArr.reduce((s,[,v]) => s+v, 0);
  const buckets= aggregateDates(dates);

  document.getElementById('src-kpis').innerHTML = srcArr.slice(0,4).map(([k,v],i) =>
    kpiHTML(shortSrc(k), v.toLocaleString(), `${{total>0?(v/total*100).toFixed(1):0}}% of inbound`, ['kpi navy','kpi blue','kpi teal','kpi amber'][i])
  ).join('');

  // Donut with counts in legend labels (FIX 6)
  mkChart('src-donut', {{type:'doughnut', data:{{
    labels: srcArr.map(([k]) => shortSrc(k)),
    datasets:[{{data:srcArr.map(([,v])=>v), backgroundColor:srcArr.map(([k])=>SRC_COLORS[k]||'#8b5cf6'), borderWidth:3, borderColor:'#fff'}}]
  }}, options:{{responsive:true, maintainAspectRatio:false, cutout:'55%',
    plugins:{{
      legend:{{position:'bottom', labels:{{
        font:{{size:11}}, boxWidth:10, padding:8,
        generateLabels(chart) {{
          return chart.data.labels.map((lbl,i) => ({{
            text: `${{lbl}}  ${{chart.data.datasets[0].data[i].toLocaleString()}} (${{total>0?(chart.data.datasets[0].data[i]/total*100).toFixed(0):0}}%)`,
            fillStyle: chart.data.datasets[0].backgroundColor[i],
            strokeStyle:'#fff', lineWidth:2, index:i
          }}));
        }}
      }}}},
      tooltip:{{callbacks:{{label:c=>` ${{c.label}}: ${{c.raw.toLocaleString()}} (${{(c.raw/total*100).toFixed(1)}}%)`}}}}
    }}
  }}}});

  // Daily by source — light colors, period-aware (FIX 5 + 7)
  document.getElementById('src-daily-wrap').innerHTML = scrollWrap('src-daily', 240, buckets.length);
  // Build source daily datasets outside mkChart to avoid f-string nesting issues
  const srcDailyDatasets = srcArr.slice(0,4).map(([k]) => {{
    return {{
      label: shortSrc(k),
      data: buckets.map(b => b.dates.reduce((s,d) => {{
        const row = DAILY[d];
        if (!row || !row.src) return s;
        const totalIb = row.inbound||1;
        const facIb   = FAC==='fw'?(row.fw_inbound||0):FAC==='wl'?(row.wl_inbound||0):totalIb;
        const facRatio= FAC==='all'?1:(totalIb>0?facIb/totalIb:0);
        return s + Math.round((row.src[k]||0) * facRatio);
      }}, 0)),
      borderColor:     SRC_BORDER[k]||'rgba(139,92,246,0.7)',
      backgroundColor: SRC_BG[k]||'rgba(139,92,246,0.08)',
      borderWidth:2, pointRadius:2, tension:0.3, fill:true
    }};
  }});
  mkChart('src-daily', {{
    type:'line',
    data:{{labels:buckets.map(b=>b.label), datasets:srcDailyDatasets}},
    options:{{
      responsive:true, maintainAspectRatio:false,
      plugins:{{legend:{{position:'bottom', labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}},
      scales:{{
        x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},
        y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}
      }}
    }}
  }});

  // Tracking numbers
  const tns = FAC==='wl'?[
    {{number:'(319) 319-6661',label:'Waterloo #1',source:'Google Organic',calls:98}},
    {{number:'(319) 323-1119',label:'Waterloo #2',source:'Google Business',calls:60}}
  ]:FAC==='fw'?[
    {{number:'(260) 261-2663',label:'Google Business Profile (static)',source:'Google Business',calls:921}},
    {{number:'(260) 308-6324',label:'IVR / Internal',source:'Direct',calls:546}},
    {{number:'(260) 544-2260',label:'Google Organic FW',source:'Google Organic',calls:115}},
    {{number:'(260) 544-6060',label:'Google Ads FW',source:'Google Ads',calls:34}}
  ]:[
    {{number:'(260) 261-2663',label:'Google Business Profile (static)',source:'Google Business',calls:921}},
    {{number:'(260) 308-6324',label:'IVR / Internal',source:'Direct',calls:546}},
    {{number:'(260) 544-2260',label:'Google Organic FW',source:'Google Organic',calls:115}},
    {{number:'(319) 319-6661',label:'Waterloo #1',source:'Google Organic',calls:98}},
    {{number:'(319) 323-1119',label:'Waterloo #2',source:'Google Business',calls:60}},
    {{number:'(260) 544-6060',label:'Google Ads FW',source:'Google Ads',calls:34}}
  ];
  const tnT = tns.reduce((s,t)=>s+t.calls,0);
  document.getElementById('tn-table').innerHTML =
    `<thead><tr><th>Number</th><th>Label</th><th>Source</th><th>Calls</th><th>Share</th></tr></thead><tbody>` +
    tns.map(t=>`<tr>
      <td style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#0a3d5c">${{t.number}}</td>
      <td style="font-size:12px;color:#6b7e96">${{t.label}}</td>
      <td style="font-size:11px;color:#6b7e96">${{t.source}}</td>
      <td style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#0a3d5c">${{t.calls.toLocaleString()}}</td>
      <td style="font-family:'Space Mono',monospace;font-size:10px;color:#6b7e96">${{(t.calls/tnT*100).toFixed(1)}}%</td>
    </tr>`).join('') + '</tbody>';
}}

// ═══════════════════════════════════════════════════════
// HEATMAP
// ═══════════════════════════════════════════════════════
function buildHeatmap() {{
  const hm = FAC==='fw'?SD.hm_fw:FAC==='wl'?SD.hm_wl:SD.hm_all;
  const maxV = Math.max(...Object.values(hm).filter(v=>v>0), 1);

  const hourTotals = {{}};
  HOURS_ORD.forEach(h => {{ hourTotals[h] = DAYS_ORD.reduce((s,d) => s+(hm[`${{d}}|${{h}}`]||0), 0); }});
  const dowTotals = {{}};
  DAYS_ORD.forEach(d => {{ dowTotals[d] = HOURS_ORD.reduce((s,h) => s+(hm[`${{d}}|${{h}}`]||0), 0); }});
  let hotV=0, hotC='';
  Object.entries(hm).forEach(([k,v]) => {{ if(v>hotV){{hotV=v; hotC=k.replace('|',' ');}} }});
  const peakHour = HOURS_ORD.reduce((a,b) => hourTotals[a]>hourTotals[b]?a:b);
  const peakDay  = DAYS_ORD.reduce((a,b) => dowTotals[a]>dowTotals[b]?a:b);
  const dow      = FAC==='fw'?SD.dow_fw:FAC==='wl'?SD.dow_wl:SD.dow_all;
  const wkend    = (dow['Saturday']||0)+(dow['Sunday']||0);

  document.getElementById('hm-kpis').innerHTML =
    kpiHTML('Peak Hour',      peakHour,                                              'Highest call density', 'kpi navy') +
    kpiHTML('Busiest Day',    `<span style="font-size:20px">${{peakDay}}</span>`,    `${{dowTotals[peakDay]||0}} calls`, 'kpi teal') +
    kpiHTML('Hottest Cell',   `<span style="font-size:18px">${{hotC}}</span>`,       `${{hotV}} calls`,      'kpi blue') +
    kpiHTML('Weekend Volume', wkend.toLocaleString(),                                'Sat + Sun',            'kpi amber');

  // Build heatmap grid — red color scheme (FIX 8)
  let html = '<div class="hm-grid"><div class="hm-hrow"><div></div>';
  DAYS_ORD.forEach(d => {{ html += `<div class="hm-dlbl">${{d.slice(0,3)}}</div>`; }});
  html += '</div>';
  HOURS_ORD.forEach(h => {{
    html += '<div class="hm-row">';
    html += `<div class="hm-hlbl">${{h}}</div>`;
    DAYS_ORD.forEach(d => {{
      const v = hm[`${{d}}|${{h}}`]||0;
      const p = v/maxV;
      const bg = v===0 ? 'rgba(245,245,245,0.5)' : `rgba(239,68,68,${{(0.06+p*0.92).toFixed(2)}})`;
      const tc = p>0.55 ? 'rgba(255,255,255,.95)' : p>0.15 ? 'rgba(160,20,20,.9)' : 'transparent';
      html += `<div class="hm-cell" style="background:${{bg}};color:${{tc}}" title="${{d}} ${{h}}: ${{v}} calls">${{v>0?v:''}}</div>`;
    }});
    html += '</div>';
  }});
  html += '</div>';
  document.getElementById('hm-container').innerHTML = html;

  // Hourly bar
  mkChart('hm-hourly', {{type:'bar', data:{{labels:HOURS_ORD, datasets:[{{label:'Calls',
    data:HOURS_ORD.map(h=>hourTotals[h]),
    backgroundColor:HOURS_ORD.map(h=>{{const hp=hourTotals[h]/Math.max(...Object.values(hourTotals),1);return hp>0.8?'rgba(239,68,68,0.85)':hp>0.5?'rgba(239,68,68,0.55)':'rgba(239,68,68,0.25)'}}),
    borderRadius:5, borderSkipped:false
  }}]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:9}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});

  const wkday = DAYS_ORD.slice(0,5).reduce((s,d)=>s+(dow[d]||0),0);
  const wkend2= DAYS_ORD.slice(5).reduce((s,d)=>s+(dow[d]||0),0);
  mkChart('hm-wknd', {{type:'doughnut', data:{{labels:['Weekday (Mon–Fri)','Weekend (Sat–Sun)'],datasets:[{{data:[wkday,wkend2],backgroundColor:['#0a3d5c','#3dffc0'],borderWidth:3,borderColor:'#fff'}}]}},
    options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}}}}
  }});
}}

// ═══════════════════════════════════════════════════════
// MISSED
// ═══════════════════════════════════════════════════════
function buildMissed() {{
  const dates   = getPeriodDates();
  const buckets = aggregateDates(dates);
  const total   = dates.reduce((s,d)=>s+agg([d],'missed'),0);
  const ib      = dates.reduce((s,d)=>s+agg([d],'inbound'),0);
  const worst   = dates.reduce((a,d) => agg([d],'missed')>agg([a],'missed')?d:a, dates[0]||'—');

  document.getElementById('ms-kpis').innerHTML =
    kpiHTML('Total Missed', total,                                                     'No-answer + busy',  'kpi red') +
    kpiHTML('Miss Rate',    ib>0?(total/ib*100).toFixed(1)+'%':'0%',                  'Of inbound',        'kpi amber') +
    kpiHTML('Avg / Day',    (total/Math.max(dates.length,1)).toFixed(1),               `Over ${{dates.length}} days`, 'kpi navy') +
    kpiHTML('Worst Day',    `<span style="font-size:18px">${{worst.slice(5)}}</span>`, `${{agg([worst],'missed')}} missed`, 'kpi blue');

  const log = SD.missed_all.filter(m => FAC==='all'||(FAC==='fw'&&m.fa==='Fort Wayne')||(FAC==='wl'&&m.fa==='Waterloo'));
  document.getElementById('ms-chip').textContent = log.length+' TOTAL';
  document.getElementById('missed-list').innerHTML = log.map(m =>
    `<div class="mitem"><div class="mtime">${{m.time}}</div><div class="mcaller">${{m.caller}}</div><div class="msrc">${{m.source}}</div></div>`
  ).join('');

  document.getElementById('miss-daily-wrap').innerHTML = scrollWrap('miss-daily', 180, buckets.length);
  mkChart('miss-daily', {{type:'bar', data:{{labels:buckets.map(b=>b.label), datasets:[{{label:'Missed',
    data:buckets.map(b=>agg(b.dates,'missed')),
    backgroundColor:buckets.map(b=>{{const v=agg(b.dates,'missed');return v>=7?'#ef4444':v>=4?'#f59e0b':'rgba(239,68,68,.4)'}}),
    borderRadius:5, borderSkipped:false
  }}]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}}}
  }});
}}

// ═══════════════════════════════════════════════════════
// FACILITY
// ═══════════════════════════════════════════════════════
function buildFacility() {{
  mkChart('fac-donut', {{type:'doughnut', data:{{labels:['Fort Wayne (260)','Waterloo (319)'],datasets:[{{data:[1616,158],backgroundColor:['#0a3d5c','#3dffc0'],borderWidth:3,borderColor:'#fff'}}]}},
    options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}}}}
  }});
  const dates = Object.keys(DAILY).sort();
  const lbls  = dates.map(d=>{{const[,m,day]=d.split('-');return`${{parseInt(m)}}/${{parseInt(day)}}`}});
  mkChart('fac-daily', {{type:'line', data:{{labels:lbls, datasets:[
    {{label:'Fort Wayne', data:dates.map(d=>DAILY[d]?.fw_total||0),  borderColor:'#0a3d5c',backgroundColor:'rgba(10,61,92,.07)',  borderWidth:2,pointRadius:1.5,tension:.3,fill:true}},
    {{label:'Waterloo',   data:dates.map(d=>DAILY[d]?.wl_total||0),  borderColor:'#3dffc0',backgroundColor:'rgba(61,255,192,.07)',borderWidth:2,pointRadius:1.5,tension:.3,fill:true}}
  ]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});
  dowBars('fac-dow', SD.dow_all);
}}

// ═══════════════════════════════════════════════════════
// NEW CALLERS
// ═══════════════════════════════════════════════════════
function buildNewCallers() {{
  const dates   = getPeriodDates();
  const buckets = aggregateDates(dates);
  const total   = dates.reduce((s,d)=>s+agg([d],'new'),0);
  const ib      = dates.reduce((s,d)=>s+agg([d],'inbound'),0);
  const ncDow   = FAC==='fw'?SD.nc_dow_fw:FAC==='wl'?SD.nc_dow_wl:SD.nc_dow_all;
  const ncHr    = FAC==='fw'?SD.nc_hr_fw:FAC==='wl'?SD.nc_hr_wl:SD.nc_hr_all;
  const peakDay = DAYS_ORD.reduce((a,b)=>(ncDow[a]||0)>(ncDow[b]||0)?a:b);

  document.getElementById('nc-kpis').innerHTML =
    kpiHTML('New Callers',     total.toLocaleString(),                                  facLabel(),        'kpi green') +
    kpiHTML('Avg / Day',       (total/Math.max(dates.length,1)).toFixed(1),             'New leads/day',   'kpi navy') +
    kpiHTML('New Caller Rate', ib>0?(total/ib*100).toFixed(1)+'%':'0%',                'Of inbound',      'kpi teal') +
    kpiHTML('Peak Day',        `<span style="font-size:20px">${{peakDay}}</span>`,      `${{ncDow[peakDay]||0}} new callers`, 'kpi blue');

  document.getElementById('nc-daily-wrap').innerHTML = scrollWrap('nc-daily', 200, buckets.length);
  mkChart('nc-daily', {{type:'line', data:{{labels:buckets.map(b=>b.label), datasets:[{{label:'New Callers',
    data:buckets.map(b=>agg(b.dates,'new')),
    borderColor:'#10b981',backgroundColor:'rgba(16,185,129,.08)',borderWidth:2.5,pointRadius:3,tension:.3,fill:true
  }}]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}}}
  }});
  mkChart('nc-dow', {{type:'bar', data:{{labels:DAYS_ORD.map(d=>d.slice(0,3)), datasets:[{{label:'New Callers',
    data:DAYS_ORD.map(d=>ncDow[d]||0),
    backgroundColor:DAYS_ORD.map((_,i)=>i<5?'rgba(10,61,92,.75)':'rgba(61,255,192,.6)'),borderRadius:5,borderSkipped:false
  }}]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{size:11}}}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}}}
  }});
  const hrs = HOURS_ORD.filter(h=>ncHr[h]);
  const maxHr = Math.max(...hrs.map(h=>ncHr[h]),1);
  mkChart('nc-hour', {{type:'bar', data:{{labels:hrs, datasets:[{{label:'New Callers',
    data:hrs.map(h=>ncHr[h]||0),
    backgroundColor:hrs.map(h=>{{const p=ncHr[h]/maxHr;return p>0.8?'#0a3d5c':p>0.5?'#3b82f6':'rgba(61,255,192,.7)'}}),
    borderRadius:5,borderSkipped:false
  }}]}}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:9}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}}}
  }});
  const srcTots = getSrcTotals(dates);
  mkChart('nc-source', {{type:'doughnut', data:{{
    labels:srcTots.map(([k])=>shortSrc(k)),
    datasets:[{{data:srcTots.map(([,v])=>v),backgroundColor:srcTots.map(([k])=>SRC_COLORS[k]||'#8b5cf6'),borderWidth:3,borderColor:'#fff'}}]
  }}, options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}}}}
  }});
}}

// ═══════════════════════════════════════════════════════
// RECORDINGS
// ═══════════════════════════════════════════════════════
function updateRecKPIs() {{
  const filtered = filterRecs();
  document.getElementById('rec-kpis').innerHTML =
    kpiHTML('Total Recordings', RECS.filter(r=>FAC==='all'||(r.f===(FAC==='fw'?'Fort Wayne':'Waterloo'))).length.toLocaleString(), facLabel(), 'kpi navy') +
    kpiHTML('With AI Summary',  RECS.filter(r=>r.su).length.toLocaleString(), 'Auto-generated',    'kpi blue') +
    kpiHTML('Fort Wayne',       RECS.filter(r=>r.f==='Fort Wayne').length.toLocaleString(), '92.7%', 'kpi teal') +
    kpiHTML('Waterloo',         RECS.filter(r=>r.f==='Waterloo').length.toLocaleString(),   '7.3%',  'kpi green');
}}

function filterRecs() {{
  const q  = (document.getElementById('rec-search')?.value||'').toLowerCase();
  const ag = (document.getElementById('rec-agent-sel')?.value||'').toLowerCase();
  return RECS.filter(r => {{
    const facOk = FAC==='all'||r.f===(FAC==='fw'?'Fort Wayne':'Waterloo');
    const txt   = (r.c+r.su+r.tr+r.a+r.p).toLowerCase();
    return facOk && (!q||txt.includes(q)) && (!ag||r.a.toLowerCase().includes(ag));
  }});
}}

function renderRecs(page) {{
  const REC_PS = 50;
  const items  = filterRecs();
  const pages  = Math.ceil(items.length/REC_PS);
  const slice  = items.slice((page-1)*REC_PS, page*REC_PS);
  document.getElementById('rec-count').textContent = `Showing ${{(page-1)*REC_PS+1}}–${{Math.min(page*REC_PS,items.length)}} of ${{items.length.toLocaleString()}} recordings`;
  document.getElementById('rec-list').innerHTML = slice.map((r,i) => {{
    const idx = (page-1)*REC_PS+i;
    return `<div class="rec-item" id="ri${{idx}}" onclick="toggleRec(${{idx}})">
      <div class="rec-top">
        <div class="rec-caller">${{r.c||r.p}}</div>
        <div class="rec-time">${{r.t}}</div>
        <div class="rec-dur">${{r.d}}</div>
        ${{r.a?`<div class="rec-agent">${{r.a}}</div>`:''}}
        <div style="font-size:10px;color:#6b7e96;padding:2px 7px;background:#f4f6f9;border-radius:4px;border:1px solid #e1e7ef">${{r.s}}</div>
        <span class="${{r.f==='Fort Wayne'?'fac-fw':'fac-wl'}}">${{r.f==='Fort Wayne'?'FW':'WL'}}</span>
      </div>
      <div class="rec-body" id="rb${{idx}}">
        ${{r.su?`<div class="rec-summary">💡 ${{r.su}}</div>`:''}}
        ${{r.au?`<a class="play-btn" href="${{r.au}}" target="_blank" rel="noopener">▶ Open in CTM</a>`:'<span style="font-size:11px;color:#6b7e96">No recording URL</span>'}}
        ${{r.tr?`<div class="rec-transcript">${{r.tr.replace(/\\n/g,'<br>')}}<br><em style="color:#6b7e96;font-size:10px">...transcript preview</em></div>`:''}}
      </div>
    </div>`;
  }}).join('');
  const pg = document.getElementById('rec-pager');
  pg.innerHTML = pages>1 ? [
    page>1?`<button class="pager-btn" onclick="renderRecs(${{page-1}})">← Prev</button>`:'',
    `<span class="pager-info">Page ${{page}} of ${{pages}}</span>`,
    page<pages?`<button class="pager-btn" onclick="renderRecs(${{page+1}})">Next →</button>`:''
  ].join('') : '';
}}

function toggleRec(i) {{
  document.getElementById('ri'+i)?.classList.toggle('open');
  document.getElementById('rb'+i)?.classList.toggle('open');
}}

// ═══════════════════════════════════════════════════════
// CALL LOG
// ═══════════════════════════════════════════════════════
function filterLog() {{
  const q      = (document.getElementById('log-search')?.value||'').toLowerCase();
  const dir    = document.getElementById('log-dir')?.value||'';
  const status = document.getElementById('log-status')?.value||'';
  const newOnly= document.getElementById('log-new')?.value==='new';
  return LOG.filter(c => {{
    const facOk = FAC==='all'||c.fa===(FAC==='fw'?'Fort Wayne':'Waterloo');
    const txt   = ((c.nm||'')+(c.cl||'')+(c.ci||'')+(c.ag||'')+(c.sr||'')).toLowerCase();
    const stOk  = !status||(c.st===status)||(status==='no-answer'&&c.st==='no answer');
    return facOk && (!q||txt.includes(q)) && (!dir||c.di===dir) && stOk && (!newOnly||c.nw);
  }});
}}

function renderLog(page) {{
  const LOG_PS = 100;
  const items  = filterLog();
  const pages  = Math.ceil(items.length/LOG_PS);
  const slice  = items.slice((page-1)*LOG_PS, page*LOG_PS);
  const start  = (page-1)*LOG_PS+1;
  const end    = Math.min(page*LOG_PS, items.length);
  document.getElementById('log-count').textContent = `Showing ${{start.toLocaleString()}}–${{end.toLocaleString()}} of ${{items.length.toLocaleString()}} calls`;
  const dirCls = {{inbound:'dir-in',outbound:'dir-out',form:'dir-form',msg_inbound:'dir-sms'}};
  const stCls  = s => ['answered','completed'].includes(s)?'st-ans':['no-answer','busy','missed','no answer'].includes(s)?'st-mis':'st-oth';
  document.getElementById('log-body').innerHTML = slice.map(c => `<tr>
    <td style="font-family:'Space Mono',monospace;font-size:10px;color:#6b7e96">${{c.dt}}</td>
    <td><span class="${{dirCls[c.di]||'dir-in'}}">${{c.di.toUpperCase()}}</span></td>
    <td style="font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#0a3d5c">${{c.cl}}</td>
    <td style="font-size:12px">${{c.nm}}${{c.nw?'<span class="new-badge">NEW</span>':''}}</td>
    <td style="font-size:11px;color:#6b7e96">${{c.ci}}${{c.sa?', '+c.sa:''}}</td>
    <td style="font-size:11px;color:#6b7e96">${{c.sr}}</td>
    <td style="font-size:11px;color:#6b7e96">${{c.ag||'—'}}</td>
    <td style="font-family:'Space Mono',monospace;font-size:10px;color:#6b7e96">${{fmtDur(c.du)}}</td>
    <td><span class="${{stCls(c.st)}}" style="font-family:'Space Mono',monospace;font-size:10px;font-weight:700">${{c.st}}</span></td>
    <td><span class="${{c.fa==='Fort Wayne'?'fac-fw':'fac-wl'}}">${{c.fa==='Fort Wayne'?'FW':'WL'}}</span></td>
    <td>${{c.tr?'<span class="t-badge">T</span>':'—'}}</td>
  </tr>`).join('');
  const pg = document.getElementById('log-pager');
  pg.innerHTML = pages>1 ? [
    page>1?`<button class="pager-btn" onclick="renderLog(${{page-1}})">← Prev</button>`:'',
    `<span class="pager-info">Page ${{page}} of ${{pages}} · ${{items.length.toLocaleString()}} results</span>`,
    page<pages?`<button class="pager-btn" onclick="renderLog(${{page+1}})">Next →</button>`:''
  ].join('') : '';
}}

// ═══════════════════════════════════════════════════════
// FORMS
// ═══════════════════════════════════════════════════════
function buildFormCharts() {{
  const fms = FAC==='all'?FORMS:FORMS.filter(f=>f.fa===(FAC==='fw'?'Fort Wayne':'Waterloo'));
  const fw  = FORMS.filter(f=>f.fa==='Fort Wayne').length;
  const wl  = FORMS.filter(f=>f.fa==='Waterloo').length;
  const nw  = fms.filter(f=>f.nw).length;
  document.getElementById('fm-kpis').innerHTML =
    kpiHTML('Total Form Leads', fms.length,            'All time',               'kpi navy') +
    kpiHTML('Fort Wayne',       fw,                    '59.9% of all forms',     'kpi teal') +
    kpiHTML('Waterloo',         wl,                    '40.1% of all forms',     'kpi blue') +
    kpiHTML('New Contacts',     nw, `${{fms.length>0?(nw/fms.length*100).toFixed(1):0}}% new`, 'kpi green');

  // Daily form submissions — scrollable, all time
  const dateCounts = {{}};
  fms.forEach(f => {{ const d=f.dt.slice(0,10); dateCounts[d]=(dateCounts[d]||0)+1; }});
  const sortedDates = Object.keys(dateCounts).sort();
  document.getElementById('form-daily-wrap').innerHTML = scrollWrap('form-daily', 180, sortedDates.length);
  mkChart('form-daily', {{type:'bar', data:{{
    labels:sortedDates.map(d=>{{const[,m,day]=d.split('-');return`${{parseInt(m)}}/${{parseInt(day)}}`}}),
    datasets:[{{label:'Form Leads',data:sortedDates.map(d=>dateCounts[d]||0),backgroundColor:'rgba(10,61,92,.7)',borderRadius:5,borderSkipped:false}}]
  }}, options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:9}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true,stepSize:1}}}}}}
  }});
  mkChart('form-fac', {{type:'doughnut', data:{{labels:['Fort Wayne','Waterloo'],datasets:[{{data:[fw,wl],backgroundColor:['#0a3d5c','#3dffc0'],borderWidth:3,borderColor:'#fff'}}]}},
    options:{{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}}}}
  }});
}}

function renderForms() {{
  const q  = (document.getElementById('form-search')?.value||'').toLowerCase();
  const fm = (FAC==='all'?FORMS:FORMS.filter(f=>f.fa===(FAC==='fw'?'Fort Wayne':'Waterloo')))
    .filter(f => !q||((f.n+f.e+f.ph+f.hw+f.ci).toLowerCase().includes(q)));
  document.getElementById('fm-chip').textContent = fm.length+' RESULTS';
  document.getElementById('forms-tbody').innerHTML = fm.map(f => `<tr>
    <td style="font-family:'Space Mono',monospace;font-size:10px;color:#6b7e96;white-space:nowrap">${{f.dt}}</td>
    <td style="font-size:12px;font-weight:600;color:#0a3d5c">${{f.n}}</td>
    <td style="font-size:12px;color:#374151;max-width:260px;white-space:normal;line-height:1.4">${{f.hw||'<span style="color:#aaa;font-style:italic">—</span>'}}</td>
    <td style="font-family:'Space Mono',monospace;font-size:11px;color:#0a3d5c">${{f.ph}}</td>
    <td style="font-size:11px;color:#6b7e96">${{f.e}}</td>
    <td style="font-size:11px;color:#6b7e96">${{f.ci?f.ci+(f.st?', '+f.st:''):'—'}}</td>
    <td style="font-size:11px;color:#6b7e96">${{f.sr}}</td>
    <td><span class="${{f.fa==='Fort Wayne'?'fac-fw':'fac-wl'}}">${{f.fa}}</span></td>
    <td>${{f.nw?'<span class="new-pill">NEW</span>':'<span class="ret-pill">RETURN</span>'}}</td>
  </tr>`).join('');
}}

// ═══════════════════════════════════════════════════════
// MARKETING
// ═══════════════════════════════════════════════════════
function buildMarketing() {{
  const dates   = getPeriodDates();
  const buckets = aggregateDates(dates);
  const labels  = buckets.map(b=>b.label);
  const total   = dates.reduce((s,d)=>s+agg([d],'total'),0);
  const nw      = dates.reduce((s,d)=>s+agg([d],'new'),0);
  const yes     = dates.reduce((s,d)=>s+(DAILY[d]?.yes||0),0);
  const no      = dates.reduce((s,d)=>s+(DAILY[d]?.no||0),0);
  const disp    = FAC==='fw'?MKT.disp_by_fac['Fort Wayne']||{{}}:FAC==='wl'?MKT.disp_by_fac['Waterloo']||{{}}:MKT.disposition;
  const preA    = disp['conducted pre-assessment']||0;
  const dispTot = Object.values(disp).reduce((a,b)=>a+b,0);

  document.getElementById('mkt-kpis').innerHTML =
    kpiHTML('Total Calls',       total.toLocaleString(),                                              facLabel(),        'kpi navy') +
    kpiHTML('New Callers',       nw.toLocaleString(),                                                 'Unique new leads','kpi green') +
    kpiHTML('Lead Score: Yes',   yes,                                                                 'AI-scored leads', 'kpi teal') +
    kpiHTML('Lead Score: No',    no,                                                                  'Scored non-leads','kpi red') +
    kpiHTML('Pre-Assessments',   preA, `${{dispTot>0?(preA/dispTot*100).toFixed(1):0}}% of dispositioned`, 'kpi blue');

  // Trend chart — scrollable
  document.getElementById('mkt-trend-wrap').innerHTML = scrollWrap('mkt-trend', 200, buckets.length);
  mkChart('mkt-trend', {{type:'line', data:{{labels, datasets:[
    {{label:'Total',   data:buckets.map(b=>agg(b.dates,'total')),   borderColor:'#0a3d5c',backgroundColor:'rgba(10,61,92,.06)',  borderWidth:2.5,pointRadius:3,tension:.3,fill:true}},
    {{label:'Inbound', data:buckets.map(b=>agg(b.dates,'inbound')), borderColor:'#3b82f6',backgroundColor:'rgba(59,130,246,.04)',borderWidth:2,pointRadius:2,tension:.3,fill:false}},
    {{label:'New',     data:buckets.map(b=>agg(b.dates,'new')),     borderColor:'#10b981',backgroundColor:'rgba(16,185,129,.04)',borderWidth:2,pointRadius:2,tension:.3,fill:false}},
    {{label:'Missed',  data:buckets.map(b=>agg(b.dates,'missed')),  borderColor:'#ef4444',backgroundColor:'rgba(239,68,68,.04)', borderWidth:1.5,pointRadius:2,tension:.3,fill:false}}
  ]}}, options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}
  }}}});

  // Yes/No trend — scrollable
  document.getElementById('mkt-yesno-wrap').innerHTML = scrollWrap('mkt-yesno', 200, buckets.length);
  mkChart('mkt-yesno', {{type:'bar', data:{{labels, datasets:[
    {{label:'Yes (Lead)',data:buckets.map(b=>b.dates.reduce((s,d)=>s+(DAILY[d]?.yes||0),0)),backgroundColor:'rgba(16,185,129,.75)',borderRadius:4,borderSkipped:false}},
    {{label:'No',        data:buckets.map(b=>b.dates.reduce((s,d)=>s+(DAILY[d]?.no||0), 0)), backgroundColor:'rgba(239,68,68,.55)', borderRadius:4,borderSkipped:false}}
  ]}}, options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}},
    scales:{{x:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}
  }}}});

  // Disposition donut
  const dispE = Object.entries(disp).sort((a,b)=>b[1]-a[1]);
  const dColors = ['#0a3d5c','#3dffc0','#3b82f6','#f59e0b','#ef4444','#8b5cf6','#10b981'];
  mkChart('mkt-disp', {{type:'doughnut', data:{{labels:dispE.map(([k])=>k),datasets:[{{data:dispE.map(([,v])=>v),backgroundColor:dColors,borderWidth:2,borderColor:'#fff'}}]}},
    options:{{responsive:true,maintainAspectRatio:false,cutout:'55%',plugins:{{legend:{{position:'right',labels:{{font:{{size:11}},boxWidth:10,padding:8}}}},tooltip:{{callbacks:{{label:c=>` ${{c.label}}: ${{c.raw}}`}}}}}}}}
  }});

  // Daily score trend — scrollable
  document.getElementById('mkt-score-wrap').innerHTML = scrollWrap('mkt-score', 180, buckets.length);
  mkChart('mkt-score', {{type:'bar', data:{{labels, datasets:[
    {{label:'Yes',  data:buckets.map(b=>b.dates.reduce((s,d)=>s+(DAILY[d]?.yes||0),0)),  backgroundColor:'rgba(16,185,129,.75)',borderRadius:3,borderSkipped:false}},
    {{label:'No',   data:buckets.map(b=>b.dates.reduce((s,d)=>s+(DAILY[d]?.no||0), 0)),  backgroundColor:'rgba(239,68,68,.55)', borderRadius:3,borderSkipped:false}},
    {{label:'Lead', data:buckets.map(b=>b.dates.reduce((s,d)=>s+(DAILY[d]?.lead||0),0)), backgroundColor:'rgba(59,130,246,.6)', borderRadius:3,borderSkipped:false}}
  ]}}, options:{{responsive:true,maintainAspectRatio:false,
    plugins:{{legend:{{position:'bottom',labels:{{font:{{size:11}},boxWidth:10,padding:10}}}}}},
    scales:{{x:{{stacked:true,grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:8}},maxRotation:45}}}},y:{{stacked:true,grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}},beginAtZero:true}}}}
  }}}});

  // Landing pages
  const pgE = Object.entries(MKT.pages).sort((a,b)=>b[1]-a[1]).slice(0,10);
  mkChart('mkt-pages', {{type:'bar', data:{{labels:pgE.map(([k])=>k.length>38?k.slice(0,36)+'…':k),datasets:[{{label:'Calls',data:pgE.map(([,v])=>v),backgroundColor:'rgba(10,61,92,.7)',borderRadius:4,borderSkipped:false}}]}},
    options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}}}},y:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});

  // Referrers
  const rfE = Object.entries(MKT.refs).sort((a,b)=>b[1]-a[1]).slice(0,8);
  mkChart('mkt-refs', {{type:'bar', data:{{labels:rfE.map(([k])=>k),datasets:[{{label:'Calls',data:rfE.map(([,v])=>v),backgroundColor:rfE.map((_,i)=>i===0?'#0a3d5c':i===1?'#3b82f6':'rgba(61,255,192,.7)'),borderRadius:4,borderSkipped:false}}]}},
    options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(225,231,239,.6)'}},ticks:{{font:{{family:'Space Mono',size:9}}}}}},y:{{grid:{{display:false}},ticks:{{font:{{family:'Space Mono',size:9}}}}}}}}}}
  }});

  renderNotes();
}}

function renderNotes() {{
  const q  = (document.getElementById('notes-search')?.value||'').toLowerCase();
  const ns = MKT.notes.filter(n => {{
    const facOk = FAC==='all'||n.fa===(FAC==='fw'?'Fort Wayne':'Waterloo');
    return facOk && (!q||(n.n+n.ag).toLowerCase().includes(q));
  }});
  document.getElementById('notes-chip').textContent = ns.length+' NOTES';
  document.getElementById('notes-tbody').innerHTML = ns.map(n => `<tr>
    <td style="font-family:'Space Mono',monospace;font-size:10px;color:#6b7e96;white-space:nowrap">${{n.dt}}</td>
    <td style="font-size:11px;font-weight:600;color:#0a3d5c;white-space:nowrap">${{n.ag||'—'}}</td>
    <td><span class="${{n.fa==='Fort Wayne'?'fac-fw':'fac-wl'}}">${{n.fa==='Fort Wayne'?'FW':'WL'}}</span></td>
    <td style="font-size:12px;color:#374151;white-space:normal;line-height:1.5">${{n.n}}</td>
  </tr>`).join('');
}}

// ═══════════════════════════════════════════════════════
// REFRESH
// ═══════════════════════════════════════════════════════
function doRefresh() {{
  const btn = document.querySelector('.btn-refresh');
  const sp  = document.getElementById('spinEl');
  btn.disabled = true; sp.classList.add('go');
  setTimeout(() => {{
    document.getElementById('syncLbl').textContent = 'Synced: '+new Date().toLocaleTimeString([],{{hour:'2-digit',minute:'2-digit'}});
    btn.disabled = false; sp.classList.remove('go');
  }}, 1200);
}}

// ═══════════════════════════════════════════════════════
// BOOT
// ═══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {{
  document.getElementById('syncLbl').textContent = 'Synced: '+new Date().toLocaleTimeString([],{{hour:'2-digit',minute:'2-digit'}});
  buildCtrlBars();
  buildOverview();
  CHARTS['built_overview'] = true;
}});
</script>
</body>
</html>"""

    with open('strive_ctm_clean.html', 'w') as f:
        f.write(html)

    size = len(html)
    print(f"Built: strive_ctm_clean.html — {size//1024} KB")
    return html

if __name__ == '__main__':
    build()
