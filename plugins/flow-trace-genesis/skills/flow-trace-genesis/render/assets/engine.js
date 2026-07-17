// engine.js — SPA router + copy button (addEventListener only, sandbox-safe).
// Generated docs use <section id="s-<id>"> and hash "#s-<id>".
// Adapted from mAIvt engine.js (bỏ hook DSA/KB không dùng trong flow-trace).
(function () {
  function showSection(name) {
    document.querySelectorAll('.sec').forEach(s => s.classList.remove('active'));
    const t = document.getElementById('s-' + name);
    if (t) t.classList.add('active');
    document.querySelectorAll('.nav-btn, .tn-btn').forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-target') === name);
    });
    // #main is the internal scroll container (app box has overflow:hidden); fall back to window.
    const _m = document.getElementById('main');
    if (_m && _m.scrollHeight > _m.clientHeight) _m.scrollTo({ top: 0, behavior: 'smooth' });
    else window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function activate(name, subId) {
    showSection(name);
    if (subId) {
      const el = document.getElementById(subId);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function bindNav() {
    document.querySelectorAll('.nav-btn, .tn-btn').forEach(el => {
      if (el._bound) return; el._bound = true;
      el.addEventListener('click', e => {
        e.preventDefault();
        const target = el.getAttribute('data-target');
        if (!target) return;
        try { history.pushState(null, '', '#s-' + target); }
        catch (err) { window.location.hash = 's-' + target; }
        showSection(target);
      });
    });
  }

  function wireCopy() {
    document.querySelectorAll('.code-copy').forEach(btn => {
      if (btn._bound) return; btn._bound = true;
      btn.addEventListener('click', () => {
        const pre = btn.closest('.code-wrap').querySelector('pre');
        if (!pre) return;
        navigator.clipboard.writeText(pre.innerText).then(() => {
          btn.textContent = 'Copied!'; btn.style.color = 'var(--green)';
          setTimeout(() => { btn.textContent = 'Copy'; btn.style.color = ''; }, 2000);
        });
      });
    });
  }

  function handleHash() {
    const h = window.location.hash;
    const submap = window.__SUBMAP__ || {};
    if (h.startsWith('#s-')) {
      const id = h.slice(3);
      if (document.getElementById('s-' + id)) { activate(id, null); return; }
    }
    const key = h.slice(1);
    if (submap[key]) { activate(submap[key], key); return; }
    const active = document.querySelector('.sec.active');
    const first = document.querySelector('.sec');
    activate(active ? active.id.replace(/^s-/, '') : (first ? first.id.replace(/^s-/, '') : ''), null);
  }
  window.addEventListener('hashchange', handleHash);

  function init() { bindNav(); wireCopy(); handleHash(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
