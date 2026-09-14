# GitHub 棚卸し表 / 整理方針

調査日: 2026-09-12
対象アカウント: `Sasuraimitsu`（個人） / `sakanaya-japon`（Organization）

## この文書の位置づけ

「どのリポジトリが本物で、どれが役目を終えたか」を一覧にし、
SAKANAYA 系を Organization へ寄せるまでの手順をまとめたもの。

**採用した方針: 案A（Org 移管・独自ドメインは取得しない）**

---

## 1. 全リポジトリ一覧（15本）

`private` 以外はすべて公開 + GitHub Pages 有効。

| # | リポジトリ | 用途（推定含む） | 最終更新 | 判定 |
|---|---|---|---|---|
| 1 | `sakanaya-japon/sakanaya-productlist` | **法人向け商品カタログ（現行本番）** | 2026-09-11 | 維持（正） |
| 2 | `Sasuraimitsu/sakanaya-productlist` | 旧カタログURL → 移転案内ページ | 2026-09-03 | 案内期間終了後に Archive |
| 3 | `Sasuraimitsu/sakanayajapon` | 個人向けサイト（本リポジトリ） | 2026-06-15 | **Org へ移管** |
| 4 | `Sasuraimitsu/sakanayajapon-air` | カタログの旧試作版 | 2026-09-14 | 価格削除済 → **Archive待ち**（§2参照） |
| 5 | `Sasuraimitsu/sakanaya-punch` | 勤怠管理システム | 2026-06-30 | **Org へ移管 + 公開範囲要確認** |
| 6 | `Sasuraimitsu/metis-order-web` | METIS 受注サイト | 2026-07-12 | 維持（要 description） |
| 7 | `Sasuraimitsu/metis-photos` | METIS 商品写真の公開ミラー | 2026-08-01 | 維持 |
| 8 | `Sasuraimitsu/ISEC` | 伊勢志摩水産物輸出促進協議会 | 2026-09-11 | 維持 |
| 9 | `Sasuraimitsu/JCFS` | JCFS 本体サイト（漁船紹介・モデル詳細） | 2025-09-09 | 維持 |
| 10 | `Sasuraimitsu/JCFS-sub` | JCFS 投資家向けページ（ガバナンス・漁船モデル） | 2026-02-17 | 維持（改名検討） |
| 11 | `Sasuraimitsu/jcfs-all` | JCFS プロトコル 1ページ紹介サイト | 2026-03-17 | 維持（改名検討） |
| 12 | `Sasuraimitsu/smallearthtrading` | 輸送サービスのウェブページ | 2026-04-29 | 維持（不要ワークフロー要削除） |
| 13 | `Sasuraimitsu/cambodia-products` | ニャムガウスープ等の通販ページ | 2026-05-03 | 維持 |
| 14 | `Sasuraimitsu/acledasupport` | ACLEDA銀行 口座開設サポート案内（日英） | 2025-06-28 | 維持（不要ワークフロー要削除） |
| 15 | `Sasuraimitsu/privacy-policy` | 汎用プライバシーポリシー（LINE公式QR同梱） | 2025-03-29 | 維持 |
| 16 | `Sasuraimitsu/shadow` | 非公開 | 2026-09-12 | 対象外 |

**2026-09-13 更新**: 当初「要確認」としていたリポジトリはすべて中身を確認し、判定を確定しました（§5参照）。
`shadow`（非公開）のみ未確認です。

### いま効いている問題

1. **description が 15本中 9本で空**。リポジトリ一覧を見ても何のサイトか分からない。
2. **SAKANAYA 系が4本に分散**（`sakanayajapon` / `-air` / `-punch` / `-productlist`）。
   さらに `-productlist` は個人と Org の両方に存在する。
3. **JCFS 系が3本に分散**（`JCFS` / `JCFS-sub` / `jcfs-all`）。
   役割は実際には異なる（本体 / 投資家向け / 1ページ紹介）が、**名前からは判別できない**。
4. **全リポジトリが public + Pages 有効**。勤怠管理システムも公開されている
   （認証情報や従業員データは含まれていないことを確認済み。§5参照）。
