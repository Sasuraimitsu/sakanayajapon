# 営業時間・注文窓口の統一案

調査日: 2026-09-12
調査対象: `Sasuraimitsu/sakanayajapon`（公開中5ページ） / `sakanayajapon-air` / `sakanaya-japon/sakanaya-productlist`

ページ改修に入る前に、ここを確定させる必要があります。
表示内容が食い違ったままレイアウトだけ直しても、矛盾がそのまま新しいサイトに移るだけだからです。

---

## 1. 営業時間の食い違い（実測）

| ファイル | 日本語 | 英語 |
|---|---|---|
| `aboutus.html` (L220 / L262) | 毎日 10:00〜19:30（国民の休日を除く） | Daily 10:00am–7:30pm (Closed on public holidays) |
| `q&a.html` (L197 / L251) | 火曜〜日曜 11:00〜18:00（祝日除く） | Tuesday–Sunday, 11:00 AM to 6:00 PM (Except national holidays) |

**日数も時間帯も一致していません。** 月曜が定休かどうかすら、ページによって答えが違う状態です。

### 付随して確認が必要な点

`q&a.html` には以下の記述があります（L161 / L215）。

> 注文の締切時間はありますか？ → **16:30が締切**です。ご希望の**2時間前**までにご注文ください。

`q&a.html` の営業時間（18:00 まで）だと、16:30 締切 + 2時間後配送 = **18:30 で閉店後**になります。
`aboutus.html` の 19:30 までなら整合します。

→ **2026-09-13 確定: `aboutus.html` の「毎日 10:00〜19:30（国民の休日を除く）」が正しい。**
　 したがって `q&a.html` の「火曜〜日曜 11:00〜18:00」が誤りであり、修正対象です。

### 統一案

1. ~~**正となる値を1つ決める**（推奨: `aboutus.html` 側）~~ → **確定済み**
2. **営業時間を書くページを `aboutus.html` 1か所に限定する**
3. `q&a.html` からは営業時間の記述を削除し、「営業時間は ABOUT US をご覧ください」のリンクに置き換える

同じ情報を2か所に書く限り、いつかまた片方だけ古くなります。書く場所を減らすのが唯一の根本対策です。

---

## 2. 注文・問い合わせ窓口の一覧（実測 8系統 → 整理後 7系統）

| # | 窓口 | URL / ID | 掲載場所 | 想定用途 |
|---|---|---|---|---|
| 1 | Telegram グループ（個人向け） | `t.me/+UZAm7-eLzD0yZTA1` | index, menu, howto, aboutus, q&a | 個人注文 |
| 2 | ~~Telegram グループ（法人向け）~~ | ~~`t.me/+9MZ3SB5xav42YjZl`~~ | — | **廃止済**。後継は #9 |
| 3 | Telegram チャンネル | `t.me/fishstoreJapon` | aboutus, q&a | 情報発信？ |
| 4 | Telegram 公式 | `t.me/SAKANAYAJAPON` | 現行カタログ | 法人問い合わせ |
| 5 | Telegram Bot | `t.me/sakanaya_bot` | 現行カタログ / `-air` | 注文受付ボット |
| 6 | LINE Mini App | `miniapp.line.me/2006469733-lgZj9vJ4` | menu, howto, aboutus, q&a | 個人注文 |
| 7 | LINE 公式アカウント | `line.me/R/ti/p/@sakanayajapan` | q&a のみ | 個人問い合わせ |
| 8 | Facebook | `facebook.com/fishstorejapan` | 全ページ（**2026-09-14 に統一済**） | SNS |
| 9 | Telegram（法人向け・現行） | `t.me/sakanayaorder` | `-air` | 法人の注文・問い合わせ |

### 問題点

- ~~**Facebook が2つの異なるURLで掲載**~~ → **2026-09-14 解決**。
  `facebook.com/fishstorejapan` に全8箇所を統一し、追跡パラメータ `?mibextid=ZbWKwL` も除去しました。
- ~~**法人向けグループ #2 の扱いが不明**~~ → **廃止済みと確定**。現行の法人窓口は `@sakanayaorder`（#9）。
  `-air` の案内2箇所を差し替え済みです。
- ~~**LINE ID の表記ゆれ**~~ → **現状維持で確定**。
  LINE 側は `@sakanayajapan`（japan）で登録済みのため、変更すると友だち追加リンクが切れます。
  ブランド表記 `JAPON` との不一致は許容します。
- **Telegram が依然として4系統**あります（#1 個人グループ / #3 チャンネル / #5 Bot / #9 法人）。
  役割は分かれていますが、お客様から見た使い分けの説明がページ上にありません。
  Phase 1 で個人/法人の導線を分ける際に、それぞれ1つだけ見せる形にするのが望ましいです。

### 統一案

**「1導線あたり1窓口」まで絞り込む**ことを提案します。

| 導線 | 主窓口（ボタンで大きく出す） | 副窓口（フッターに小さく） |
|---|---|---|
| 個人（For Home） | LINE Mini App #6 | Telegram グループ #1 / LINE公式 #7 |
| 法人（For Business） | Telegram Bot #5（カタログ経由） | Telegram 法人 #9 |
| SNS | Facebook #8（`fishstorejapan`） | Telegram チャンネル #3 |

**2026-09-14 確定**: #7（LINE公式アカウント）は**個人のお客様向けの問い合わせ窓口として残します**。
Mini App への一本化は行いません。#2（旧法人グループ）のみ廃止です。

---

## 3. 実装案: 情報を1か所にまとめる

