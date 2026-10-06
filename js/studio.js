/* PJ116 通用脚本：1) 从网址 ?theme=12&bg=05 或本地记忆应用主题/背景  2) 右下角"样式切换条"（选编号即可预览）  3) 滚动出现动效 */
(function () {
  var C = window.PJ116 || { themes: [], bgs: [] }, de = document.documentElement, q = new URLSearchParams(location.search);
  function get(k) { var v = q.get(k); if (v == null) { try { v = localStorage.getItem('pj116-' + k); } catch (e) {} } return v; }
  function put(k, v) { try { localStorage.setItem('pj116-' + k, v); } catch (e) {} }
  function pad(n) { n = String(n).replace(/\D/g, ''); return n.length === 1 ? '0' + n : n; }
  function setTheme(n) { n = pad(n); if (!n) return; de.dataset.theme = 't' + n; put('theme', n); }
  function setBg(n) { if (n === 'user') { de.dataset.bg = 'user'; put('bg', 'user'); return; } if (n === 'none') { de.dataset.bg = 'none'; put('bg', 'none'); return; } n = pad(n); if (!n) return; de.dataset.bg = n; put('bg', n); }
  var t = get('theme'), b = get('bg');
  if (t) setTheme(t); else if (!de.dataset.theme) de.dataset.theme = de.getAttribute('data-default-theme') || 't01';
  if (b) setBg(b); else if (!de.dataset.bg) de.dataset.bg = de.getAttribute('data-default-bg') || '02';
  // 用户自己的照片背景：存在 localStorage 'pj116-userbg'（dataURL），用 data-bg="user"
  function setUserBg(u) {
    var st = document.getElementById('pj116-userbg');
    if (!u) { try { localStorage.removeItem('pj116-userbg'); } catch (e) {} if (st) st.remove(); if (de.dataset.bg === 'user') de.dataset.bg = 'none'; return; }
    if (!st) { st = document.createElement('style'); st.id = 'pj116-userbg'; document.head.appendChild(st); }
    st.textContent = '[data-bg="user"]{--bg-img:url("' + u + '")}'; de.dataset.bg = 'user'; put('bg', 'user');
  }
  window.PJ116apply = { setTheme: setTheme, setBg: setBg, setUserBg: setUserBg };
  var noSw = q.has('nosw');
  if (!noSw) { try { var ub = localStorage.getItem('pj116-userbg'); if (ub && localStorage.getItem('pj116-bg') === 'user') setUserBg(ub); } catch (e) {} }
  // 动态背景脚本（和本脚本同目录）
  if (!noSw && !window.PJ116live) { var cs = document.currentScript; if (cs) { var ls = document.createElement('script'); ls.src = cs.src.replace('studio.js', 'livebg.js'); document.head.appendChild(ls); } }

  function reveal() {
    var els = document.querySelectorAll('[data-reveal],.grow-bar');
    if (!('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { threshold: .15 });
    els.forEach(function (e) { io.observe(e); });
  }
  function bar() {
    if (q.has('nosw') || document.body.hasAttribute('data-no-switcher') || !C.themes.length) return;
    var d = document.createElement('div'); d.className = 'switcher';
    var th = C.themes.map(function (x) { return '<option value="' + x.n + '">' + (x.n < 10 ? '0' : '') + x.n + ' ' + x.name + '</option>'; }).join('');
    var bgs = '<option value="none">无背景图</option>' + C.bgs.map(function (x) { return '<option value="' + x.n + '">' + (x.n < 10 ? '0' : '') + x.n + ' ' + x.name + '</option>'; }).join('');
    d.innerHTML = '<button type="button" class="sw-toggle" aria-expanded="false" aria-label="换主题和背景">🎨</button><div class="sw-panel" hidden><label>主题<select id="swT">' + th + '</select></label><label>背景<select id="swB">' + bgs + '</select></label><small class="muted">改动会记住，所有模板页都用</small><a href="' + (document.body.dataset.root || '../') + 'index.html">← 设计库首页</a></div>';
    document.body.appendChild(d);
    var st = d.querySelector('#swT'), sb = d.querySelector('#swB'), tg = d.querySelector('.sw-toggle'), pn = d.querySelector('.sw-panel');
    st.value = String(parseInt(de.dataset.theme.slice(1), 10)); sb.value = de.dataset.bg === 'none' ? 'none' : String(parseInt(de.dataset.bg, 10));
    st.onchange = function () { setTheme(st.value); }; sb.onchange = function () { setBg(sb.value); };
    tg.onclick = function () { var o = pn.hidden; pn.hidden = !o; tg.setAttribute('aria-expanded', o); };
  }
  function ready() { reveal(); bar(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();
})();