5. `metis-order-web` だけデフォルトブランチが `master`（他は `main`）。

---

## 2. Step 1 の結論: `sakanayajapon-air` と `sakanaya-productlist` の関係

結論から言うと、**`sakanayajapon-air` は役目を終えた旧試作版**です。

| 項目 | `Sasuraimitsu/sakanayajapon-air` | `sakanaya-japon/sakanaya-productlist` |
|---|---|---|
| 最終更新 | 2026-03-15（半年停止） | 2026-09-11（現役） |
| 商品データ | ~~公開JSに32件ハードコード~~ → **2026-09-14 に価格を削除済み** | GAS から動的取得 |
| GAS 接続先 | `AKfycbxR97eDr6u...`（旧） | `AKfycbwgE8fOWPy...`（2026-07-06 新ブック移行済み） |
| 注文送信 | Telegram のテキスト本文に流し込むだけ | GAS `send_order` + Cloud Run Bot、冪等キー付き |
| 顧客登録 | なし | `register_user`（店名・担当者・電話） |
| 商品画像 | なし（`images/...` 参照だけで実体なし） | 167枚 / 23MB を同梱 |
| その他 | — | Excel 出力、在庫表示、サイズバリアント |

### ここから導かれる重要な帰結

**添付 `README_RESTRUCTURE.md` の Phase 1「`business/index.html`：法人向け入口 + 業務用商品一覧」は、作り直しになります。**

法人向け商品一覧は `sakanaya-japon.github.io/sakanaya-productlist/` として既に完成・稼働しており、
GAS の新ブック・Cloud Run Bot・顧客登録まで繋がっています。
これを `sakanayajapon` 側に作り直すと、**価格マスターの二重管理**が発生します。

→ 推奨する修正: `business/index.html` は「法人向けの入口（加工・配送・新規取引の説明）」に徹し、
　 商品一覧は現行カタログへ**リンクで送る**。カタログ本体は Org 側で育てる。

これにより README_RESTRUCTURE の懸念事項3（顧客別価格を公開JS/Pages に置かない）も自動的に解決します。
現行カタログは価格を GAS 経由で取得しており、公開JSに価格は入っていません。

### `sakanayajapon-air` の後始末

Archive するだけでは**公開状態は続き、価格は誰でも読めたまま**です。順番に注意してください。

1. ✅ **完了（2026-09-14）**: `script.js` の `SAMPLE_PRODUCTS` から価格32件を削除（すべて `price: null`）。
   既存の `hasPrice` 分岐により「価格はお問い合わせください」＋Telegram問い合わせボタン表示に切り替わる。
   併せて `index.html` のお知らせを新カタログへの導線に差し替え、README に後継を明記
2. ⬜ **未実施**: Archive（読み取り専用化）
   → `python3 docs/apply-repo-metadata.py --apply --archive` で実行できます

過去のコミット履歴にも価格は残るため、**完全に消したい場合はリポジトリ削除**が確実です。
（履歴の書き換えより、削除のほうが事故が少ない）

---

## 3. 案A の実施手順（Org 移管）

`sakanaya-productlist` で一度成功しているやり方の横展開です。

### 移管対象

- `Sasuraimitsu/sakanaya-punch` → `sakanaya-japon/sakanaya-punch`（**最優先**。出勤記録システムのため先行実施）
- `Sasuraimitsu/sakanayajapon` → `sakanaya-japon/sakanayajapon`

**2026-09-13 決定事項**

- `sakanaya-punch` を**他より先に**移管する。手順は `docs/punch-migration.md` に分離
- `sakanaya-punch` は **public のまま**運用する（GitHub Pages で打刻ページを配信しているため）
- `sakanaya-punch` は**今後も独立したリポジトリとして維持し、`sakanayajapon` には統合しない**

### 手順（1リポジトリあたり）

1. **GitHub の Transfer 機能を使う**
   `Settings` → 最下部 `Danger Zone` → `Transfer ownership` → 移管先に `sakanaya-japon`
   - Star / Issue / PR / コミット履歴はすべて保持される
   - 旧URL `github.com/Sasuraimitsu/...` は**自動リダイレクト**される
