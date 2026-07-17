// kg-init.js — render knowledge graph (Cytoscape.js vendored) từ window.__KG_DATA__.
// 2 tông: verified (từ bảng bước, đã Read) sáng — candidate (máy sinh k-hop) mờ + nét đứt.
// Panel điều khiển kiểu Obsidian graph view: search, filter theo loại node/verified,
// slider node size / link thickness / text fade, re-layout, fit.
(function () {
  var COLORS = { Class: '#00d4ff', Method: '#00ff88', Function: '#2dd4bf',
                 Interface: '#a855f7', Route: '#f59e0b', Node: '#94a3b8' };
  var S = { nodeScale: 1, linkScale: 1, labelOpacity: 1, verifiedOnly: false,
            search: '', kinds: {} };

  function buildControls(wrap, kinds, counts) {
    var panel = document.createElement('div');
    panel.className = 'kg-controls';
    var kindRows = kinds.map(function (k) {
      return '<label class="kg-row kg-kind"><input type="checkbox" data-kind="' + k + '" checked>' +
             '<span class="kg-dot" style="background:' + (COLORS[k] || COLORS.Node) + '"></span>' +
             k + ' <span class="kg-count">' + counts[k] + '</span></label>';
    }).join('');
    panel.innerHTML =
      '<div class="kg-sec">Filters</div>' +
      '<input type="search" class="kg-search" placeholder="Tìm node (fuzzy, tên/file)...">' +
      '<label class="kg-row"><input type="checkbox" data-act="verified"> Chỉ verified (bảng bước)</label>' +
      kindRows +
      '<div class="kg-sec">Display</div>' +
      '<label class="kg-row kg-slider">Node size<input type="range" min="50" max="220" value="100" data-act="node"></label>' +
      '<label class="kg-row kg-slider">Link thickness<input type="range" min="40" max="300" value="100" data-act="link"></label>' +
      '<label class="kg-row kg-slider">Text fade<input type="range" min="0" max="100" value="100" data-act="text"></label>' +
      '<div class="kg-btns"><button data-act="relayout">Re-layout</button>' +
      '<button data-act="fit">Fit</button><button data-act="reset">Reset</button></div>';
    wrap.insertBefore(panel, wrap.firstChild);
    return panel;
  }

  function init() {
    var el = document.getElementById('kg-canvas');
    var data = window.__KG_DATA__;
    if (!el || !data || typeof cytoscape === 'undefined') return;
    var wrap = el.closest('.kg-wrap') || el.parentNode;
    var elements = [];
    var counts = {};
    data.nodes.forEach(function (n) {
      counts[n.label] = (counts[n.label] || 0) + 1;
      elements.push({ data: { id: n.id, label: n.name, kind: n.label, file: n.file,
                              line: n.line, repo: n.repo, v: n.verified ? 1 : 0 } });
    });
    data.edges.forEach(function (e, i) {
      elements.push({ data: { id: 'e' + i, source: e.source, target: e.target,
                              rel: e.type, v: e.verified ? 1 : 0 } });
    });
    var kinds = Object.keys(counts).sort();
    kinds.forEach(function (k) { S.kinds[k] = true; });

    var cy = cytoscape({
      container: el,
      elements: elements,
      wheelSensitivity: 0.2,
      style: [
        { selector: 'node', style: {
            'label': 'data(label)', 'font-family': 'JetBrains Mono, monospace',
            'color': '#e2e8f0', 'text-valign': 'bottom', 'text-margin-y': 4,
            'font-size': function () { return 9 * S.nodeScale; },
            'width': function () { return 16 * S.nodeScale; },
            'height': function () { return 16 * S.nodeScale; },
            'background-opacity': 0.35,
            'background-color': function (n) { return COLORS[n.data('kind')] || COLORS.Node; },
            'border-width': 1, 'border-opacity': 0.4,
            'border-color': function (n) { return COLORS[n.data('kind')] || COLORS.Node; },
            'text-opacity': function () { return 0.45 * S.labelOpacity; } } },
        { selector: 'node[v = 1]', style: {
            'background-opacity': 1, 'border-opacity': 1, 'font-weight': 700,
            'width': function () { return 22 * S.nodeScale; },
            'height': function () { return 22 * S.nodeScale; },
            'font-size': function () { return 10 * S.nodeScale; },
            'text-opacity': function () { return S.labelOpacity; } } },
        { selector: 'edge', style: {
            'width': function () { return 1 * S.linkScale; },
            'line-color': '#64748b', 'line-opacity': 0.25, 'line-style': 'dashed',
            'curve-style': 'bezier', 'target-arrow-shape': 'triangle',
            'target-arrow-color': '#64748b', 'arrow-scale': 0.7 } },
        { selector: 'edge[v = 1]', style: {
            'line-color': '#00d4ff', 'line-opacity': 0.85, 'line-style': 'solid',
            'target-arrow-color': '#00d4ff',
            'width': function () { return 1.6 * S.linkScale; } } },
        // Chọn (tap): overlay trắng + viền trắng — tương phản mạnh với mọi màu kind.
        { selector: '.kg-hl', style: { 'background-opacity': 1, 'border-width': 3,
            'border-color': '#ffffff', 'text-opacity': 1, 'color': '#ffffff',
            'overlay-color': '#ffffff', 'overlay-padding': 6, 'overlay-opacity': 0.18,
            'z-index': 30 } },
        // Hover: node + neighborhood tô vàng ấm (#ffd166 — không trùng palette kind).
        { selector: 'node.kg-hover', style: { 'background-opacity': 1, 'border-width': 3,
            'border-color': '#ffd166', 'text-opacity': 1, 'color': '#ffd166',
            'overlay-color': '#ffd166', 'overlay-padding': 5, 'overlay-opacity': 0.2,
            'z-index': 20 } },
        { selector: 'node.kg-nbr', style: { 'background-opacity': 1, 'border-width': 2,
            'border-color': '#ffd166', 'border-opacity': 0.9, 'text-opacity': 1,
            'z-index': 10 } },
        { selector: 'edge.kg-nbr', style: { 'line-color': '#ffd166', 'line-style': 'solid',
            'line-opacity': 1, 'target-arrow-color': '#ffd166',
            'width': function () { return 2.2 * S.linkScale; }, 'z-index': 10 } },
        // Fade phần không liên quan khi hover — tương phản kiểu Obsidian.
        { selector: 'node.kg-fade', style: { 'background-opacity': 0.06, 'text-opacity': 0.03,
            'border-opacity': 0.06 } },
        { selector: 'edge.kg-fade', style: { 'line-opacity': 0.04 } },
        { selector: '.kg-dim', style: { 'background-opacity': 0.08, 'text-opacity': 0.05,
            'border-opacity': 0.08 } }
      ],
      layout: { name: 'cose', animate: false, nodeRepulsion: 9000, idealEdgeLength: 60,
                nodeOverlap: 12, padding: 20 }
    });

    // Fuzzy subsequence: "rsba2" khớp "ResubmitA2..." — các ký tự query xuất hiện đúng
    // thứ tự trong target. Substring luôn khớp trước (nhanh), fuzzy là fallback.
    function fuzzyMatch(q, s) {
      if (!s) return false;
      if (s.indexOf(q) >= 0) return true;
      var i = 0;
      for (var j = 0; j < s.length && i < q.length; j++) {
        if (s[j] === q[i]) i++;
      }
      return i === q.length;
    }

    function applyFilters() {
      var q = S.search.toLowerCase().replace(/\s+/g, '');
      cy.batch(function () {
        cy.nodes().forEach(function (n) {
          var show = S.kinds[n.data('kind')] !== false;
          if (show && S.verifiedOnly && n.data('v') !== 1) show = false;
          n.style('display', show ? 'element' : 'none');
          if (q) {
            var hit = fuzzyMatch(q, (n.data('label') || '').toLowerCase()) ||
                      fuzzyMatch(q, (n.data('file') || '').toLowerCase());
            n.toggleClass('kg-dim', !hit);
          } else n.removeClass('kg-dim');
        });
      });
    }

    var panel = buildControls(wrap, kinds, counts);
    panel.addEventListener('input', function (e) {
      var t = e.target;
      if (t.classList.contains('kg-search')) { S.search = t.value; applyFilters(); return; }
      if (t.dataset.kind) { S.kinds[t.dataset.kind] = t.checked; applyFilters(); return; }
      var act = t.dataset.act;
      if (act === 'verified') { S.verifiedOnly = t.checked; applyFilters(); }
      else if (act === 'node') { S.nodeScale = t.value / 100; cy.style().update(); }
      else if (act === 'link') { S.linkScale = t.value / 100; cy.style().update(); }
      else if (act === 'text') { S.labelOpacity = t.value / 100; cy.style().update(); }
    });
    panel.addEventListener('click', function (e) {
      var act = e.target.dataset && e.target.dataset.act;
      if (act === 'relayout') cy.layout({ name: 'cose', animate: 'end', nodeRepulsion: 9000,
                                          idealEdgeLength: 60, nodeOverlap: 12, padding: 20 }).run();
      else if (act === 'fit') cy.fit(undefined, 30);
      else if (act === 'reset') {
        S.nodeScale = 1; S.linkScale = 1; S.labelOpacity = 1;
        S.verifiedOnly = false; S.search = '';
        kinds.forEach(function (k) { S.kinds[k] = true; });
        panel.querySelectorAll('input[type=checkbox]').forEach(function (c) {
          c.checked = !c.dataset.act; });
        panel.querySelector('[data-act=verified]').checked = false;
        panel.querySelectorAll('input[type=range]').forEach(function (r) { r.value = 100; });
        panel.querySelector('.kg-search').value = '';
        cy.style().update(); applyFilters(); cy.fit(undefined, 30);
      }
    });

    // Hover-highlight kiểu Obsidian: node + neighborhood nổi vàng, phần còn lại fade.
    cy.on('mouseover', 'node', function (evt) {
      var n = evt.target;
      var hood = n.closedNeighborhood();
      cy.batch(function () {
        cy.elements().not(hood).addClass('kg-fade');
        hood.addClass('kg-nbr');
        n.removeClass('kg-nbr').addClass('kg-hover');
      });
    });
    cy.on('mouseout', 'node', function () {
      cy.batch(function () {
        cy.elements().removeClass('kg-fade kg-nbr');
        cy.nodes().removeClass('kg-hover');
      });
    });

    var info = document.getElementById('kg-info');
    cy.on('tap', 'node', function (evt) {
      cy.nodes().removeClass('kg-hl');
      var n = evt.target; n.addClass('kg-hl');
      if (info) {
        var loc = n.data('file') ? n.data('file') + (n.data('line') ? ':' + n.data('line') : '') : '';
        info.innerHTML = '<strong>' + n.data('label') + '</strong> · ' + n.data('kind') +
          (n.data('v') ? ' · verified' : ' · candidate') +
          (loc ? ' — <code>' + n.data('repo') + '/' + loc + '</code>' : '');
      }
    });
    cy.on('tap', function (evt) {
      if (evt.target === cy) {
        cy.nodes().removeClass('kg-hl');
        if (info) info.textContent = 'Click một node để xem file:line — kéo/zoom chuột để duyệt.';
      }
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
