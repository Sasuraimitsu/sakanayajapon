# SAKANAYA JAPON — 個人向けウェブサイト

カンボジア・プノンペンの魚屋 SAKANAYA JAPON の、個人のお客様向けサイトです。

- 公開URL: https://sasuraimitsu.github.io/sakanayajapon/
  （`sakanaya-japon` Organization への移管後は `https://sakanaya-japon.github.io/sakanayajapon/`）
- ホスティング: GitHub Pages（`main` ブランチ / ルート直下）
- 法人向け商品カタログは別リポジトリ: https://github.com/sakanaya-japon/sakanaya-productlist

---

## 1. ファイル構成

| ファイル | 役割 |
|---|---|
| `index.html` | トップ（リンク集型）。各ページと注文窓口への入口 |
| `menu.html` | メニュー画像1枚 + 注文ボタン |
| `howto.html` | LINE での注文方法（動画 `howtouse.mp4`） |
| `q&a.html` | よくあるご質問 |
| `aboutus.html` | 店舗情報・営業時間・アクセス |
| `logo.jpg` | ロゴ（favicon / OGP 兼用） |
| `fish-photo.jpg` | トップ背景スライドショー用 |
| `english-menu20260207.jpg` | `menu.html` に表示するメニュー画像 |
| `howtouse.mp4` | 注文方法の説明動画（約2.8MB） |
| `docs/` | 運用ドキュメント（サイトとしては公開されない） |

### 注意点

- `index.html` の背景スライドショーは `fish-photo.jpg` / `sashimi.jpg` / `event.jpg` を読もうとしますが、
  **現在リポジトリにあるのは `fish-photo.jpg` だけ**です。
  存在しない画像は自動でスキップされる作りなので表示は壊れませんが、実質1枚のみ表示されています。
  スライドショーにしたい場合は残り2枚を追加してください。
- `q&a.html` はファイル名に `&` を含むため、URL では `q%26a.html` になります。
  将来 `faq.html` へ改名する際は、旧URLからの案内を用意してください。

---

## 2. 更新のしかた（ブランチ運用ルール）

**ページの種類によって手順を変えます。** すべてに PR を要求すると緊急修正が回らず、
逆にすべて `main` 直編集にすると価格ミスがそのまま本番に出てしまうためです。

### A. `main` を直接編集してよいもの

- 文言の修正、誤字脱字
- 営業時間・お知らせの更新
- 画像の差し替え

GitHub のウェブ画面から直接編集してコミットして構いません。スマホからでも直せます。

### B. ブランチ + Pull Request が必須のもの

- **価格が表示される箇所**（法人向けページ、商品リスト）
- 注文フロー・注文先URLの変更
- `assets/` 配下の共通CSS / JS（全ページに影響するため）
- ページの新規追加・削除・改名

```bash
# 作業ブランチを切る
git checkout main
git pull origin main
git checkout -b feature/business-page

# 編集してコミット
git add .
git commit -m "法人向けページに加工サービスの説明を追加"
git push -u origin feature/business-page

# GitHub 上で Pull Request を作成 → 内容を確認 → merge
```

### 本番反映前のプレビュー

PR を作っても GitHub Pages にはプレビューが出ません。確認方法は2つです。

1. ローカルで確認（推奨）
   ```bash
   python3 -m http.server 8000
   # ブラウザで http://localhost:8000/ を開く
   ```
2. GitHub のファイル画面で `Preview` タブを使う（CSS は反映されないため簡易確認のみ）

---

## 3. 再編計画

詳細は `docs/` を参照してください。

| ドキュメント | 内容 |
|---|---|
| `docs/github-inventory.md` | 全リポジトリの棚卸し、Organization への移管手順 |
| `docs/contact-points.md` | 営業時間・注文窓口の食い違いと統一案 |
| `docs/punch-migration.md` | `sakanaya-punch` の Organization 移管手順（先行実施） |
| `docs/apply-repo-metadata.py` | 全リポジトリの description / topics を一括設定するスクリプト |

### Phase 1（未着手）

個人向け / 法人向けの2導線を持つトップページを追加します。

- `index.html`：個人 / 法人を選ぶ新トップ
- `retail/index.html`：個人向け入口（既存ページをそのまま利用）
- `business/index.html`：法人向け入口
- `assets/css/`, `assets/js/`：共通スタイル・日英切替

**当初計画からの変更点:** `business/index.html` に業務用商品一覧を新規実装する予定でしたが、
同等以上のものが `sakanaya-japon/sakanaya-productlist` として**既に本番稼働中**です
（GAS 連携・顧客登録・在庫表示・Excel出力・商品画像167枚）。
作り直すと価格マスターが二重管理になるため、**法人向けページからはカタログへリンクする方針に変更**します。
根拠は `docs/github-inventory.md` の §2 を参照してください。

既存ページは Phase 1 では削除しません。公開中ページの安全性を優先します。

### Phase 2

- 既存4ページの CSS / ナビゲーションを共通化
- `assets/js/site-info.js` による営業時間・窓口URLの単一情報源化（`docs/contact-points.md` §3）
- `q&a.html` → `faq.html` への改名（旧URLからの案内を用意）
- 画像を `assets/images/` へ整理
- 法人向け「加工」「配送」「新規取引」の詳細ページ追加

### 着手前に確定が必要な事項

`docs/contact-points.md` §4 の6項目（営業時間、定休日、Facebook / LINE の正URL など）。
ここが決まらないままページを作ると、食い違いを新しいページに複製することになります。
