---
name: suyen-content-thumbnail
description: Content & Thumbnail Skills —— Master Suyen（林舒苑）的①贴文文案（Facebook / Instagram / WhatsApp / Telegram，马来西亚口吻、去 AI 化、短、狠、有情绪）②海报设计（IG reels 封面 9:16 + WhatsApp 方图 1:1，两张同一套字，锁住设计只换字）。写 caption、贴文、post description、IG 文案、FB 文案、WhatsApp status / 群发图、Telegram 频道贴文、reels 封面、thumbnail、cover、海报、方图时用。
---

# Content & Thumbnail Skills

> Reagan 2026-11-20：做一个 skill，①FB / IG / WhatsApp / Telegram 的文案，②IG reels 封面 + WhatsApp 方图。两张图用同一套字。样板设计之后会给，**以后只换内容，其他照旧**。
> 参考图：`examples/ref-2028-1x1.jpg`、`examples/ref-2028-9x16.jpg`（以后所有封面和贴文都照这两张）。
> 冲突时：Reagan 在对话里的最新指示 > 这份 > `HANDOFF.md`。

一次交件 = **一套字 → 两张图 + 四个平台的文案**。

```
brief（题目 + 一句重点 + 要人做什么）
  ├─ A. 海报字（5 格）──→ thumb-9x16.png（IG reels 封面）
  │                    └→ wa-1x1.png  （WhatsApp 方图 / FB / IG feed）
  └─ B. 贴文文案 ──→ IG / FB / WhatsApp / Telegram 各一段
```

## 0. 开工前先问 4 样（缺了就问，不要自己编）

1. **这一支 / 这一篇讲什么**：一句话的重点（例：2027 是最难的一年，撑过去 2028 才吃得到）。
2. **配哪一支片 / 哪个活动**：reels 的链接、或活动日期。
3. **要人做什么（只一样）**：留言某个字 / 点链接看片 / 报名。留言送什么东西要**真的有**，没有就留【待补：留言送什么】。
4. **她的照片用哪一张**：去背的形象照（`Master Photo/`，见 `DRIVE.md`）。

## A. 海报（封面 + 方图，同一套字）

### A1. 字：只有 5 格，2 秒看完

照参考图的结构，**格子数不能加**：

| 格 | 参考图 | 做什么 | 字数上限 |
|---|---|---|---|
| `line1` 金色大数字／关键字 | 2028 | 第一眼抓住的东西：年份、数字、钱 | 4 |
| `line2` 米金大字 | 是黄金年 | 把 line1 讲完成一句「好消息／常识」 | 5 |
| `band` 红条白字 | 但你撑得过 | **转折**：「但…」「可是…」，情绪从这里来 | 6 |
| `line4` + `line4_tail` 金大字 + 白小字 | 2027 吗？ | 刺他一下的问题 / 结果 | 数字 4（中文 3）+ 2 |
| `sticker` 米黄贴纸 3 行 | 赤马红羊 · / 2026–2027 / 两年大转变 | 补充资料，**眼睛最后才看**，可以不放 | 每行 9，最多 3 行 |

- 大字加起来 ≤ 20 字（参考图 19 字）。超过 = 2 秒看不完 → 删字，**不要缩字号**。
- 读的顺序 = 上到下一条线：好消息 → 但是 → 问你。眼睛不用跳。
- 不放第二个小标题、不放 hashtag、不放网址、不放「点击观看」。
- 写法规则（去 AI 化、马来西亚口吻）跟文案一样，见 `references/copy-rules.md`。海报字更狠：**一句话只留名词和动词**。
- 出 3 组给 Reagan 挑（同结构，不同角度：钱 / 家人 / 运势），见 `references/poster-spec.md` 第 3 节。

### A0. 编辑器（不用打指令）

```bash
node project/suyen2027conference/skills/suyen-content-thumbnail/scripts/editor-server.mjs   # 在 repo 根目录跑
# 打开 http://localhost:4321
```

