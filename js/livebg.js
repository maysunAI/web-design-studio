/* PJ116 动态背景：蓝天白云(云飘) / 下雨(地上有水花) / 大海(海浪) / 大雪(风吹枯树)。
   纯 Canvas，无图片、无外部库。PJ116live.set('sky'|'rain'|'sea'|'snow'|'none') 设为整页背景；
   PJ116live.mount(canvas, kind) 在任意 canvas 里播放（用于预览小卡片），返回停止函数。
   系统开了"减少动态效果"时只画静止的一帧。 */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function rnd(a, b) { return a + Math.random() * (b - a); }

  function grad(c, w, h, stops) {
    var g = c.createLinearGradient(0, 0, 0, h);
    stops.forEach(function (s) { g.addColorStop(s[0], s[1]); });
    c.fillStyle = g; c.fillRect(0, 0, w, h);
  }
  function puff(c, x, y, s, a) {            // 一朵云 = 几个圆叠在一起
    c.fillStyle = 'rgba(255,255,255,' + a + ')';
    [[0, 0, 1], [-.9, .25, .7], [.9, .2, .75], [-.35, -.3, .75], [.45, -.25, .65]].forEach(function (p) {
      c.beginPath(); c.arc(x + p[0] * s, y + p[1] * s, p[2] * s, 0, 6.2832); c.fill();
    });
  }

  var scenes = {
    sky: function () {
      var clouds = [];
      for (var i = 0; i < 9; i++) clouds.push({ x: rnd(0, 1), y: rnd(.05, .55), s: rnd(.03, .09), v: rnd(.006, .02), a: rnd(.6, .95) });
      return function (c, w, h, t, dt) {
        grad(c, w, h, [[0, '#4aa3f0'], [.7, '#a9d8fb'], [1, '#e6f4ff']]);
        c.fillStyle = 'rgba(255,244,190,.9)'; c.beginPath(); c.arc(w * .86, h * .16, Math.min(w, h) * .05, 0, 6.2832); c.fill();
        clouds.forEach(function (k) {
          k.x += k.v * dt; if (k.x > 1.2) k.x = -.2;
          puff(c, k.x * w, k.y * h, k.s * Math.min(w, h * 1.6), k.a);
        });
      };
    },
    rain: function () {
      var drops = [], rings = [], N = 160;
      return function (c, w, h, t, dt) {
        grad(c, w, h, [[0, '#3b4658'], [1, '#1f2733']]);
        var ground = h * .86;
        c.fillStyle = '#18202b'; c.fillRect(0, ground, w, h - ground);
        while (drops.length < N) drops.push({ x: rnd(0, w), y: rnd(-h, 0), v: rnd(.9, 1.5), l: rnd(.025, .05) });
        c.strokeStyle = 'rgba(190,215,255,.65)'; c.lineWidth = 1.3; c.beginPath();
        drops.forEach(function (d) {
          d.y += d.v * h * .9 * dt; d.x -= d.v * w * .05 * dt;
          if (d.y > ground + rnd(0, h * .1)) {            // 落地：产生水花圈
            rings.push({ x: d.x, y: d.y > h ? ground + 4 : d.y, r: 1, a: .6 });
            d.y = rnd(-h * .3, 0); d.x = rnd(0, w * 1.1);
          }
          c.moveTo(d.x, d.y); c.lineTo(d.x + d.l * h * .12, d.y - d.l * h);
        });
        c.stroke();
        rings = rings.filter(function (r) { return r.a > .02; });
        rings.forEach(function (r) {
          r.r += 28 * dt; r.a -= 1.1 * dt;
          c.strokeStyle = 'rgba(200,225,255,' + r.a + ')'; c.lineWidth = 1.2;
          c.beginPath(); c.ellipse(r.x, r.y, r.r, r.r * .32, 0, 0, 6.2832); c.stroke();
        });
      };
    },
    sea: function () {
      return function (c, w, h, t) {
        var hz = h * .45;
        grad(c, w, hz, [[0, '#7cc3ff'], [1, '#fde7c0']]);
        c.fillStyle = 'rgba(255,240,200,.95)'; c.beginPath(); c.arc(w * .75, hz - h * .05, Math.min(w, h) * .06, 0, 6.2832); c.fill();
        var cols = ['#2f86c8', '#2573b5', '#1b5f9d', '#144b83'];
        for (var k = 0; k < cols.length; k++) {                        // 4 层海浪，速度和起伏各不同
          var y0 = hz + (k + .6) * (h - hz) / (cols.length + .4), amp = h * (.012 + k * .006), sp = .6 + k * .25, len = w / (2.2 + k * .6);
          c.fillStyle = cols[k]; c.beginPath(); c.moveTo(0, h);
          for (var x = 0; x <= w; x += 8) c.lineTo(x, y0 + Math.sin(x / len * 6.2832 / 3 + t * sp + k * 1.7) * amp + Math.sin(x / len * 6.2832 / 1.3 - t * sp * .7) * amp * .4);
          c.lineTo(w, h); c.closePath(); c.fill();
        }
      };
    },
    snow: function () {
      var flakes = [], N = 140;
      function branch(c, x, y, len, ang, depth, sway) {
        if (depth === 0 || len < 4) return;
        var x2 = x + Math.cos(ang) * len, y2 = y + Math.sin(ang) * len;
        c.lineWidth = Math.max(1, depth * 1.4); c.beginPath(); c.moveTo(x, y); c.lineTo(x2, y2); c.stroke();
        var s = sway * (1 / depth) * .5;                             // 越细的枝摆得越多
        branch(c, x2, y2, len * .74, ang - .42 + s, depth - 1, sway);
        branch(c, x2, y2, len * .72, ang + .38 + s, depth - 1, sway);
      }
      return function (c, w, h, t, dt) {
        grad(c, w, h, [[0, '#5b6b84'], [1, '#c9d5e6']]);
        var ground = h * .84;
        c.fillStyle = '#eef3fa'; c.beginPath(); c.moveTo(0, h);
        for (var x = 0; x <= w; x += 20) c.lineTo(x, ground + Math.sin(x / w * 9) * h * .012);
        c.lineTo(w, h); c.fill();
        var wind = Math.sin(t * .8) * .5 + .5;                        // 风忽大忽小
        c.strokeStyle = '#2a2420'; c.lineCap = 'round';
        branch(c, w * .22, ground + 4, h * .17, -Math.PI / 2 + wind * .06, 8, Math.sin(t * 1.6) * wind * .5);
        while (flakes.length < N) flakes.push({ x: rnd(0, w), y: rnd(0, h), r: rnd(1, 3.2), v: rnd(.03, .09), p: rnd(0, 6) });
        c.fillStyle = 'rgba(255,255,255,.92)';
        flakes.forEach(function (f) {
          f.y += f.v * h * dt; f.x += (Math.sin(t + f.p) * .02 + wind * .07) * w * dt;
          if (f.y > h) { f.y = -5; f.x = rnd(0, w); } if (f.x > w) f.x = 0;
          c.beginPath(); c.arc(f.x, f.y, f.r, 0, 6.2832); c.fill();
        });
      };
    }
  };

  function mount(canvas, kind) {
    if (!scenes[kind]) return function () {};
    var c = canvas.getContext('2d'), draw = scenes[kind](), raf = 0, last = 0, t = 0, dead = false;
    function size() {
      var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(2, Math.round((r.width || innerWidth) * dpr)); canvas.height = Math.max(2, Math.round((r.height || innerHeight) * dpr));
    }
    function frame(now) {
      if (dead) return;
      var dt = last ? Math.min((now - last) / 1000, .05) : .016; last = now; t += dt;
      draw(c, canvas.width, canvas.height, t, dt);
      if (!reduce) raf = requestAnimationFrame(frame);
    }
    size(); window.addEventListener('resize', size);
    raf = requestAnimationFrame(frame);
    return function () { dead = true; cancelAnimationFrame(raf); window.removeEventListener('resize', size); };
  }

  var page = null, stop = null;
  function set(kind) {
    if (stop) { stop(); stop = null; }
    if (page) { page.remove(); page = null; }
    try { localStorage.setItem('pj116-live', kind || 'none'); } catch (e) {}
    if (!kind || kind === 'none' || !scenes[kind]) { document.documentElement.removeAttribute('data-live'); return; }
    document.documentElement.dataset.live = kind;
    page = document.createElement('canvas');
    page.setAttribute('aria-hidden', 'true');
    page.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none';
    // 字是浅色(深色主题)就把背景压暗，字是深色就稍微提亮，保证字看得清
    var m = (getComputedStyle(document.body).color.match(/\d+/g) || [0, 0, 0]).map(Number), lum = (m[0] * .3 + m[1] * .59 + m[2] * .11) / 255;
    page.style.filter = lum > .5 ? 'brightness(.62) saturate(.95)' : 'brightness(1.12) saturate(.75) contrast(.85)';
    document.body.appendChild(page);
    stop = mount(page, kind);
  }
  window.PJ116live = { set: set, mount: mount, kinds: ['sky', 'rain', 'sea', 'snow'] };

  function init() {
    if (new URLSearchParams(location.search).has('nosw')) return;
    var q = new URLSearchParams(location.search).get('live'), v = q;
    if (v == null) { try { v = localStorage.getItem('pj116-live'); } catch (e) {} }
    if (v && v !== 'none') set(v);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
