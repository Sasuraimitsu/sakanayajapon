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
| 4 | `Sasuraimitsu/sakanayajapon-air` | カタログの旧試作版 | 2026-03-15 | **Archive**（§2参照） |
| 5 | `Sasuraimitsu/sakanaya-punch` | 勤怠管理システム | 2026-06-30 | **Org へ移管 + 公開範囲要確認** |
| 6 | `Sasuraimitsu/metis-order-web` | METIS 受注サイト | 2026-07-12 | 維持（要 description） |
| 7 | `Sasuraimitsu/metis-photos` | METIS 商品写真の公開ミラー | 2026-08-01 | 維持 |
| 8 | `Sasuraimitsu/ISEC` | 伊勢志摩水産物輸出促進協議会 | 2026-09-11 | 維持 |
| 9 | `Sasuraimitsu/JCFS` | カンボジア漁港開発プロジェクト | 2025-09-09 | 要確認（§3） |
| 10 | `Sasuraimitsu/JCFS-sub` | JCFS 関連 | 2026-02-17 | 要確認（§3） |
| 11 | `Sasuraimitsu/jcfs-all` | JCFS 関連 | 2026-03-17 | 要確認（§3） |
| 12 | `Sasuraimitsu/smallearthtrading` | 輸送サービスのウェブページ | 2026-04-29 | 維持 |
| 13 | `Sasuraimitsu/cambodia-products` | カンボジア産品紹介？ | 2026-05-03 | 要確認 |
| 14 | `Sasuraimitsu/acledasupport` | ACLEDA 関連サポート？ | 2025-06-28 | 要確認（1年以上停止） |
| 15 | `Sasuraimitsu/privacy-policy` | プライバシーポリシー掲載用 | 2025-03-29 | 維持（アプリ審査用途なら必須） |
| 16 | `Sasuraimitsu/shadow` | 非公開 | 2026-09-12 | 対象外 |

判定が「要確認」のものは、中身を見ていないため名前と更新日からの推定です。
現役かどうかだけ教えていただければ、Archive / description 追記まで一括で進めます。

### いま効いている問題

1. **description が 15本中 9本で空**。リポジトリ一覧を見ても何のサイトか分からない。
2. **SAKANAYA 系が4本に分散**（`sakanayajapon` / `-air` / `-punch` / `-productlist`）。
   さらに `-productlist` は個人と Org の両方に存在する。
3. **JCFS 系が3本に分散**（`JCFS` / `JCFS-sub` / `jcfs-all`）。どれが本物か名前から判別不能。
4. **全リポジトリが public + Pages 有効**。勤怠管理システムまで公開されている。
5. `metis-order-web` だけデフォルトブランチが `master`（他は `main`）。

---

## 2. Step 1 の結論: `sakanayajapon-air` と `sakanaya-productlist` の関係

結論から言うと、**`sakanayajapon-air` は役目を終えた旧試作版**です。

| 項目 | `Sasuraimitsu/sakanayajapon-air` | `sakanaya-japon/sakanaya-productlist` |
|---|---|---|
| 最終更新 | 2026-03-15（半年停止） | 2026-09-11（現役） |
| 商品データ | **公開JSに40件ハードコード**（`$62.93` 等の実価格入り） | GAS から動的取得 |
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

Archive するだけでは**公開状態は続き、40件の価格は誰でも読めたまま**です。順番に注意してください。

1. 価格を含む `script.js` の `SAMPLE_PRODUCTS` を削除（または private 化）
2. そのうえで Archive（読み取り専用化）
3. README に「後継: sakanaya-japon/sakanaya-productlist」と1行記載

過去のコミット履歴にも価格は残るため、**完全に消したい場合はリポジトリ削除**が確実です。
（履歴の書き換えより、削除のほうが事故が少ない）

---

## 3. 案A の実施手順（Org 移管）

`sakanaya-productlist` で一度成功しているやり方の横展開です。

### 移管対象

- `Sasuraimitsu/sakanayajapon` → `sakanaya-japon/sakanayajapon`
- `Sasuraimitsu/sakanaya-punch` → `sakanaya-japon/sakanaya-punch`

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
- `sakanaya-punch`（勤怠管理）は移管と同時に **private 化**を検討。
  従業員名・打刻データがクライアント側に出ているなら公開は避けるべきです（要中身確認）

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
