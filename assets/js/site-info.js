/* ==========================================================================
   site-info.js — 営業時間・窓口URLの唯一の情報源
   変更するときはこのファイルだけを書き換える。各ページに直接URLを書かないこと。
   （既存4ページの移行は Phase 2。詳細は docs/contact-points.md）
   ========================================================================== */

const SITE_INFO = {
  // ── 営業時間（2026-09-13 確定） ──
  hours: {
    ja: '毎日 10:00〜19:30（国民の休日を除く）',
    en: 'Daily 10:00am–7:30pm (Closed on public holidays)',
  },
  orderDeadline: {
    ja: '16:30（ご希望の配送時間の2時間前までにご注文ください）',
    en: '4:30 PM (at least 2 hours before your desired delivery time)',
  },

  // ── 店舗・会社情報 ──
  company: {
    name: 'SAKANAYA JAPON',
    established: { ja: '2024年12月19日', en: 'December 19, 2024' },
    address: {
      ja: '#72BE0, Street 174, Phum 11, Sangkat Phsar Thmey 3, Khan Daun Penh, Phnom Penh, Cambodia',
      en: '#72BE0, Street 174, Phum 11, Sangkat Phsar Thmey 3, Khan Daun Penh, Phnom Penh, Cambodia',
    },
    phone: '+855 16 881 370',
    phoneLocal: '016-881-370',
    email: 'fishstorejapan@gmail.com',
  },

  // ── 注文・問い合わせ窓口（2026-09-14 確定） ──
  order: {
    lineMiniApp:  'https://miniapp.line.me/2006469733-lgZj9vJ4', // 個人向け 主
    telegramHome: 'https://t.me/+UZAm7-eLzD0yZTA1',              // 個人向け 副
    lineOfficial: 'https://line.me/R/ti/p/@sakanayajapan',       // 個人向け 問い合わせ
    telegramBot:  'https://t.me/sakanaya_bot',                   // 法人向け 注文ボット
    telegramBiz:  'https://t.me/sakanayaorder',                  // 法人向け 問い合わせ
  },

  // ── SNS ──
  social: {
    facebook: 'https://www.facebook.com/fishstorejapan',
    telegramChannel: 'https://t.me/fishstoreJapon',
  },

  // ── 法人向け商品カタログ（sakanaya-japon Org で稼働中の本番） ──
  catalogUrl: 'https://sakanaya-japon.github.io/sakanaya-productlist/',
};
