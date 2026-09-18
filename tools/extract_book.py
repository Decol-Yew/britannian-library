import sys, json, re, pathlib
n = int(sys.argv[1])
d = pathlib.Path(sys.argv[2])
hdr = (d / f"book{n:05d}.hdr").read_bytes()
# hdr layout: 4-byte flags, 60-byte title (NUL-terminated), 30-byte author (NUL-terminated)
def cstr(b):
    return re.sub(r"\s+", " ", b.split(b"\x00")[0].decode("latin-1")).strip()
title = cstr(hdr[4:64]); author = cstr(hdr[64:94])
txt = (d / f"book{n:05d}.txt").read_text(encoding="latin-1")
pages = []
for raw in txt.split("#EOP"):
    lines = raw.split("\n")
    paras = []
    for ln in lines:
        if not ln.strip():
            continue
        if ln.startswith("  ") or not paras:   # indented => new paragraph
            paras.append(ln.strip())
        else:
            paras[-1] += " " + ln.strip()
    pages.append(paras)
while pages and not pages[-1]:
    pages.pop()
print(json.dumps({"id": n, "title": title, "author": author, "pages": pages}, ensure_ascii=False, indent=1))