2. **Org 側で Pages を有効化**（`Settings` → `Pages` → Source: `main` / `/ (root)`）
3. **旧アカウント側に同名リポジトリを新規作成し、移転案内ページを置く**
   - ここが肝心です。**Pages の URL `sasuraimitsu.github.io/...` はリダイレクトされません**
     （リダイレクトされるのは `github.com/...` のリポジトリURLだけ）
   - `Sasuraimitsu/sakanaya-productlist` に置いた移転案内ページがまさにこの役割です。
     同じものを `noindex` 付きで流用してください
4. **リンク元の差し替え**（Facebook / LINE / Telegram のプロフィール、名刺、店頭QR）
5. 移転案内ページは**最低3か月**残す（顧客のブックマーク切替期間）

### 移管で変わる URL

| | 旧 | 新 |
|---|---|---|
| 個人向けサイト | `sasuraimitsu.github.io/sakanayajapon/` | `sakanaya-japon.github.io/sakanayajapon/` |
| 勤怠管理 | `sasuraimitsu.github.io/sakanaya-punch/` | `sakanaya-japon.github.io/sakanaya-punch/` |

`index.html` の OGP に旧URLが直書きされているので、移管と同時に差し替えが必要です。

```html
<!-- 移管後に修正が必要な箇所（index.html） -->
<meta property="og:image" content="https://sasuraimitsu.github.io/sakanayajapon/logo.jpg">
<meta property="og:url"   content="https://sasuraimitsu.github.io/sakanayajapon/">
```

### 移管前に決めておくこと

- **Org の Owner を2名以上にする**。1名だとアカウント喪失時に全サイトが復旧不能になります
- ~~`sakanaya-punch` の private 化~~ → **public のまま維持で確定**。
  中身を確認した結果、認証情報・従業員データの混入はなく、認証は短命トークン+PINでGAS側実装のため
  （詳細は `docs/punch-migration.md`）

### 独自ドメインについて（今回は見送り）

今回は取得しない判断ですが、将来 `sakanayajapon.com` 等を取得すると
GitHub アカウントを移しても**顧客に案内する URL は一切変わらなくなります**。
年 $10〜15 程度。次にアカウント構成を触るときの選択肢として残しておいてください。

---

## 4. 全リポジトリ共通の整備（移管と独立して進められる）

1. **description を全リポジトリに付ける**（1行でよい。一覧の視認性が段違いに上がる）
2. **topics を付ける**: `sakanaya` / `jcfs` / `metis` / `website` / `gas`
3. **役目を終えたものを Archive**（削除ではなく読み取り専用化。誤編集を防げる）
4. **README を最低3行にする**: ①何のサイトか ②公開URL ③関連リポジトリ
5. `metis-order-web` のデフォルトブランチを `master` → `main` に統一

---

## 5. description / topics の一括設定

### 実行方法

`docs/apply-repo-metadata.py` に全14リポジトリ分の description / topics を定義してあります。
**Claude の実行環境からは GitHub のリポジトリ設定への書き込みがプロキシで遮断される**ため
（`Repository settings writes are not permitted through this proxy`）、
手元の PC で実行してください。GitHub App の権限とは別の制限で、権限追加では解決しません。

```bash
# 1. トークンを用意（https://github.com/settings/tokens?type=beta）
#    Repository access: All repositories
#    Administration: Read and write / Metadata: Read and write
export GITHUB_TOKEN=github_pat_xxxxxxxx

# 2. 確認（何も変更しない）
python3 docs/apply-repo-metadata.py

# 3. 適用
python3 docs/apply-repo-metadata.py --apply
```

`--archive` を付けると Archive 対象（現時点では `sakanayajapon-air` のみ）も実行します。
**先に価格を含む `script.js` を削除してから**実行してください。Archive しても公開は続きます。

### 設定する内容

