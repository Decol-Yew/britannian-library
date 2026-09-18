# Books of Britannia — UO NPC本 対訳集

Ultima Online（1998年当時）のゲーム内 NPC 本を、原文と日本語訳を見開きで並べて読めるようにした静的サイト。
GitHub Pages で公開（`index.html` と `books/` がサイト本体）。

## 構成

- `index.html` … 書架（目次）ページ。翻訳済みの本だけリンクになる
- `books/bookNNNNN_*.html` … 各本の対訳ページ（1ファイル完結）
- `data/en/bookNNNNN.json` … 原文（UO Demo の `books/bookNNNNN.hdr/.txt` から抽出）
- `data/ja/bookNNNNN.json` … 日本語訳（`title`, `author`, `pages`＝原文と同じページ数・同じ段落構成）
- `tools/` … 生成スクリプト
  - `extract_book.py N <rundir/books>` … 原文抽出 → JSON
  - `build.py N out.html` … 1冊分の対訳 HTML を生成
  - `build_index.py` … 全冊を再生成し `index.html` を作る
  - `template.html` … 本のページのテンプレート

## 本を1冊追加する手順

1. `data/ja/bookNNNNN.json` を書く（`data/en/bookNNNNN.json` とページ数を揃える）
2. `python3 tools/build_index.py` を実行（`tools/` の相対パス前提なので、スクリプト側のパス設定を参照）
3. 生成された `index.html` と `books/` をコミット

原文は Ultima Online のゲーム内テキスト（Electronic Arts / Origin Systems）。日本語訳は非公式な私訳です。
