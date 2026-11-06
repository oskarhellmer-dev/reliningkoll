#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hämtar riktig bostadsdata per kommun från SCB:s öppna API och sparar
som data/scb_bostad.json  -> {kommunkod: {...}}"""
import json, urllib.request, os

URL = "https://api.scb.se/OV0104/v1/doris/sv/ssd/BO/BO0104/BO0104D/BO0104T02"

meta = json.load(urllib.request.urlopen(URL, timeout=30))
region_var = [v for v in meta["variables"] if v["code"] == "Region"][0]
codes = region_var["values"]
names = dict(zip(region_var["values"], region_var["valueTexts"]))

# kommunkoder = 4 siffror
kom = [c for c in codes if len(c) == 4]

body = {
  "query": [
    {"code": "Region", "selection": {"filter": "item", "values": kom}},
    {"code": "Hustyp", "selection": {"filter": "item", "values": ["SMÅHUS", "FLERBOST"]}},
    {"code": "Byggnadsperiod", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "ContentsCode", "selection": {"filter": "item", "values": ["BO0104AB"]}},
    {"code": "Tid", "selection": {"filter": "item", "values": ["2024"]}}
  ],
  "response": {"format": "json"}
}
req = urllib.request.Request(URL, data=json.dumps(body).encode(),
      headers={"Content-Type": "application/json"})
res = json.load(urllib.request.urlopen(req, timeout=90))

data = {}
for row in res["data"]:
    kod, hustyp, period, _tid = row["key"]
    val = int(row["values"][0]) if row["values"][0].isdigit() else 0
    d = data.setdefault(kod, {"namn": names.get(kod, "").replace(" kommun", ""),
                              "smahus": {}, "flerbost": {}})
    key = "smahus" if hustyp == "SMÅHUS" else "flerbost"
    d[key][period] = val

# härledda nyckeltal per kommun
PRE1950 = ["-1930", "1931-1940", "1941-1950"]
PRE1970 = ["-1930", "1931-1940", "1941-1950", "1951-1960", "1961-1970"]

out = {}
for kod, d in data.items():
    sm = d["smahus"]; fb = d["flerbost"]
    tot_sm = sum(sm.values()); tot_fb = sum(fb.values()); tot = tot_sm + tot_fb
    if tot == 0:
        continue
    pre1950_sm = sum(sm.get(p, 0) for p in PRE1950)
    pre1970_sm = sum(sm.get(p, 0) for p in PRE1970)
    pre1970_tot = pre1970_sm + sum(fb.get(p, 0) for p in PRE1970)
    out[kod] = {
      "namn": d["namn"],
      "smahus": tot_sm, "flerbost": tot_fb, "totalt": tot,
      "smahus_andel": round(100 * tot_sm / tot),
      "smahus_pre1950": pre1950_sm,
      "smahus_pre1970": pre1970_sm,
      "pre1970_andel": round(100 * pre1970_tot / tot),
      "aldsta_period": max(sm, key=sm.get) if sm else None,
    }

os.makedirs("/home/clawd/reliningkoll/data", exist_ok=True)
json.dump(out, open("/home/clawd/reliningkoll/data/scb_bostad.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("Kommuner med data:", len(out))
for k in ["0180", "1480", "1280", "2584"]:
    if k in out: print(" ", out[k])