| リポジトリ | description | topics |
|---|---|---|
| `sakanayajapon` | SAKANAYA JAPON 個人向け公式サイト（カンボジア・プノンペンの魚屋／鮮魚・刺身の宅配） | sakanaya-japon, cambodia, seafood, website, github-pages |
| `sakanayajapon-air` | 【旧版】法人向け商品カタログの試作。後継は sakanaya-japon/sakanaya-productlist | sakanaya-japon, deprecated, product-catalog |
| `sakanaya-punch` | SAKANAYA JAPON 勤怠打刻システム（QRキオスク＋PIN認証／GASバックエンド） | sakanaya-japon, attendance, google-apps-script, qrcode, internal-tool |
| `sakanaya-productlist` | 【移転案内】商品カタログは sakanaya-japon/sakanaya-productlist へ移転しました | sakanaya-japon, redirect-notice |
| `JCFS` | JCFS カンボジア漁港開発プロジェクト 公式サイト（日本製FRP漁船の導入・インパクト投資） | jcfs, cambodia, fishery, impact-investing, website |
| `JCFS-sub` | JCFS プロジェクト 投資家向けページ（ガバナンス・セキュリティ・漁船モデル紹介） | jcfs, cambodia, fishery, investor-relations |
| `jcfs-all` | JCFS プロトコル 1ページ紹介サイト | jcfs, cambodia, fishery, landing-page |
| `metis-order-web` | METIS B2B受注サイト（system5 フロントエンド） | metis, b2b, order-system, website |
| `metis-photos` | （変更なし。既存の英語 description が適切） | metis, images, assets |
| `ISEC` | 伊勢志摩水産物輸出促進協議会 公式サイト（三重県志摩市） | iseshima, seafood, export, website |
| `smallearthtrading` | SMALL EARTH TRADING Co.,ltd 公式サイト（輸送サービス案内・手続きの流れ・FAQ） | logistics, cambodia, website |
| `cambodia-products` | カンボジア産品の通販サイト（ニャムガウスープ・塩漬けライム・乾燥ハーブ） | cambodia, ec, food, website |
| `acledasupport` | ACLEDA銀行 口座開設サポート案内（日本語／英語） | cambodia, banking, guide, website |
| `privacy-policy` | 各サービス共通のプライバシーポリシー掲載ページ | privacy-policy, legal |

`shadow`（非公開）は中身を確認していないため対象外です。

### 中身を確認して判明したこと

§1 の表で「要確認」としていた項目は、実際に中身を読んで確定させました。

- **JCFS 系3本は役割が違い、統合の必要はない**
  - `JCFS`: 本体サイト（漁船82ファイル・モデル詳細ページあり）
  - `JCFS-sub`: 投資家向けページ（ガバナンス／セキュリティ、漁船モデル一覧）
  - `jcfs-all`: 1ページ完結の紹介サイト（4ファイル）
  - ただし**名前から役割が読めない**ため、`jcfs-site` / `jcfs-ir` / `jcfs-landing` のような改名は検討価値があります
- **`cambodia-products` は現役**（ニャムガウスープの通販ページ）
- **`acledasupport` は ACLEDA銀行の口座開設サポート案内**（日英2言語）
- **`privacy-policy` は汎用のプライバシーポリシー**。LINE公式アカウントのQRを同梱

### 併せて対処したい点

1. **GitHub Skills のチュートリアル用ワークフローが残っている**
   `acledasupport` と `smallearthtrading` の `.github/workflows/` に
   `0-welcome.yml` 〜 `5-merge-your-pull-request.yml` が残存しています。
   GitHub Pages 入門コースのテンプレート由来で、**本来のサイト運用には不要**です。
   Issue を自動作成するなど予期しない動作をする可能性があるため、削除を推奨します。

2. **`sakanaya-punch` の公開について（確認結果）**
   中身を確認したところ、**ハードコードされた認証情報や従業員データは含まれていません**。
   短命トークン + PIN 認証で、実データは GAS 側にあります。
   そのため「公開されているから即危険」という状態ではありませんでした。
   ただし打刻ロジックと画面構成は誰でも読める状態なので、
   業務システムとして Org 移管時に private 化する判断は依然として妥当です。
