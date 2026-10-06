/* 模板可直接改字：body 上写 data-editable data-ref="参考网址"。点文字就能改，"下载 HTML"得到单文件（样式已内联）。 */
(function(){
  var b=document.body;if(!b.hasAttribute('data-editable'))return;
  var sel='h1,h2,h3,h4,p,li,span,b,.logo,.item,.go,.more,.btn,.pill,.st b,.st span';
  function on(){document.querySelectorAll(sel).forEach(function(e){if(e.closest('#edbar'))return;e.setAttribute('contenteditable','true');e.spellcheck=false})}
  on();
  var s=document.createElement('style');
  s.textContent='[contenteditable]:hover{outline:2px dashed rgba(47,128,237,.6);outline-offset:2px}[contenteditable]:focus{outline:2px solid #2f80ed;outline-offset:2px}#edbar{position:fixed;right:10px;bottom:10px;z-index:99;display:flex;gap:6px;align-items:center;flex-wrap:wrap;background:#14233a;color:#fff;padding:6px 8px;border-radius:10px;font:13px system-ui,sans-serif;box-shadow:0 4px 18px rgba(0,0,0,.3)}#edbar a,#edbar button{color:#fff;background:#2f80ed;border:0;border-radius:6px;padding:4px 10px;font:inherit;text-decoration:none;cursor:pointer}#edbar a.ref{background:transparent;text-decoration:underline}';
  document.head.appendChild(s);
  var bar=document.createElement('div');bar.id='edbar';
  var ref=b.getAttribute('data-ref');
  bar.innerHTML='<span>✏️ 点文字直接改</span>'+(ref?'<a class="ref" target="_blank" rel="noopener" href="'+ref+'">参考原站 ↗</a>':'')+'<button type="button" id="edDl">下载 HTML</button>';
  b.appendChild(bar);
  document.getElementById('edDl').onclick=function(){
    var links=[].slice.call(document.querySelectorAll('link[rel=stylesheet]'));
    Promise.all(links.map(function(l){return fetch(l.href).then(function(r){return r.text()}).catch(function(){return ''})})).then(function(cs){
      var d=document.documentElement.cloneNode(true);
      d.querySelectorAll('link[rel=stylesheet],script,#edbar').forEach(function(n){n.remove()});
      d.querySelectorAll('[contenteditable]').forEach(function(n){n.removeAttribute('contenteditable');n.removeAttribute('spellcheck')});
      var st=document.createElement('style');st.textContent=cs.join('\n');d.querySelector('head').appendChild(st);
      var a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['<!doctype html>\n'+d.outerHTML],{type:'text/html'}));a.download='my-page.html';a.click();
    });
  };
})();
