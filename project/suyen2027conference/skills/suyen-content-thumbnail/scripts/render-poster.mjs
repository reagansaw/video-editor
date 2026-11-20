#!/usr/bin/env node
// 用法：node scripts/render-poster.mjs <brief.json> [输出资料夹] [--debug]
//   出 thumb-9x16.png（1080×1920，IG reels 封面）和 wa-1x1.png（1080×1080，WhatsApp 方图）
//   --debug 会画出护脸框（紫）和 IG 网格 3:4 裁切线（青），给自己检查用，不要交出去
// 交件前会自动检查：字数上限、有没有字盖到脸框。超过就报错，不出图。
import { createRequire } from 'node:module';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require('playwright')); }
catch { ({ chromium } = require(path.resolve(process.cwd(), 'remotion/node_modules/playwright'))); }

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2).filter(a => !a.startsWith('--'));
const debug = process.argv.includes('--debug');
if (!args[0]) { console.error('用法：node render-poster.mjs <brief.json> [out]'); process.exit(1); }

const briefPath = path.resolve(args[0]);
const outDir = path.resolve(args[1] || path.dirname(briefPath));
const brief = JSON.parse(fs.readFileSync(briefPath, 'utf8'));
fs.mkdirSync(outDir, { recursive: true });

// 相对路径一律以 brief.json 所在资料夹为准，转成 file:// 给浏览器
const toUrl = p => (!p || /^(https?|file|data):/.test(p)) ? p : pathToFileURL(path.resolve(path.dirname(briefPath), p)).href;
for (const k of Object.keys(brief.assets || {})) brief.assets[k] = toUrl(brief.assets[k]);
const design = brief.design || 'golden';            // golden = 2028 参考图；case = 案例封面
const tpl = path.resolve(here, '../templates/' + ({ golden: 'poster.html', case: 'case.html' }[design] || 'poster.html'));
for (const o of [brief.poster?.sticker, brief.poster?.pill, brief.poster?.question])
  if (o?.icon && /\.(png|jpe?g|svg|webp)$/i.test(o.icon)) o.icon = toUrl(o.icon);

// ---- 字数检查（2 秒规则：眼睛只扫得完这么多） ----
const P = brief.poster || {};
const len = s => [...String(s || '').replace(/[\s\[\]]/g, '')].length;   // [重点] 的括号不算字
const errs = [];
const need = (k, max) => { if (!P[k]) errs.push(`poster.${k} 没写`); else if (len(P[k]) > max) errs.push(`poster.${k}「${P[k]}」${len(P[k])} 字，上限 ${max}`); };
const lines = (o, name, maxLines, maxEach) => { const l = o?.lines || []; if (l.length > maxLines) errs.push(`${name} 最多 ${maxLines} 行`);
  l.forEach((x, i) => { if (len(x) > maxEach) errs.push(`${name} 第 ${i + 1} 行「${x}」${len(x)} 字，上限 ${maxEach}`); }); };
if (design === 'case') {
  // 案例封面：标签 + 2 行大标题（2 秒看完的就是这 2 行）+ 米黄条 2 行 + 问句 2 行
  if (P.tag && len(P.tag) > 4) errs.push('poster.tag 上限 4 字（例：案例1）');
  need('h1', 6); need('h2', 7);
  if (len(P.h1) + len(P.h2) > 12) errs.push(`大标题 2 行加起来 ${len(P.h1) + len(P.h2)} 字，超过 12`);
  lines(P.pill, '米黄条', 2, 9); lines(P.question, '问句', 2, 9);
} else {
  const LIMIT = { line1: 4, line2: 4, band: 6, line4: 4, line4_tail: 2, bigTotal: 20 };
  for (const k of ['line1', 'line2', 'band', 'line4']) need(k, LIMIT[k]);
  if (len(P.line4_tail) > LIMIT.line4_tail) errs.push(`poster.line4_tail 上限 ${LIMIT.line4_tail} 字`);
  lines(P.sticker, '贴纸', 3, 9);
  const big = len(P.line1) + len(P.line2) + len(P.band) + len(P.line4) + len(P.line4_tail);
  if (big > LIMIT.bigTotal) errs.push(`大字加起来 ${big} 字，超过 ${LIMIT.bigTotal}（2 秒看不完）`);
}
if (errs.length) { console.error('✗ 文案不合格：\n  ' + errs.join('\n  ')); process.exit(2); }

const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
const formats = brief.formats || ['9x16', '1x1'];
const names = { '9x16': 'thumb-9x16.png', '1x1': 'wa-1x1.png' };
let bad = false;
for (const F of formats) {
  const H = F === '9x16' ? 1920 : 1080;
  const page = await browser.newPage({ viewport: { width: 1080, height: H }, deviceScaleFactor: 1 });
  await page.addInitScript(([b, f, d]) => { window.BRIEF = b; window.FORMAT = f; window.DEBUG = d; }, [brief, F, debug]);
  await page.goto(pathToFileURL(tpl).href);
  await page.waitForFunction(() => window.__READY__);
  await page.waitForLoadState('networkidle').catch(() => {});
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  // 护脸检查：任何字的框跟脸框重叠就不合格
  const hits = await page.evaluate(() => {
    const f = window.__FACE__, out = [];
    document.querySelectorAll('.gold,.white,.band,.sticker,.underline,.t,.tag,.pill,.q,.rule').forEach(e => {
      const r = e.getBoundingClientRect();
      if (r.right > f.x && r.left < f.x + f.w && r.bottom > f.y && r.top < f.y + f.h) out.push(e.textContent.trim().slice(0, 12));
    });
    return out;
  });
  const over = await page.evaluate(() => window.__OVERFLOW__ || []);
  if (over.length) { bad = true; console.error(`✗ ${F}：${over.join('、')}（删字）`); }
  if (hits.length) { bad = true; console.error(`✗ ${F}：这些字碰到脸：${hits.join('、')}（字太长，删字，不要缩字号）`); }
  const out = path.join(outDir, debug ? names[F].replace('.png', '-debug.png') : names[F]);
  await page.screenshot({ path: out });
  console.log((hits.length || over.length ? '⚠ ' : '✓ ') + out);
  await page.close();
}
await browser.close();
process.exit(bad ? 3 : 0);
