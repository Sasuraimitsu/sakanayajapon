/* ==========================================================================
   common.js — 日英切替 と site-info.js の値の流し込み
   読み込み順: site-info.js → common.js（どちらも defer）
   ========================================================================== */

(function () {
  'use strict';

  var STORAGE_KEY = 'sakanaya.lang';
  var VALID = ['ja', 'en'];

  /* ── 言語の決定 ────────────────────────────────────
     ①前回の選択 → ②ブラウザの言語 → ③日本語 の順に決める。
     localStorage はプライベートモード等で例外を投げるため必ず try/catch。 */
  function readSavedLang() {
    try {
      var v = window.localStorage.getItem(STORAGE_KEY);
      return VALID.indexOf(v) >= 0 ? v : null;
    } catch (e) {
      return null;
    }
  }

  function saveLang(lang) {
    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* 保存できなくても表示は成立するので無視する */
    }
  }

  function detectLang() {
    var saved = readSavedLang();
    if (saved) return saved;
    var nav = (navigator.language || navigator.userLanguage || 'ja').toLowerCase();
    return nav.indexOf('ja') === 0 ? 'ja' : 'en';
  }

  /* ── 言語の適用 ──────────────────────────────────── */
  function setLang(lang) {
    if (VALID.indexOf(lang) < 0) lang = 'ja';
    document.documentElement.setAttribute('lang', lang);

    // data-ja / data-en を持つ要素はテキストを差し替える
    var nodes = document.querySelectorAll('[data-ja][data-en]');
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i].getAttribute('data-' + lang);
      if (t !== null && t !== '') nodes[i].textContent = t;
    }

    // 切替ボタンの状態
    var btns = document.querySelectorAll('.lang-toggle button[data-set-lang]');
    for (var j = 0; j < btns.length; j++) {
      btns[j].setAttribute('aria-pressed',
        btns[j].getAttribute('data-set-lang') === lang ? 'true' : 'false');
    }

    applySiteInfo(lang);
    saveLang(lang);
  }

  /* ── site-info.js の値を流し込む ─────────────────────
       <span data-info="hours"></span>              → 現在の言語の値
       <span data-info="company.phone"></span>      → 言語を持たない値はそのまま
       <a data-info-href="order.lineMiniApp"></a>   → href に設定
     値が取れない場合は HTML に書かれた既定値を残す（空欄にして事故らせない）。 */
  function dig(path, root) {
    var parts = path.split('.');
    var cur = root;
    for (var i = 0; i < parts.length; i++) {
      if (cur === null || typeof cur !== 'object') return undefined;
      cur = cur[parts[i]];
    }
    return cur;
  }

  function applySiteInfo(lang) {
    if (typeof SITE_INFO === 'undefined') {
      // site-info.js の読み込みに失敗した場合。HTML の既定値がそのまま残る。
      console.warn('[common.js] site-info.js が読み込まれていません');
      return;
    }

    var texts = document.querySelectorAll('[data-info]');
    for (var i = 0; i < texts.length; i++) {
      var v = dig(texts[i].getAttribute('data-info'), SITE_INFO);
      if (v && typeof v === 'object') v = v[lang];          // { ja, en } 形式
      if (typeof v === 'string' && v !== '') {
        texts[i].textContent = v;
      } else {
        console.warn('[common.js] 未定義のキー:', texts[i].getAttribute('data-info'));
      }
    }

    var links = document.querySelectorAll('[data-info-href]');
    for (var k = 0; k < links.length; k++) {
      var u = dig(links[k].getAttribute('data-info-href'), SITE_INFO);
      if (typeof u === 'string' && u !== '') {
        links[k].setAttribute('href', u);
        if (/^https?:/i.test(u)) {
          links[k].setAttribute('target', '_blank');
          links[k].setAttribute('rel', 'noopener noreferrer');
        }
      } else {
        console.warn('[common.js] 未定義のキー:', links[k].getAttribute('data-info-href'));
      }
    }
  }

  /* ── 初期化 ──────────────────────────────────────── */
  function init() {
    var btns = document.querySelectorAll('.lang-toggle button[data-set-lang]');
    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        btn.addEventListener('click', function () {
          setLang(btn.getAttribute('data-set-lang'));
        });
      })(btns[i]);
    }
    setLang(detectLang());
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // 既存ページから呼べるよう公開しておく（Phase 2 の移行用）
  window.SakanayaCommon = { setLang: setLang };
})();
