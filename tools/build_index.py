"""Build site/index.html (bookshelf) and site/books/*.html for every book that has a translation."""
import json, pathlib, subprocess, re, html
here = pathlib.Path(__file__).parent
site = here.parent; (site / "books").mkdir(parents=True, exist_ok=True)

def slug(t):
    return re.sub(r"[^a-z0-9]+", "_", t.lower()).strip("_")

books = []
for i in range(1, 27):
    en = json.loads((here.parent / "data" / "en" / f"book{i:05d}.json").read_text())
    jp = here.parent / "data" / "ja" / f"book{i:05d}.json"
    ja = json.loads(jp.read_text()) if jp.exists() else None
    fn = f"book{i:05d}_{slug(en['title'])}.html"
    if ja:
        subprocess.run(["python3", str(here / "build.py"), str(i), str(site / "books" / fn)], check=True)
    books.append({"id": i, "title": en["title"], "author": en["author"], "pages": len(en["pages"]),
                  "ja": ja["title"] if ja else None, "file": f"books/{fn}" if ja else None})

# leather colours for the spines/covers, cycled
COLORS = ["#5b3a20", "#3f2d4a", "#274a3b", "#5a2a2a", "#2f3f5c", "#4a3b1f", "#3b2f2f", "#26414b"]

cards = []
for b in books:
    col = COLORS[b["id"] % len(COLORS)]
    inner = f'''
      <div class="cover" style="--c:{col}">
        <div class="ct">{html.escape(b["title"])}</div>
        <div class="ca">{html.escape(b["author"])}</div>
        <div class="cp">{b["pages"]} pages</div>
      </div>
      <div class="meta">
        <div class="jt">{html.escape(b["ja"]) if b["ja"] else '<span class="todo">（未訳）</span>'}</div>
      </div>'''
    if b["file"]:
        cards.append(f'<a class="card" href="{b["file"]}">{inner}</a>')
    else:
        cards.append(f'<div class="card pending">{inner}</div>')

done = sum(1 for b in books if b["file"])
page = f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Books of Britannia — UO NPC本 対訳集</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IM+Fell+English:ital@0;1&family=Shippori+Mincho:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --gold:#c9a15a;--paper:#e6d6ad;--ink:#3b2612;--ink-soft:#6b4a2b;
  --serif-en:"IM Fell English","Palatino Linotype","Book Antiqua",Georgia,serif;
  --serif-ja:"Shippori Mincho","Yu Mincho","YuMincho","Hiragino Mincho ProN","Noto Serif JP","MS Mincho",serif;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;min-height:100%}}
body{{
  background:#151009;
  background-image:
    radial-gradient(ellipse at 50% 20%, rgba(120,80,40,.28), rgba(0,0,0,0) 60%),
    url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .09 0'/></filter><rect width='200' height='200' filter='url(%23n)'/></svg>");
  color:#d8c9a3;font-family:var(--serif-ja);padding:32px 16px 60px;
  display:flex;flex-direction:column;align-items:center;gap:22px;
}}
header{{text-align:center;max-width:70ch}}
header h1{{font-family:var(--serif-en);font-weight:normal;font-size:2rem;margin:0;letter-spacing:.06em;color:var(--gold)}}
header .sub{{font-size:1rem;opacity:.8;margin-top:6px}}
header .desc{{font-size:.85rem;opacity:.6;margin-top:12px;line-height:1.7}}
header .rule{{width:220px;height:1px;margin:14px auto 0;background:linear-gradient(90deg,transparent,var(--gold),transparent);opacity:.6}}