- 上面选设计（1 · 2028 黄金年 / 2 · 案例）→ 左边打字（每格即时数字数，超过变红）→ 右边 9:16 + 1:1 **即时预览**，碰到脸会马上报。
- 「素材」可以直接上传 logo、去背人像、无字底图。
- 「贴文文案」四个 tab（IG / FB / WhatsApp / Telegram）：自动数字数（不算 hashtag、链接）、抓 AI 味的词、表情太多、一行太长。
- 「出图 + 存档」→ 跑 `render-poster.mjs`（同样的检查），存到 `content/posts/<存档名>/`：`brief.json`、`thumb-9x16.png`、`wa-1x1.png`、`copy.md`（海报字 + 四个平台文案 + 【待补】清单）。「只试出图」不存档。
- 草稿存在浏览器里，关掉再开还在；「还原范例」回到范例字。
- 一定要用上面的网址开，直接双击 `editor.html` 不能用。

### A2. 图：锁住设计，只换字

```bash
# brief.json 照 examples/2028-golden-year/brief.json 抄，只改 poster 的字和 assets
node scripts/render-poster.mjs <brief.json> <输出资料夹>          # 出 thumb-9x16.png + wa-1x1.png
node scripts/render-poster.mjs <brief.json> <输出资料夹> --debug  # 加画护脸框和 IG 网格 3:4 裁切线
```

- 模板 `templates/poster.html`：版位、颜色、字体、金字厚度、红条、贴纸全锁在里面。**换内容只改 brief.json，不改模板。**
- 脚本会自动拒绝：超字数、任何字碰到脸框。碰到 → 删字。
- 背景两种给法（`assets`）：
  - `plate_9x16` / `plate_1x1`：**正式用这个**。设计师给的样板图「关掉文字图层」导出的底图（人、卫星、地球、底纹都在，字没有）。Reagan 给的新样板到了，就把无字底图放进 `templates/assets/`，在 `poster.html` 的 `LAYOUT` 对一次版位，之后每张都只换字。
  - `person_*` + 模板自带玫红渐层：没有底图时的替代（`examples/2028-golden-year` 就是这样做的，人是从参考图裁的，只供预览）。
- `logo`：要用 Drive 上的**透明底 SUYEN 蝴蝶 logo**。`templates/assets/logo-from-ref.png` 是从参考图裁的，有方底，只供预览。
- 字体：正式出图在 Mac 上跑（有兰亭黑 `Lantinghei SC`）。云端 Linux 没有，会退到文泉驿，字形会差一点，只能当检查图。

为什么不用 AI 直接生成整张海报：AI 画中文字会错字、每次版位都跑掉，做不到「只换字其他照旧」。AI 只拿来做**底图**（无字），字一律由模板排。要用 studio.aigoal.ai 生底图 → **只建画布，不按 Run**（`references/poster-spec.md` 第 4 节有提示词）。

### A2b. 设计 2「案例」（Reagan 11-20 给的 案例1 封面）

参考：`examples/ref-case1-9x16-clean.jpg`（无播放键）、`examples/ref-case1-9x16-screenshot.jpg`。照原封面重做的对版图：`examples/case-1-recreate/`。brief 写 `"design": "case"` 就用 `templates/case.html`。示范：`examples/case-2-sample/`。

| 格 | 参考图 | 上限 |
|---|---|---|
| `tag` 深红圆角标签 | 案例1 | 4 字 |
| `h1` 白大字 | 钱进得来， | 6 字 |
| `h2` 白大字，`[方括号]` 内变黄 | 却[拿不出来]?! | 7 字；h1+h2 ≤ 12 |
| `pill` 米黄条：图标 + 2 行深红字（`[ ]` 变亮红） | 以为赚到钱， / 结果[钱被套住]！ | 每行 9 字 |
| `question` 图标 + 2 行（第 2 行整行 `[ ]` 黄） | 投资、合作之前， / 你真的看清楚了吗？ | 每行 9 字 |

- 2 秒看完的只有 **h1 + h2**；pill 和问句是第二眼。
- 内建图标 `coins`（红钱币）、`chart`（米色上升图），也可以填图片路径或一个字。
- **案例内容一定要照那支片真的案例写**，不编。

### A3. 两个尺寸各自的规矩

| | 封面 9:16（1080×1920） | 方图 1:1（1080×1080） |
|---|---|---|
| 用在 | IG reels 封面（上传 reels 时「编辑封面 → 从相簿加入」） | WhatsApp 群发 / status、FB / IG feed、Telegram |
| 安全区 | 主页网格只露**中间 3:4**（y 240–1680），5 格字全部要在里面；底部 1/4 和右边会被 reels 按钮盖，贴纸不要再往下 | 整张都看得到；WhatsApp 预览会缩很小 → 字更要大 |
| 字放哪 | 左边一条，人在右下 | 左边一条，人在右边 |

