import json, sys, pathlib
n = int(sys.argv[1]); out = sys.argv[2]
here = pathlib.Path(__file__).parent
en = json.loads((here.parent / "data" / "en" / f"book{n:05d}.json").read_text())
ja = json.loads((here.parent / "data" / "ja" / f"book{n:05d}.json").read_text())
assert len(en["pages"]) == len(ja["pages"]), (len(en["pages"]), len(ja["pages"]))
data = {"id": n, "title": en["title"], "author": en["author"], "jaTitle": ja["title"],
        "jaAuthor": ja["author"], "pages": en["pages"], "ja": ja["pages"]}
html = (here / "template.html").read_text()
html = (html.replace("__BOOKDATA__", json.dumps(data, ensure_ascii=False))
            .replace("__TITLE__", en["title"]).replace("__AUTHOR__", en["author"])
            .replace("__JATITLE__", ja["title"]).replace("__JAAUTHOR__", ja["author"])
            .replace("__ID__", f"{n:05d}"))
pathlib.Path(out).write_text(html)
print("wrote", out, len(en["pages"]), "pages")