/* shelves */
.shelf{{
  width:min(100%,1080px);
  display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:22px 18px;
  padding:26px 26px 0;
  position:relative;
}}
.shelf::after{{ /* wooden shelf board */
  content:"";position:absolute;left:0;right:0;bottom:-18px;height:18px;border-radius:2px;
  background:linear-gradient(180deg,#6b4526,#3d2612 60%,#241508);
  box-shadow:0 10px 20px rgba(0,0,0,.6), inset 0 2px 0 rgba(255,220,160,.15);
}}
.shelf-wrap{{width:min(100%,1080px);display:flex;flex-direction:column;gap:40px;
  padding:10px 0 20px;}}
.card{{
  display:flex;flex-direction:column;align-items:center;gap:8px;text-decoration:none;color:inherit;
  transition:transform .18s;
}}
.card:hover{{transform:translateY(-6px)}}
.card.pending{{opacity:.42;filter:grayscale(.5)}}
.cover{{
  width:130px;height:180px;border-radius:3px 9px 9px 3px;position:relative;
  background:
    linear-gradient(90deg, rgba(0,0,0,.45) 0, rgba(0,0,0,.25) 6px, transparent 14px),
    radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.14), transparent 55%),
    var(--c);
  box-shadow:0 12px 24px rgba(0,0,0,.6), inset 0 0 0 2px rgba(0,0,0,.3), inset 0 0 0 4px rgba(201,161,90,.35);
  padding:22px 12px 12px 18px;display:flex;flex-direction:column;align-items:center;text-align:center;
}}
.cover::before{{ /* leather grain */
  content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;mix-blend-mode:multiply;
  background:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.6' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .18 0'/></filter><rect width='160' height='160' filter='url(%23n)'/></svg>");
}}
.cover::after{{ /* page block on the right edge */
  content:"";position:absolute;right:-3px;top:6px;bottom:6px;width:5px;border-radius:0 2px 2px 0;
  background:repeating-linear-gradient(180deg,#e9dcb8 0 1px,#c8b68a 1px 2px);
}}
.ct{{font-family:var(--serif-en);color:#f0dc9a;font-size:.95rem;line-height:1.25;text-shadow:0 1px 0 rgba(0,0,0,.6);flex:1;display:flex;align-items:center}}
.ca{{font-family:var(--serif-en);font-style:italic;font-size:.72rem;color:rgba(240,220,154,.8);margin-top:6px}}
.cp{{font-family:var(--serif-en);font-size:.62rem;color:rgba(240,220,154,.5);margin-top:4px;letter-spacing:.05em}}
.meta{{text-align:center;font-size:.85rem;line-height:1.4;min-height:1.4em}}
.jt{{color:#e8d7ab}}
.todo{{opacity:.7;font-size:.8rem}}
.legend{{font-size:.78rem;opacity:.6}}
footer{{font-size:.72rem;opacity:.5;text-align:center;max-width:70ch;line-height:1.7}}
@media (max-width:520px){{
  .shelf{{grid-template-columns:repeat(auto-fill,minmax(120px,1fr));padding:20px 14px 0;gap:18px 12px}}
  .cover{{width:110px;height:154px}}
  .ct{{font-size:.85rem}}
}}
</style>
</head>
<body>
<header>
  <h1>Books of Britannia</h1>
  <div class="sub">Ultima Online NPC本 対訳集 — 原文と日本語訳</div>
  <div class="rule"></div>
  <div class="desc">1998年当時の Ultima Online に置かれていた、NPCの書いた本の全文を、原文と日本語訳を見開きで並べて読めるようにしたものです。表紙をクリックすると本が開きます。</div>
</header>

<div class="shelf-wrap">
  <div class="shelf">
    {"".join(cards)}
  </div>
</div>
<div class="legend">翻訳済み {done} / {len(books)} 冊 — 薄く表示されている本は未訳です</div>

<footer>
  Original texts are from the Ultima Online (1998) in-game books, extracted from the UO Demo server data.
  日本語訳は非公式な私訳です。Ultima Online は Electronic Arts Inc. の商標です。
</footer>
</body>
</html>
'''
(site / "index.html").write_text(page)
print("index:", done, "/", len(books), "translated")
