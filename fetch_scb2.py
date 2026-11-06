#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hämtar befolkning + hushåll per kommun från SCB och lägger till detaljerad
byggnadsperiod-fördelning. -> data/scb_extra.json"""
import json, urllib.request, os

def get(url, body=None):
    if body is None:
        return json.load(urllib.request.urlopen(url, timeout=40))
    req = urllib.request.Request(url, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=90))

out = {}

# --- befolkning
BEF = "https://api.scb.se/OV0104/v1/doris/sv/ssd/BE/BE0101/BE0101A/BefolkningNy"
m = get(BEF)
reg = [v for v in m["variables"] if v["code"] == "Region"][0]
names = dict(zip(reg["values"], reg["valueTexts"]))
kom = [c for c in reg["values"] if len(c) == 4]
years = [v for v in m["variables"] if v["code"] == "Tid"][0]["values"]
y = years[-1]
r = get(BEF, {"query": [
    {"code": "Region", "selection": {"filter": "item", "values": kom}},
    {"code": "Civilstand", "selection": {"filter": "item", "values": ["OG"]}},
    {"code": "Alder", "selection": {"filter": "item", "values": ["tot"]}},
    {"code": "Kon", "selection": {"filter": "item", "values": ["1", "2"]}},
    {"code": "ContentsCode", "selection": {"filter": "item", "values": ["BE0101N1"]}},
    {"code": "Tid", "selection": {"filter": "item", "values": [y]}}],
    "response": {"format": "json"}})
pop = {}
for row in r["data"]:
    kod = row["key"][0]
    v = row["values"][0]
    if v.isdigit():
        pop[kod] = pop.get(kod, 0) + int(v)
for k, v in pop.items():
    out.setdefault(k, {})["befolkning"] = v
    out[k]["kommun"] = names.get(k, "").replace(" kommun", "")

# --- detaljerad byggnadsperiod
T02 = "https://api.scb.se/OV0104/v1/doris/sv/ssd/BO/BO0104/BO0104D/BO0104T02"
r = get(T02, {"query": [
    {"code": "Region", "selection": {"filter": "item", "values": kom}},
    {"code": "Hustyp", "selection": {"filter": "item", "values": ["SMÅHUS", "FLERBOST"]}},
    {"code": "Byggnadsperiod", "selection": {"filter": "all", "values": ["*"]}},
    {"code": "ContentsCode", "selection": {"filter": "item", "values": ["BO0104AB"]}},
    {"code": "Tid", "selection": {"filter": "item", "values": ["2024"]}}],
    "response": {"format": "json"}})
for row in r["data"]:
    kod, hustyp, period, _ = row["key"]
    v = int(row["values"][0]) if row["values"][0].isdigit() else 0
    d = out.setdefault(kod, {})
    d.setdefault("period", {}).setdefault(hustyp, {})[period] = v

os.makedirs("/home/clawd/reliningkoll/data", exist_ok=True)
json.dump(out, open("/home/clawd/reliningkoll/data/scb_extra.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("Kommuner:", len(out))
print("Exempel:", json.dumps(out.get("1480", {}), ensure_ascii=False)[:300])
