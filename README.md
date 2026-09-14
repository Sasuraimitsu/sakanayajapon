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
| `index.html` | **新トップ**。個人 / 法人の2導線を選ぶページ |
| `retail/index.html` | 個人向け入口（旧トップのリンク集。既存4ページへ誘導） |
| `business/index.html` | 法人向け入口（商品カタログ・取引の流れ・問い合わせ） |
| `assets/css/` | `common.css`（共通）/ `home.css`（トップ）/ `business.css`（法人） |
| `assets/js/` | `site-info.js`（営業時間・窓口の情報源）/ `common.js`（日英切替） |
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

### Phase 1（✅ 完了 / 2026-09-14）

個人向け / 法人向けの2導線を持つトップページを追加しました。

| ファイル | 内容 |
|---|---|
| `index.html` | 個人 / 法人を選ぶ新トップ。旧トップのリンク集は `retail/` へ移動 |
| `retail/index.html` | 旧トップをそのまま移設（磨りガラス調のリンク集）。既存4ページへ誘導 |
| `business/index.html` | 法人向け入口。カタログ導線・加工/配送/解体ショー・注文の流れ・問い合わせ |
| `assets/css/common.css` | トークン、ヘッダー、フッター、ボタン、言語切替 |
| `assets/css/home.css` | 新トップ専用（ヒーロー、選択カード） |
| `assets/css/business.css` | 法人ページ専用（カタログCTA、サービス、取引の流れ） |
| `assets/js/site-info.js` | 営業時間・窓口URLの単一情報源 |
| `assets/js/common.js` | 日英切替、`site-info.js` の値の流し込み |

**当初計画からの変更点:** `business/index.html` に業務用商品一覧を新規実装する予定でしたが、
同等以上のものが `sakanaya-japon/sakanaya-productlist` として**既に本番稼働中**です
（GAS 連携・顧客登録・在庫表示・Excel出力・商品画像167枚）。
作り直すと価格マスターが二重管理になるため、**法人向けページからはカタログへリンクする方針に変更**しました。
根拠は `docs/github-inventory.md` の §2 を参照してください。

既存ページ（`menu.html` / `howto.html` / `q&a.html` / `aboutus.html`）は削除していません。
これらの「TOP」リンクは新トップ（選択ページ）に着地します。

#### 実装上の決めごと

- **日英切替**: `data-ja` / `data-en` 属性でテキストを差し替え、リンクを含むブロックは
  `data-lang="ja"` / `data-lang="en"` で出し分ける。選択は `localStorage` に保存（例外は握りつぶす）
- **JS が動かない場合**: HTML に日本語の既定値を書いてあるため、そのまま日本語で表示される。
  CSS も `display: block` で指定しており、`display: revert` 非対応ブラウザでも本文が消えない
- **窓口URLの直書き禁止**: 新規ページでは `data-info-href="order.xxx"` を使い、
  実体は `assets/js/site-info.js` にだけ書く

#### 動作確認済みの項目

- 新規3ページの HTML タグ構造
- 内部リンク45件がすべて実在（CSS の背景画像参照を含む）
- `data-info` 12件がすべて `SITE_INFO` に定義済み
- `common.js` / `site-info.js` の構文
- ローカル配信で全アセットが 200 を返すこと

### Phase 2

- 既存4ページの CSS / ナビゲーションを共通化（`assets/css/common.css` へ寄せる）
- 既存4ページにも `site-info.js` を適用し、営業時間・窓口URLの直書きをなくす
- `q&a.html` → `faq.html` への改名（旧URLからの案内を用意）
- 画像を `assets/images/` へ整理
- 法人向け「加工」「配送」「新規取引」の詳細ページ追加

### 着手前に確定が必要な事項

~~`docs/contact-points.md` §4 の6項目~~ → **2026-09-14 に全6項目が確定し、ページへの反映も完了しました。**

確定した内容（詳細は `docs/contact-points.md` §4）:

| 項目 | 確定値 |
|---|---|
| 営業時間 | 毎日 10:00〜19:30（国民の休日を除く）。定休日なし |
| Facebook | `facebook.com/fishstorejapan` に統一 |
| LINE ID | `@sakanayajapan` のまま（変更すると友だち追加リンクが切れるため） |
| LINE 公式アカウント | 個人のお客様向け問い合わせ窓口として残す |
| 法人向け Telegram | 旧グループは廃止。現行は `@sakanayaorder` |

Phase 1 に着手できる状態です。
