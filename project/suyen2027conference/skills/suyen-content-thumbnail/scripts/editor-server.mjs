#!/usr/bin/env node
// Content & Thumbnail 编辑器
//   node project/suyen2027conference/skills/suyen-content-thumbnail/scripts/editor-server.mjs
//   打开 http://localhost:4321
// 选设计 → 打字 → 即时预览 9:16 + 1:1 → 写四个平台文案（自动数字数、抓 AI 词）→ 按「出图」
// 出图用的是 render-poster.mjs（同一套字数检查 + 护脸检查），成品存到 content/posts/<名字>/
// 不用装任何套件；出图要 playwright（repo 的 remotion/node_modules 里有，或全域装的）。
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const skill = path.resolve(here, '..');
const repo = path.resolve(skill, '../../../..');
const postsRoot = path.resolve(skill, '../../content/posts');
const PORT = Number(process.env.PORT || 4321);

const TYPES = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml', '.webp': 'image/webp', '.css': 'text/css', '.md': 'text/markdown; charset=utf-8' };

function send(res, code, body, type = 'application/json') { res.writeHead(code, { 'Content-Type': type, 'Cache-Control': 'no-store' }); res.end(body); }
function readBody(req) { return new Promise((ok, bad) => { const c = []; req.on('data', d => c.push(d)); req.on('end', () => ok(Buffer.concat(c).toString('utf8'))); req.on('error', bad); }); }
function safeName(s) { return String(s || '').trim().replace(/[\/\\:*?"<>|\s]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 60) || 'untitled'; }
function inside(root, p) { const r = path.resolve(root, p); return r === root || r.startsWith(root + path.sep) ? r : null; }

// 上传的图（data URL）存成档，brief 里换成档名
function saveDataUrls(brief, dir) {
  const fix = (obj, key, base) => {
    const v = obj?.[key]; const m = typeof v === 'string' && v.match(/^data:image\/(png|jpe?g|webp);base64,(.+)$/);
    if (!m) return;
    const file = `${base}.${m[1] === 'jpeg' ? 'jpg' : m[1]}`;
    fs.writeFileSync(path.join(dir, file), Buffer.from(m[2], 'base64'));
    obj[key] = file;
  };
  for (const k of Object.keys(brief.assets || {})) fix(brief.assets, k, k);
  for (const k of ['sticker', 'pill', 'question']) fix(brief.poster?.[k], 'icon', `icon-${k}`);
}
// 编辑器送来的素材路径是相对 templates/ 的（assets/xxx.png），出图前转成绝对路径
function absAssets(brief) {
  const abs = v => (typeof v === 'string' && !/^(data|https?|file):/.test(v) && !path.isAbsolute(v) && !/^[\w-]+\.(png|jpe?g|webp)$/.test(v)) ? path.resolve(skill, 'templates', v) : v;
  for (const k of Object.keys(brief.assets || {})) brief.assets[k] = abs(brief.assets[k]);
  for (const k of ['sticker', 'pill', 'question']) if (brief.poster?.[k]?.icon && /\.(png|jpe?g|svg|webp)$/i.test(brief.poster[k].icon)) brief.poster[k].icon = abs(brief.poster[k].icon);
}

function copyMd(name, brief, captions) {
  const P = brief.poster, rows = brief.design === 'case'
    ? [P.tag, P.h1, P.h2, ...(P.pill?.lines || []), ...(P.question?.lines || [])]
    : [P.line1, P.line2, P.band, `${P.line4}${P.line4_tail || ''}`, ...(P.sticker?.lines || [])];
  const block = (t, s) => s?.trim() ? `**${t}**\n\`\`\`\n${s.trim()}\n\`\`\`\n` : '';
  const pending = [...new Set((JSON.stringify(brief) + JSON.stringify(captions)).match(/【待补[^】]*】/g) || [])];
  return `# ${name}\n\n> 用编辑器做的（design: ${brief.design || 'golden'}）。${brief.topic ? '题目：' + brief.topic : ''}\n\n## 海报字\n\n${rows.filter(Boolean).map(r => '- ' + r).join('\n')}\n\n## 文案\n\n` +
    block('Instagram', captions?.ig) + block('Facebook', captions?.fb) + block('WhatsApp', captions?.wa) + block('Telegram', captions?.tg) +
    `\n## 待补\n\n${pending.length ? pending.map(p => '- ' + p).join('\n') : '- （没有）'}\n`;
}

async function render(req, res) {
  let body; try { body = JSON.parse(await readBody(req)); } catch { return send(res, 400, JSON.stringify({ ok: false, log: '格式不对' })); }
  const { brief, captions, name, save } = body;
  const dir = save ? path.join(postsRoot, safeName(name)) : path.join(skill, 'out', 'preview');
  fs.mkdirSync(dir, { recursive: true });
  const b = structuredClone(brief);
  saveDataUrls(b, dir); absAssets(b);
  fs.writeFileSync(path.join(dir, 'brief.json'), JSON.stringify(b, null, 2));
  if (save) fs.writeFileSync(path.join(dir, 'copy.md'), copyMd(name, b, captions));
  const env = { ...process.env, NODE_PATH: [path.join(repo, 'remotion/node_modules'), process.env.NODE_PATH].filter(Boolean).join(path.delimiter) };
  const p = spawn(process.execPath, [path.join(here, 'render-poster.mjs'), path.join(dir, 'brief.json'), dir], { cwd: repo, env });
  let log = ''; p.stdout.on('data', d => log += d); p.stderr.on('data', d => log += d);
  p.on('close', code => {
    const rel = path.relative(skill, dir).split(path.sep).join('/');
    const inPosts = dir.startsWith(postsRoot);
    const urlBase = inPosts ? '/posts/' + path.relative(postsRoot, dir).split(path.sep).map(encodeURIComponent).join('/') : '/' + rel;
    const files = ['thumb-9x16.png', 'wa-1x1.png'].filter(f => fs.existsSync(path.join(dir, f))).map(f => `${urlBase}/${f}?t=${Date.now()}`);
    send(res, 200, JSON.stringify({ ok: code === 0, code, log: log.trim(), files, folder: path.relative(repo, dir) }));
  });
}

http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://x');
    if (req.method === 'POST' && url.pathname === '/api/render') return render(req, res);
    let p = decodeURIComponent(url.pathname);
    if (p === '/') { res.writeHead(302, { Location: '/templates/editor.html' }); return res.end(); }
    const file = p.startsWith('/posts/') ? inside(postsRoot, p.slice(7)) : inside(skill, p.slice(1));
    if (!file || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return send(res, 404, 'not found', 'text/plain');
    send(res, 200, fs.readFileSync(file), TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream');
  } catch (e) { send(res, 500, String(e), 'text/plain'); }
}).listen(PORT, '127.0.0.1', () => console.log(`编辑器：http://localhost:${PORT}  （Ctrl+C 关掉）`));
