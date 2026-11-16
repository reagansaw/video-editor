# Suyen 2027 奇门战略大会广告

**素材 / 原片 / 品牌档的 Google Drive 链接一律看 `DRIVE.md`**（拿到新链接也贴回那里，不要另外记一份）。
**哪一支原片是什么看 `原片目录.md`**（写法一律 `[题目] (C0001)`）。
**做内容片前先在 `pipeline/内容片-style.md` 给那一支定 style**，并确认装了 video-craft 版式库插件（`claude plugin marketplace add reagansaw/jingjian`）。

开工前**先完整读 `HANDOFF.md`**，所有规则和流程都在里面（全部是 Reagan 批注过的）。最重要的几条：

- 横版广告只用 C0001–C0048（竖版内容片才用 C0049–C0060，见下面）
- 每支在 1 分钟以内，整支 1.1 倍速
- 字绝对不盖脸：字放人后层，再加护脸层，前景只放离脸远的东西
- 先给分镜检查图，Reagan 点头才渲染
- studio.aigoal.ai 只建画布，不按 Run
- 名字是「林舒苑」（不是林苏妍）

## 竖版内容片（C0049–C0060）
做 Suyen **竖版内容片 / reels**（玫红模板）时，先读 `skills/suyen-content-rose/SKILL.md`。跟横版广告不同：
- 段内停顿删掉 + 1.15 倍（`content/cutlib.py`）
- 不要圆框、不要瞄准框，改用聚光灯
- 一支只用 1 个 B-roll
- 下 banner 一律用 **`remotion/public/suyenc/banner_bottom_2027.png`**（2026-11-16 起，广告和内容片都用这张；2170×725 → 贴底约 361 高，盖住 y1559 以下，所以贴底的元件要收在 y≤1540）
- 片尾**不要那张整屏粉红 CTA 卡**（`CTA_ON = false`）；改成最后 3.2 秒左下角人后层「正能量」气泡（`CtaBehind`，写在 `suyenc/kit.tsx`，每一集自动有）

## 交片去哪里
影片做完（首页海报 + 下 banner + 片尾 CTA 齐了才算完成）就复制到 iCloud 的 **`Master Suyen`**（2026-11-16 改名，旧名 `Suyen`）：

| 放哪里 | 什么 |
|---|---|
| `Content 成品/` | 竖版内容片成品，档名 `内容N.mp4` |
| `Marketing Video/` | 横版广告成品，档名 `广告N.mp4` |
| `中国报 2026/` · `RAW/` · `Others/` | 原片（repo 的 `raw/` 用软连结指过去） |
| `2027 奇门战略大会/` | `Bottom Banner.png`（下 banner）、`Top Banner.png`（1:1 上 banner）、`OTO/` |
| `CTA/` | 片尾 CTA 卡 `CTA 正能量.mp4` |
| `Content Sample Thumbnail.png` | 内容片首页海报的样板（3:4 1086×1448） |
| `2027 丁未年十二生肖/` · `2027 生肖求财方向指南/` | lead magnet 的文件 |
| `Master Photo/` | 她的形象照 |

repo 里已经同步一份：`remotion/public/suyenc/banner_bottom_2027.png`、`banner_top_2027.png`、`cta_card.mp4`、`content_thumbnail_sample.png`。

**只放完成版**（高码率、不要 crf 25 手机版），粗剪／检查图／赛马备选留在 `~/Downloads`。

## 1:1 上下 banner 版
横版影片要出 1:1（1080×1080，上 banner 换字 + 中间影片不裁 + 下 banner 原图）时，先读 `docs/1比1-上下banner.md`，用 `pipeline/square_banner.py` 做。

## 落地页 / landing page
做 Suyen 的落地页、lead magnet 领取页、webinar 报名页、opt-in / thank you 页时，先读 `skills/suyen-landing/SKILL.md`（照 Canva 文案模板 + suyen2027.aigoal.ai 排版，有 lead-magnet 和 webinar 两个 category）。

## WhatsApp 讯息
写 Suyen 的 WhatsApp 讯息、活动 / webinar 前的预热讯息、提醒讯息时，先读 `skills/suyen-whatsapp/SKILL.md`（7 条预热公式；老师故事和学员案例只用真的，没有就留【待补】）。