Phase 2 で共通CSS化を行うとき、同時に**表示内容の単一情報源**も作ることを推奨します。
以下をそのまま `assets/js/site-info.js` として置けば動きます。

```javascript
// assets/js/site-info.js
// 営業時間・窓口URLの唯一の情報源。変更はこのファイルだけを書き換える。
// 各ページは <script src="assets/js/site-info.js" defer></script> を読み込むだけでよい。

const SITE_INFO = {
  // ── 営業時間（2026-09-13 確定。変更時はここだけ書き換える） ──
  hours: {
    ja: '毎日 10:00〜19:30（国民の休日を除く）',
    en: 'Daily 10:00am–7:30pm (Closed on public holidays)',
  },
  orderDeadline: {
    ja: '16:30（ご希望の配送時間の2時間前までにご注文ください）',
    en: '4:30 PM (at least 2 hours before your desired delivery time)',
  },

  // ── 注文窓口（2026-09-14 確定） ──
  order: {
    lineMiniApp:  'https://miniapp.line.me/2006469733-lgZj9vJ4', // 個人向け 主
    telegramHome: 'https://t.me/+UZAm7-eLzD0yZTA1',              // 個人向け 副
    lineOfficial: 'https://line.me/R/ti/p/@sakanayajapan',       // 個人向け 問い合わせ（ID は japan のままで確定）
    telegramBot:  'https://t.me/sakanaya_bot',                   // 法人向け 主
    telegramBiz:  'https://t.me/sakanayaorder',                  // 法人向け 副（旧グループから移行済み）
  },

  // ── SNS（2026-09-14 確定） ──
  social: {
    facebook: 'https://www.facebook.com/fishstorejapan',
    telegramChannel: 'https://t.me/fishstoreJapon',
  },

  // ── 法人向けカタログ（Org 側で稼働中の本番） ──
  catalogUrl: 'https://sakanaya-japon.github.io/sakanaya-productlist/',
};

/**
 * data-info 属性を持つ要素に SITE_INFO の値を流し込む。
 *   <span data-info="hours.ja"></span>
 *   <a data-info-href="order.lineMiniApp">ご注文</a>
 * 値が見つからない場合は既存のHTMLをそのまま残す（空欄にして事故らせない）。
 */
function applySiteInfo(root = document) {
  const dig = (path) => path.split('.').reduce((o, k) => (o == null ? undefined : o[k]), SITE_INFO);

  root.querySelectorAll('[data-info]').forEach((el) => {
    const v = dig(el.dataset.info);
    if (typeof v === 'string' && v !== '') el.textContent = v;
    else console.warn('[site-info] 未定義のキー:', el.dataset.info);
  });

  root.querySelectorAll('[data-info-href]').forEach((el) => {
    const v = dig(el.dataset.infoHref);
    if (typeof v === 'string' && v !== '') {
      el.href = v;
      if (/^https?:/.test(v)) { el.target = '_blank'; el.rel = 'noopener noreferrer'; }
    } else {
      console.warn('[site-info] 未定義のキー:', el.dataset.infoHref);
    }
  });
}

document.addEventListener('DOMContentLoaded', () => applySiteInfo());
```

HTML 側はこう書きます。

```html
<!-- aboutus.html -->
<li><strong>営業時間：</strong><span data-info="hours.ja">毎日 10:00〜19:30（国民の休日を除く）</span></li>

<!-- q&a.html：営業時間を持たせず、同じ値を参照するだけにする -->
<p><strong>営業時間：</strong><span data-info="hours.ja"></span></p>

<!-- 注文ボタン -->
<a class="float-btn btn-line" data-info-href="order.lineMiniApp">📲 Order by LINE</a>
```

HTML に元の文字列を残しておけば、**JS が読み込めなかった場合でも正しい営業時間が表示されます**
（`textContent` の上書きに失敗しても空欄にならない）。
`q&a.html` のように参照専用にする箇所だけは空にして、更新漏れを物理的に起こせなくします。

---

## 4. 確定をお願いしたい項目

| # | 項目 | 選択肢 |
|---|---|---|
| ~~1~~ | ~~正しい営業時間~~ | ✅ **確定: 毎日 10:00〜19:30（国民の休日を除く）** |
| ~~2~~ | ~~定休日~~ | ✅ **確定: 定休日なし（国民の休日のみ休業）** |
| ~~3~~ | ~~Facebook の正URL~~ | ✅ **確定: `facebook.com/fishstorejapan`**（全8箇所を統一済み） |
| ~~4~~ | ~~LINE ID の綴り~~ | ✅ **確定: `@sakanayajapan` のまま**（変更すると友だち追加リンクが切れるため） |
| ~~5~~ | ~~法人向け Telegram グループ #2~~ | ✅ **確定: 廃止済み。現行は `@sakanayaorder`** |
| ~~6~~ | ~~LINE 公式アカウント #7~~ | ✅ **確定: 個人のお客様向け問い合わせ窓口として残す** |

**全6項目が確定しました。** 反映状況は以下のとおりです。

| 反映内容 | 状態 |
|---|---|
| `q&a.html` の営業時間を「毎日 10:00〜19:30」に修正（日英2箇所） | ✅ 完了 |
| Facebook URL を `fishstorejapan` に統一（index / aboutus / q&a 計8箇所） | ✅ 完了 |
| 追跡パラメータ `?mibextid=ZbWKwL` の除去 | ✅ 完了 |
| `-air` の法人窓口を `@sakanayaorder` に差し替え | ✅ 完了 |
| LINE ID・LINE公式アカウント | 変更なし（現状維持で確定） |
| `assets/js/site-info.js` による単一情報源化 | ⬜ Phase 2 |
