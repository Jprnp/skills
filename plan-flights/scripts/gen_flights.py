#!/usr/bin/env python
"""Render a flight-planning HTML report from a JSON spec of VERIFIED single-ticket fares.

Usage:  python gen_flights.py <spec.json> [out.html]

The JSON is produced by Claude after browser-verifying single-ticket fares on Kayak.
See example.json in the skill folder for the full schema. Scoring: three rankings
(balanced / value-first / duration-first) over price + total stops + longest single leg,
normalized within each section. Duration shown = longest single leg (the tiring number).
"""
import json, sys, os

VERSIONS = [
    ("Balanced", "price + stops + longest-leg, equal weight", (1/3, 1/3, 1/3)),
    ("Value-first", "price 60% &middot; longest-leg 25% &middot; stops 15%", (0.60, 0.15, 0.25)),
    ("Duration-first", "longest-leg 60% &middot; stops 25% &middot; price 15%", (0.15, 0.25, 0.60)),
]  # weights = (price, stops, duration)

def hm(m): return "{}h{:02d}".format(m // 60, m % 60)

def esc(s): return (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def book_base(spec):
    # default Kayak domain by currency; override with spec["book_domain"].
    dom = spec.get("book_domain")
    if not dom:
        dom = {"USD": "www.kayak.com", "BRL": "www.kayak.com.br", "EUR": "www.kayak.es",
               "GBP": "www.kayak.co.uk", "CAD": "www.kayak.ca", "AUD": "www.kayak.com.au"
               }.get(spec.get("currency_code", "").upper(), "www.kayak.com")
    return dom

def kayak(spec, sec, ret_date):
    origin = sec["origin"]; dest = sec.get("dest", spec["dest"]); outd = spec["out_date"]; dom = book_base(spec)
    if sec.get("linktype") == "openjaw":
        return "https://{}/flights/{}-{}/{}/{}-{}/{}?sort=bestflight_a".format(
            dom, origin, dest, outd, dest, sec["openjaw_dest"], ret_date)
    return "https://{}/flights/{}-{}/{}/{}?sort=bestflight_a".format(dom, origin, dest, outd, ret_date)

def nz(v, arr):
    lo, hi = min(arr), max(arr)
    return 0.0 if hi == lo else (v - lo) / (hi - lo)

def prep(combos):
    for c in combos:
        c["stops"] = c["o"]["st"] + c["r"]["st"]
        c["longest"] = max(c["o"]["mm"], c["r"]["mm"])
        c["rtmin"] = c["o"]["mm"] + c["r"]["mm"]
    return combos

def rank(combos, w):
    wp, ws, wd = w
    ps = [c["price"] for c in combos]; ss = [c["stops"] for c in combos]; ds = [c["longest"] for c in combos]
    out = []
    for c in combos:
        c = dict(c)
        c["score"] = round(wp*nz(c["price"],ps) + ws*nz(c["stops"],ss) + wd*nz(c["longest"],ds), 3)
        out.append(c)
    out.sort(key=lambda c: (c["score"], c["price"]))
    return out[:6]

def legcell(L):
    return ('<span class="air">' + esc(L["air"]) + '</span> &middot; ' + str(L["st"]) + ' stop(s)<br>'
            '<span class="meta">via ' + esc(L["route"]) + ' &middot; ' + esc(L["lab"]) + '</span>')

def rows(spec, sec, combos, cur):
    out = []
    for i, c in enumerate(combos, 1):
        bar = int((1 - c["score"]) * 100)
        medal = {1: "1st", 2: "2nd", 3: "3rd"}.get(i, str(i))
        lf = " warn" if c["longest"] >= 1300 else ""
        link = kayak(spec, sec, c["ret_date"])
        out.append(
            '<tr>'
            '<td class="rank">' + medal + '</td>'
            '<td><b>' + esc(spec["out_label"]) + '</b> ' + esc(c["o"]["t"]) + '<br>' + legcell(c["o"]) + '</td>'
            '<td><b>' + esc(c["ret_label"]) + '</b> ' + esc(c["r"]["t"]) + '<br>' + legcell(c["r"]) + '</td>'
            '<td class="price">' + cur + str("{:,}".format(c["price"])) + '</td>'
            '<td class="ctr">' + str(c["stops"]) + '</td>'
            '<td class="ctr' + lf + '"><b>' + hm(c["longest"]) + '</b><br><span class="meta">RT ' + hm(c["rtmin"]) + '</span></td>'
            '<td><div class="barwrap"><div class="bar" style="width:' + str(bar) + '%"></div></div><span class="sc">' + str(c["score"]) + '</span></td>'
            '<td><a class="btn" href="' + link + '" target="_blank">Kayak &#8599;</a></td>'
            '</tr>')
    return "".join(out)

def section_html(spec, sec, cur):
    combos = prep([dict(c) for c in sec["combos"]])
    origin = sec["origin"]; retc = sec.get("retcity", origin); d = sec.get("dest", spec["dest"])
    blocks = ""
    for vname, vdesc, w in VERSIONS:
        blocks += ('<h3 class="vh">' + vname + ' <span class="vd">&mdash; ' + vdesc + '</span></h3>'
            '<table><tr><th>#</th><th>Outbound (' + origin + '&rarr;' + d + ')</th>'
            '<th>Return (' + d + '&rarr;' + retc + ')</th><th>Price (RT)</th><th>Stops</th>'
            '<th>Longest leg / RT</th><th>Score</th><th>Book</th></tr>'
            + rows(spec, sec, rank(combos, w), cur) + '</table>')
    return ('<section><h2 class="' + sec.get("css", "") + '">' + esc(sec["name"]) + '</h2>'
            '<p class="note">' + sec.get("note", "") + '</p>' + blocks + '</section>')

def verdict_html(v, cur):
    if not v: return ""
    head = "<tr>" + "".join("<th>" + h + "</th>" for h in v["columns"]) + "</tr>"
    body = ""
    for r in v["rows"]:
        body += "<tr>" + "".join("<td>" + cell + "</td>" for cell in r) + "</tr>"
    return ('<section><h2 class="oj">&#9878;&#65039; ' + esc(v["heading"]) + '</h2>'
            '<p class="note">' + v.get("note", "") + '</p>'
            '<table>' + head + body + '</table>'
            '<div class="box ok" style="margin-top:14px">' + v["conclusion_html"] + '</div></section>')

CSS = """
:root{--bg:#0f1115;--card:#181b22;--line:#272b34;--txt:#e6e8ec;--mut:#9aa3b2;--acc:#4f9cff;--good:#2ec27e;--gold:#f5c451;--warn:#f5874f;}
*{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--txt);font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif;padding:32px}
h1{font-size:26px;margin:0 0 4px} .sub{color:var(--mut);margin:0 0 18px}
.box{border-radius:10px;padding:12px 16px;margin-bottom:14px;font-size:13px}
.legend{background:var(--card);border:1px solid var(--line);color:var(--mut)} .legend b{color:var(--txt)}
.ok{background:#13261c;border:1px solid #2ec27e55;color:#bfeccd} .ok b{color:var(--good)}
.constraint{background:#2a1d14;border:1px solid var(--warn);color:#ffd9c2} .constraint b{color:var(--warn)}
section{margin-bottom:42px} h2{font-size:20px;border-left:4px solid var(--acc);padding-left:10px;margin:0 0 6px}
h2.bsb{border-color:var(--good)} h2.oj{border-color:var(--gold)}
h3.vh{font-size:14px;color:var(--txt);text-transform:uppercase;letter-spacing:.04em;margin:22px 0 8px}
.vd{text-transform:none;color:var(--mut);font-weight:400;letter-spacing:0;font-size:12px}
.note{color:var(--mut);font-size:13px;margin:0 0 6px}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden;border:1px solid var(--line);margin-bottom:8px}
th,td{padding:10px 12px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#1f2430;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.04em}
tr:last-child td{border-bottom:none}
.rank{font-size:14px;font-weight:700;text-align:center;width:42px;color:var(--gold)}
.price{font-weight:700;color:var(--good);white-space:nowrap;font-size:16px}
.ctr{text-align:center} .ctr.warn b{color:var(--warn)}
.air{color:var(--acc);font-size:13px;font-weight:600} .meta{color:var(--mut);font-size:12px}
.barwrap{background:#0d0f13;border-radius:5px;height:8px;width:74px;overflow:hidden;display:inline-block;vertical-align:middle}
.bar{height:100%;background:linear-gradient(90deg,var(--good),var(--gold))} .sc{color:var(--mut);font-size:11px;margin-left:6px}
.btn{background:var(--acc);color:#fff;text-decoration:none;padding:6px 11px;border-radius:7px;font-size:12px;white-space:nowrap}
.how{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 22px} .how h3{margin:0 0 10px} .how ol{margin:0;padding-left:20px} .how li{margin-bottom:7px}
code{background:#0d0f13;padding:2px 6px;border-radius:5px;color:#9fd0ff;font-size:13px} a{color:var(--acc)}
"""

def build(spec):
    cur = spec.get("currency", "R$")
    boxes = "".join('<div class="box ' + b.get("kind", "legend") + '">' + b["html"] + '</div>' for b in spec.get("boxes", []))
    verdict = verdict_html(spec.get("verdict"), cur)
    secs = "".join(section_html(spec, s, cur) for s in spec["sections"])
    how = "".join("<li>" + s + "</li>" for s in spec.get("how_steps", []))
    how_block = ('<div class="how"><h3>How to open / book these</h3><ol>' + how + '</ol></div>') if how else ""
    return ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
        "<title>" + esc(spec["title"]) + "</title><style>" + CSS + "</style></head><body>"
        "<h1>" + esc(spec["title"]) + "</h1>"
        "<p class=\"sub\">" + spec.get("subtitle", "") + "</p>"
        + boxes + verdict + secs + how_block +
        "</body></html>")

def main():
    if len(sys.argv) < 2:
        print("usage: python gen_flights.py <spec.json> [out.html]"); sys.exit(1)
    spec_path = sys.argv[1]
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(spec_path)[0] + ".html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(build(spec))
    print("wrote", out)

if __name__ == "__main__":
    main()
