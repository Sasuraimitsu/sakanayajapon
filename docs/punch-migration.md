# sakanaya-punch の Organization 移管手順

作成日: 2026-09-13
対象: `Sasuraimitsu/sakanaya-punch` → `sakanaya-japon/sakanaya-punch`

## 方針（確定事項）

- **出勤記録システムのため、他より先に移管する**
- **公開範囲は public のまま**（GitHub Pages で打刻ページを配信し続けるため）
- **今後も独立したリポジトリとして維持する。`sakanayajapon`（サイト）には統合しない**

移管作業自体は GitHub の画面操作が必要です（API 経由の実行は環境側で遮断されており、
また取り消しの効きにくい操作のため、手順書という形にしています）。

---

## 事前に押さえておくべき技術的な前提

移管前にコードを確認した結果、**壊れる箇所は1か所だけ**です。

### ✅ 自動で追従するもの（対応不要）

`display.html` が生成する打刻QRは、自分自身のURLを基準に組み立てています。

```javascript
// display.html L66
function punchBase() { return new URL('.', location.href).href; }
// → renderQR() で punchBase() + '?dc=' + code を QR に符号化
```

固定URLを持っていないため、**移管後は自動的に新URLを指すQRが生成されます**。
店頭に貼り出しているQRは30秒ごとに更新される動的QRなので、刷り直しも不要です。

### ✅ 移管の影響を受けないもの

`app.js` の `CONFIG.API_URL`（GAS WebApp の `/exec` URL）は GitHub とは無関係です。そのまま動きます。

### ⚠️ 唯一の要対応箇所: キオスク表示URL

`display.html` は、スプレッドシートのメニューから発行される
**`.../display.html?k=<kiosk鍵>` というURL**で開く設計です（L77 のヒント文言より）。

> Open the kiosk URL from the spreadsheet menu:
> **Payroll Admin → Setup → Show kiosk QR display URL**

この URL は **GAS 側（スプレッドシート）に保存されており、旧アドレスのまま**のはずです。
移管すると `sasuraimitsu.github.io/sakanaya-punch/` は配信されなくなる
（GitHub Pages はリダイレクトされません）ため、**ここを更新しないと打刻端末が動かなくなります**。

---

## 作業手順

### 0. 作業タイミングを選ぶ

営業時間は毎日 10:00〜19:30 です。**開店前か閉店後**に実施してください。
作業中は数分間、打刻ページが開けない時間が発生します。

### 1. 現在のキオスクURLを控える

スプレッドシートの **Payroll Admin → Setup → Show kiosk QR display URL** を開き、
表示される URL（`?k=` の鍵を含む完全な形）をメモしてください。
**この `k=` の値は移管後もそのまま使います。**

### 2. リポジトリを移管する

1. https://github.com/Sasuraimitsu/sakanaya-punch/settings を開く
2. 最下部 **Danger Zone** → **Transfer ownership**
3. New owner に `sakanaya-japon` を入力
4. 確認のためリポジトリ名を入力して実行

コミット履歴・Issue・Star はすべて引き継がれます。

### 3. Org 側で GitHub Pages を有効化する

**移管で Pages 設定が外れることがあります。必ず確認してください。**

1. https://github.com/sakanaya-japon/sakanaya-punch/settings/pages
2. Source: `Deploy from a branch`
3. Branch: `main` / `/ (root)` → Save
4. 反映まで1〜2分待つ

### 4. 新URLで動作確認する

```
https://sakanaya-japon.github.io/sakanaya-punch/
```

打刻ページ（Welcome画面）が表示されれば成功です。

### 5. キオスク表示URLを新アドレスに更新する

手順1で控えた URL のドメイン部分だけを差し替えて、GAS 側の設定を更新します。

```
旧: https://sasuraimitsu.github.io/sakanaya-punch/display.html?k=<鍵>
新: https://sakanaya-japon.github.io/sakanaya-punch/display.html?k=<鍵>
```

**`k=` の値は変更しないでください。** 変えるとキオスク認証が通りません。

更新場所が Apps Script のスクリプトプロパティか、シート上のセルかは
GAS 側の実装（`10_punch_api.gs` 周辺）を見て判断してください。
分からなければ、そのファイルを共有いただければこちらで特定します。

### 6. 店頭端末を更新する

- キオスク端末（タブレット等）のブックマーク / ホーム画面ショートカットを新URLに差し替え
- スタッフが個人スマホにブックマークしている場合は、そちらも案内

### 7. 実際に1回打刻して確認する

QRが表示されること、スキャンして PIN を入力し打刻が記録されることを、**実データで1回確認**してください。
画面が出るだけでは GAS 連携の確認になりません。

### 8. 旧URLに案内ページを置く（推奨）

古いブックマークを開いたスタッフが打刻できないと困るため、
個人アカウント側に同名の空リポジトリ `Sasuraimitsu/sakanaya-punch` を作り直し、
新URLへのボタンだけを置いた `index.html` を配置します。

`Sasuraimitsu/sakanaya-productlist` に置いた移転案内ページと同じやり方です。
必要であればこちらで用意します。

---

## うまくいかないときの戻し方

移管は**逆方向にもう一度 Transfer すれば元に戻せます**
（`sakanaya-japon/sakanaya-punch` → `Sasuraimitsu`）。
データは失われません。Pages の再有効化とキオスクURLの差し戻しも忘れずに。

打刻が止まった場合の応急処置として、**GAS 側の打刻記録シートに手入力する運用**を
スタッフに周知しておくと安全です。

---

## 移管前に決めておくこと

**Org の Owner を2名以上にしてください。** 現在 `sakanaya-japon` の Owner が1名だけの場合、
そのアカウントが使えなくなると**勤怠システムごと復旧不能**になります。
出勤記録は労務上の記録でもあるため、ここは他のサイトより重要度が高いです。

https://github.com/orgs/sakanaya-japon/people から Owner 権限のメンバーを追加できます。

---

## 補足: 公開のままにする判断について

中身を確認した結果、以下を確認済みです。

- ハードコードされた認証情報・APIキーは**なし**
- 従業員名・打刻データは**リポジトリに含まれない**（すべて GAS 側）
- 認証は短命トークン（TTL 90秒）+ PIN。QRの写真を保存しても約1分で失効する設計

公開されているのは画面と呼び出しロジックのみで、**即座に悪用できる情報はありません**。
public のまま運用する判断で問題ないと考えます。

ただし1点だけ注意すると、`app.js` の `CONFIG.API_URL`（GAS の `/exec`）は誰でも読めます。
GAS 側で以下が担保されているか、一度確認しておくことを勧めます。

- `k=`（kiosk鍵）や PIN の検証が**必ずサーバ側で**行われている
- 打刻APIが総当たり攻撃に耐える（PIN試行回数の制限、レート制限）
- `doGet`/`doPost` が想定外の action を受け付けない
