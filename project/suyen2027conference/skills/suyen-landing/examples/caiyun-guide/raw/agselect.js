function agSelect(sel){if(sel.__agSel||sel.multiple||sel.size>1||!sel.parentNode||sel.hasAttribute('data-native'))return;sel.__agSel=1;
var w=document.createElement('div');w.className='ag-sel';sel.parentNode.insertBefore(w,sel);w.appendChild(sel);
var btn=document.createElement('button');btn.type='button';btn.className=('ag-sel-btn '+(sel.className||'')).trim();if(sel.getAttribute('style'))btn.setAttribute('style',sel.getAttribute('style'));
btn.setAttribute('aria-haspopup','listbox');btn.setAttribute('aria-expanded','false');if(sel.getAttribute('aria-label'))btn.setAttribute('aria-label',sel.getAttribute('aria-label'));
sel.classList.add('ag-sel-native');sel.tabIndex=-1;sel.setAttribute('aria-hidden','true');
var lab=document.createElement('span');lab.className='ag-sel-label';var ar=document.createElement('span');ar.className='ag-sel-arrow';ar.setAttribute('aria-hidden','true');btn.appendChild(lab);btn.appendChild(ar);
var lb=document.createElement('div');lb.className='ag-sel-list';lb.setAttribute('role','listbox');w.appendChild(btn);w.appendChild(lb);
// 页面自己已经替这个下拉画了箭头（select 的 background-image，按钮沿用了同样的 class）→ 不再画我们的，只留一个（2026-10-28 Reagan：两个箭头）
function ownArrow(){try{if(/url\(/.test(getComputedStyle(btn).backgroundImage))w.classList.add('ag-sel-own-arrow');}catch(e){}}ownArrow();window.addEventListener('load',ownArrow);
if(sel.id){$('label[for="'+sel.id+'"]').forEach(function(l){l.addEventListener('click',function(e){e.preventDefault();btn.focus();});});}
var act=-1;
var _k='';function sync(){var o=sel.options[sel.selectedIndex];var k=sel.selectedIndex+'|'+(o?o.text:'')+'|'+sel.disabled;if(k===_k)return;_k=k;lab.textContent=o?o.text:'';btn.disabled=!!sel.disabled;if(!o||o.value==='')w.classList.add('ag-sel-ph');else w.classList.remove('ag-sel-ph');}
function items(){return lb.querySelectorAll('.ag-sel-opt:not([aria-disabled])');}
function mark(n){var it=items();if(!it.length)return;act=(n+it.length)%it.length;for(var k=0;k<it.length;k++){if(k===act)it[k].classList.add('ag-act');else it[k].classList.remove('ag-act');}if(it[act].scrollIntoView)it[act].scrollIntoView({block:'nearest'});}
function build(){lb.innerHTML='';act=-1;for(var i=0;i<sel.options.length;i++){var o=sel.options[i];if(o.hidden||(o.value===''&&o.disabled))continue;
var d=document.createElement('div');d.className='ag-sel-opt';d.setAttribute('role','option');d.setAttribute('data-i',String(i));d.textContent=o.text;
if(o.disabled)d.setAttribute('aria-disabled','true');if(i===sel.selectedIndex)d.setAttribute('aria-selected','true');lb.appendChild(d);}}
function isOpen(){return w.classList.contains('ag-sel-open');}
function open(){if(sel.disabled)return;build();w.classList.remove('ag-sel-up');w.classList.add('ag-sel-open');btn.setAttribute('aria-expanded','true');
try{var r=btn.getBoundingClientRect();if(window.innerHeight-r.bottom<Math.min(300,lb.scrollHeight+12)&&r.top>window.innerHeight-r.bottom)w.classList.add('ag-sel-up');}catch(e){}
var it=items();for(var k=0;k<it.length;k++){if(it[k].getAttribute('aria-selected')==='true'){mark(k);break;}}}
function close(){w.classList.remove('ag-sel-open');btn.setAttribute('aria-expanded','false');}
function pick(i){if(i<0||i>=sel.options.length||sel.options[i].disabled)return;var ch=sel.selectedIndex!==i;sel.selectedIndex=i;sync();close();btn.focus();
if(ch){try{sel.dispatchEvent(new Event('input',{bubbles:true}));sel.dispatchEvent(new Event('change',{bubbles:true}));}catch(e){}}}
btn.addEventListener('click',function(){if(isOpen())close();else open();});
lb.addEventListener('click',function(e){var o=e.target.closest&&e.target.closest('.ag-sel-opt');if(o&&!o.getAttribute('aria-disabled'))pick(parseInt(o.getAttribute('data-i'),10));});
btn.addEventListener('keydown',function(e){var k=e.key;if(k==='ArrowDown'||k==='ArrowUp'){e.preventDefault();if(!isOpen())open();else mark(act+(k==='ArrowDown'?1:-1));}
else if(k==='Enter'||k===' '){if(isOpen()&&act>=0){e.preventDefault();var it=items();pick(parseInt(it[act].getAttribute('data-i'),10));}}
else if(k==='Escape'||k==='Tab'){close();}});
document.addEventListener('click',function(e){if(isOpen()&&!w.contains(e.target))close();});
sel.addEventListener('change',sync);sel.addEventListener('invalid',function(){w.classList.add('ag-sel-bad');});sel.addEventListener('change',function(){w.classList.remove('ag-sel-bad');});
if(sel.form)sel.form.addEventListener('reset',function(){setTimeout(sync,0);});
sync();setInterval(function(){if(document.contains(sel))sync();},500);}