import json, os, urllib.parse, urllib.request

OUT = r"C:\Users\Алекс\.zcode\workspace\default\kaliningrad-demo\candidates"
UA = {"User-Agent": "KaliningradDemoAssetPicker/1.0 (portfolio demo; contact: sasha_hmeleva@bk.ru)"}

QUERIES = {
    "hero":    ["Königsberg Cathedral sunset", "Кафедральный собор Калининград вечер", "Kneiphof cathedral night"],
    "ryb":     ["Рыбная деревня Калининград", "Fish Village Kaliningrad"],
    "zel":     ["Зеленоградск променад", "Zelenogradsk pier", "Zelenogradsk beach"],
    "svet":    ["Светлогорск водонапорная башня", "Svetlogorsk water tower"],
    "kosa":    ["Куршская коса дюны", "Curonian Spit dune Efa", "Танцующий лес"],
    "balt":    ["Балтийск маяк", "Baltiysk lighthouse"],
}

def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=30))

os.makedirs(OUT, exist_ok=True)
manifest = {}
for slug, queries in QUERIES.items():
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    got, seen = [], set()
    for q in queries:
        if len(got) >= 4: break
        try:
            data = api({"action":"query","format":"json","generator":"search",
                        "gsrsearch": q, "gsrnamespace": "6", "gsrlimit": "8",
                        "prop":"imageinfo","iiprop":"url|size|mime","iiurlwidth":"1600"})
        except Exception as e:
            print(slug, "search fail", q, e); continue
        pages = (data.get("query") or {}).get("pages") or {}
        for p in sorted(pages.values(), key=lambda x: x.get("index", 99)):
            if len(got) >= 4: break
            ii = (p.get("imageinfo") or [{}])[0]
            u = ii.get("thumburl") or ii.get("url")
            if not u or u in seen: continue
            if not ii.get("mime","").startswith("image/"): continue
            w, h = ii.get("width",0), ii.get("height",0)
            if ii.get("mime") != "image/jpeg": continue
            if w < 900: continue
            seen.add(u)
            name = f"{slug}_{len(got)+1}.jpg"
            try:
                req = urllib.request.Request(u, headers=UA)
                data2 = urllib.request.urlopen(req, timeout=60).read()
                open(os.path.join(d, name), "wb").write(data2)
                got.append({"name": name, "title": p.get("title",""), "kb": len(data2)//1024})
            except Exception as e:
                print(slug, "dl fail", e)
    manifest[slug] = got
    print(slug, "->", [g["name"] + " " + g["title"][:60] for g in got])

json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("done")