## B. 贴文文案（FB / IG / WhatsApp / Telegram）

目标只有一个：**看到第一句心里一跳 → 忍不住读下去 → 去 IG 看片（或做那一个动作）**。

### B1. 每一段都照这个骨架

```
① 钩（1 行）    戳到他：一个他正在经历的画面 / 一句反常识。不打招呼、不自我介绍。
② 拉（2–3 行）  把情绪拉高：「你是不是也…」「最惨的是…」。短句，一句一行。
③ 转（1–2 行）  「但是」——给一点希望，不给答案（答案在片里）。
④ 推（1 行）    只叫他做一件事：去看片 / 留言一个字 / 点链接。
```

- 全文 IG ≤ 80 字、FB ≤ 120 字、WhatsApp ≤ 60 字、Telegram ≤ 100 字（不算 hashtag 和链接）。超过就删。
- 一句一行，一行手机上不换行（≤ 16 字左右）。
- 每个平台的差别、开头几个字会被截掉多少、hashtag 和格式，见 `references/captions.md`。
- 口吻：马来西亚华人讲话的样子，**去 AI 化**。黑名单和替换表在 `references/copy-rules.md`，**写之前先读**。

### B2. 一次交 2 版

- **A 版 狠**：直接戳痛（「2027 你可能会很辛苦。」）
- **B 版 好奇**：先给反常识（「2028 是好年，但很多人到不了。」）
Reagan 挑一版，四个平台都用同一版改长短。

## C. 不可以做的（跟其他 Suyen skill 一样）

- 名字一律「林舒苑」/ Master Suyen，头衔「奇门遁甲战略导师」。不提 Allianz。
- **不保证结果**（「看了就会发财」）、**不拿命运吓人**（「不看你明年会出事」）。可以讲「没看清楚就做决定，容易走冤枉路」。
- 不编数字、不编学员故事、不编「留言送 XX」。没有就【待补】。
- 字绝对不盖脸（模板会挡，但交件前自己再看一次）。

## D. 交什么

资料夹 `content/posts/<日期>-<题目>/`（或 Reagan 指定的地方）：

- `brief.json`、`thumb-9x16.png`、`wa-1x1.png`
- `copy.md`：海报 3 组字（Reagan 挑一组）＋ 文案 A / B 两版 × 四个平台 ＋【待补】清单

**先交海报字 3 组 + 文案 A/B 给 Reagan 挑，挑好才出图。**

## E. 交件前检查

- [ ] 遮住下半张，只看大字 2 秒：知道在讲什么吗？
- [ ] 海报只有 5 格，没有多出来的小标题；脚本没报错
- [ ] 9:16 的字全在 3:4 安全区（`--debug` 看青框）；字没碰脸（紫框）
- [ ] 文案第一句没有「大家好 / 今天来聊 / 你知道吗」
- [ ] 跑过 `references/copy-rules.md` 的黑名单，一个都没有
- [ ] 每段只叫他做一件事；留言送的东西是真的或写【待补】
- [ ] 林舒苑名字、头衔对；没有保证结果、没有吓人

## 档案

| 档 | 是什么 |
|---|---|
| `references/copy-rules.md` | 去 AI 化黑名单 + 马来西亚口吻用字表 + 改写前后对照 |
| `references/captions.md` | FB / IG / WhatsApp / Telegram 各自的格式、长度、hashtag、例子 |
| `references/poster-spec.md` | 两张参考图量出来的版位、颜色、字体、换设计怎么对版位、AI 底图提示词 |
| `references/cover-patterns.md` | 从小红书 / IG 高赞封面整理的规律（为什么不下载原图也在这里） |
| `templates/poster.html` | 设计 1「2028 黄金年」模板（锁设计） |
| `templates/case.html` | 设计 2「案例」模板（锁设计） |
| `scripts/render-poster.mjs` | 出图 + 字数检查 + 护脸检查 |
| `scripts/editor-server.mjs` + `templates/editor.html` | 编辑器（A0 节） |
| `examples/ref-2028-*.jpg` | Reagan 给的两张参考图 |
| `examples/2028-golden-year/` | 照参考图重做的一套：brief、两张图、文案 |
| `examples/ref-case1-9x16-screenshot.jpg` | 案例1 封面截图（设计 2 的参考） |
| `examples/case-2-sample/` | 设计 2 示范（案例2，内容是示范用的） |
