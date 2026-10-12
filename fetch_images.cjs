// Скачивает кандидатов фото с Wikimedia Commons (только JPEG >= 1200px)
const fs = require("fs");
const path = require("path");
const OUT = path.join(__dirname, "candidates");
const UA = { "User-Agent": "KaliningradDemoPicker/1.0 (portfolio demo; sasha_hmeleva@bk.ru)" };

const QUERIES = {
  hero: ["Königsberg Cathedral evening filemime:image/jpeg", "Кафедральный собор Калининград filemime:image/jpeg"],
  ryb:  ["Рыбная деревня Калининград filemime:image/jpeg", "Fish Village Kaliningrad filemime:image/jpeg"],
  zel:  ["Zelenogradsk filemime:image/jpeg", "Зеленоградск пляж filemime:image/jpeg"],
  svet: ["Svetlogorsk water tower filemime:image/jpeg", "Светлогорск filemime:image/jpeg"],
  kosa: ["Curonian Spit dune filemime:image/jpeg", "Танцующий лес filemime:image/jpeg"],
  balt: ["Baltiysk lighthouse filemime:image/jpeg", "Балтийск маяк filemime:image/jpeg"],
};

async function api(params) {
  const url = "https://commons.wikimedia.org/w/api.php?" + new URLSearchParams(params);
  const r = await fetch(url, { headers: UA });
  return r.json();
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const manifest = {};
  for (const [slug, queries] of Object.entries(QUERIES)) {
    const dir = path.join(OUT, slug);
    fs.mkdirSync(dir, { recursive: true });
    const got = [];
    for (const q of queries) {
      if (got.length >= 4) break;
      let data;
      try {
        data = await api({ action: "query", format: "json", generator: "search",
          gsrsearch: q, gsrnamespace: "6", gsrlimit: "10",
          prop: "imageinfo", iiprop: "url|size|mime", iiurlwidth: "1600" });
      } catch (e) { console.log(slug, "search fail", e.message); continue; }
      const pages = Object.values((data.query || {}).pages || {})
        .sort((a, b) => (a.index || 99) - (b.index || 99));
      for (const p of pages) {
        if (got.length >= 4) break;
        const ii = (p.imageinfo || [])[0] || {};
        const u = ii.thumburl || ii.url;
        if (!u || ii.mime !== "image/jpeg" || (ii.width || 0) < 1200) continue;
        const name = `${slug}_${got.length + 1}.jpg`;
        try {
          const r = await fetch(u, { headers: UA });
          if (!r.ok) continue;
          const buf = Buffer.from(await r.arrayBuffer());
          if (buf.length < 80_000) continue;
          fs.writeFileSync(path.join(dir, name), buf);
          got.push({ name, title: p.title, kb: Math.round(buf.length / 1024) });
          console.log(slug, name, "<-", p.title);
        } catch (e) { console.log(slug, "dl fail", e.message); }
      }
    }
    manifest[slug] = got;
  }
  fs.writeFileSync(path.join(OUT, "manifest.json"), JSON.stringify(manifest, null, 1));
  console.log("done");
})();
