// mermaid-init.js — render fence ```mermaid thành diagram thật (mermaid vendored).
// Render LAZY theo section active: mermaid đo kích thước bằng getBBox nên vẽ trong
// container display:none sẽ hỏng — chờ section hiện rồi mới run, đánh dấu bằng
// data-processed (mermaid tự set) để không render lại.
(function () {
  if (typeof mermaid === 'undefined') return;
  mermaid.initialize({
    startOnLoad: false,
    theme: 'dark',
    themeVariables: {
      fontFamily: "'JetBrains Mono', ui-monospace, monospace",
      fontSize: '13px',
      darkMode: true,
      background: '#0d1420',
      primaryColor: '#16202e',
      lineColor: '#64748b',
      clusterBkg: '#111a26',
      clusterBorder: '#2a3648',
      edgeLabelBackground: '#16202e'
    },
    sequence: { useMaxWidth: true },
    flowchart: { useMaxWidth: true }
  });

  function renderIn(root) {
    var nodes = root.querySelectorAll('.mermaid:not([data-processed])');
    if (nodes.length) mermaid.run({ nodes: nodes });
  }

  function init() {
    var active = document.querySelector('.sec.active');
    if (active) renderIn(active);
    var mo = new MutationObserver(function (muts) {
      muts.forEach(function (m) {
        if (m.target.classList && m.target.classList.contains('active')) renderIn(m.target);
      });
    });
    document.querySelectorAll('.sec').forEach(function (s) {
      mo.observe(s, { attributes: true, attributeFilter: ['class'] });
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else setTimeout(init, 0);
})();
