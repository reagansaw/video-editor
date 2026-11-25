# 2027 生肖财运指南 · 上线记录（2026-11-18）

| 网址 | aigoal page id | 是什么 |
|---|---|---|
| https://suyen2027-caiyun.aigoal.ai | lf1skpvx | **正式版**（raw，含出生年份表单、PDF 下载） = `index-prod.html` |
| https://suyen2027-caiyun-v1.aigoal.ai | nsdxd10s | 旧 asis 版，**仍挂在 funnel pbme0shf 的 optin**；正式版的报名都送到这个 slug，自动化照常跑 |
| https://suyen2027-caiyun-test.aigoal.ai | lk70bgy3 | 测试版（报名送到自己，不跑 funnel） |
| https://suyen2027-caiyun-ok.aigoal.ai | x6xiwtve | 报名成功页 |

旧版原始码备份：`backup-suyen2027-caiyun-asis.json`。
重建正式版：`python3 make_raw.py ../optin.html lichun.json out.html suyen2027-caiyun-v1 https://suyen2027-caiyun-ok.aigoal.ai suyen2027-caiyun`，再把图片 src 换成 `img-urls.json` 里的 /avatars 网址。

## 2026-11-18 暂停 funnel 讯息（Reagan：先停，等他再叫）
- 生肖 funnel（pbme0shf）的欢迎讯息 A 关不掉（aigoal 不存 A 的 off），所以改成**正式页报名送到自己的 slug**（`FUNNEL_SLUG=suyen2027-caiyun`，page lf1skpvx 不挂 funnel）→ 名单照收、照打 tag，但不进 funnel、不发 funnel 讯息。
- **恢复**：用 `suyen2027-caiyun-v1` 当 funnel slug 重建（`make_raw.py ... suyen2027-caiyun-v1 https://suyen2027-caiyun-ok.aigoal.ai suyen2027-caiyun`）再存回 lf1skpvx。
- 没动：大会 funnel ix2g7pr9（1036 人）、bot 规则（「我要出席奇门战略大会」→ registered_webinar + 恭喜讯息 照常）。
- 改动前的 funnel / bot 设定备份在 `backup-automation-2026-11-18/`。

## PDF（2026-11-18 起）
- PDF 不再在访客浏览器里画：`prerender12.js` 用真 Chrome 以网页宽度（1100px）把 12 个生肖各截一张长图（含该生肖全部出生年份卡），上传到 aigoal（挂在 thank-you 页 x6xiwtve，每页上限 20 张图），网址和切图位置在 `pdfz.json`。
- 按钮只是把那张图切成「上段 + 访客那一年的卡 + 下段」包成一页 PDF。内容有改（文案 / 补图）就要重跑 `prerender12.js`、重传、`PDFZ=pdfz.json python3 make_raw.py ...` 重建。
- 见证影片：raw 页不准嵌 iframe（frame-src 'none'），已改成 `<video>`（Bunny HLS + original mp4）。
- 2026-11-19：排名卡换成奇门盘后，12 张 PDF 长图重拍，传到旧页 nsdxd10s（suyen2027-caiyun-v1，原 4 张图，还剩 4 个位置）；conf 卡（含 WhatsApp QR）仍在 x6xiwtve（已满 20）。

## 2026-11-19 大会页 + OTO
- 新页 **https://suyen2027-caiyun-dahui.aigoal.ai**（id 25qmc3u8，「舒苑2027奇门遁甲战略大会 · 生肖财运指南」）＝ suyen2027 原大会页的复制；7 个「立即报名，提前布局 2027」都直接去 OTO https://suyen2027-vip.aigoal.ai/，没有弹窗。6 支见证影片已补上；右下 WhatsApp 浮动按钮用 CSS 藏起来（原页也没有）。
- 生肖页所有「立即报名」改去这个大会页（`make_raw.py` 的 CONF_PAGE）。
- 注意：suyen2027-caiyun-v1（nsdxd10s）、suyen2027-caiyun-ok（x6xiwtve）、suyen2027-caiyun-test（lk70bgy3）已被删除（不是 Claude 删的）；上传在那些页的图片网址照样能开。

## 2026-11-20 接上主大会 funnel（2027 Master Suyen 战略大会 · 报名，ix2g7pr9）
- 生肖页出生年份表单 → 报名送到 `landing:suyen2027`（主 funnel 的 optin），所以进主 funnel 的欢迎 + 提醒流程；回传的报名码 ft 带到「立即报名」→ 大会页 ?ft= → 大会页 7 个按钮（data-cta="order"，平台自动带 ft）→ VIP OTO ?ft=（付款才认得是谁）。
- 标签由页面设定决定：主 funnel 只打 `registered_webinar`；表单送的 `lead_magnet_2027_十二生肖` 不会被采用（生肖资料在栏位 birth_year / dob_pillar 和备注里）。
- 测试时误建了一个真实联系人「测试 / t@example.com / 0123456789」（id o2bfprll），需要在 CRM 手动删除。

## 2026-11-20 生肖 Webinar Funnel「2027 生肖财运指南 · 林舒苑老师」（iyawii07）
| aigoal 步骤 | 页 | 网址 |
|---|---|---|
| Opt-in | gzvyfwvf（funnel 页会剥掉 script，只放「打开指南」按钮） | suyen2027-caiyun-optin |
| Thank-you | tgp4spue＝大会页（复制 suyen2027，6 支影片，7 个按钮 data-cta=order → VIP 页 +ft） | suyen2027-caiyun-dahui |
| Sales | bzgzmyy3＝VIP 升级复制（pay_offers 同原页：vip RM104.76 → suyen2027-vipok） | suyen2027-caiyun-vip |
- 真正的指南仍是 raw 页 lf1skpvx（suyen2027-caiyun + 2027shengxiaocaifu.suyenlim.com）；它的表单要改成报名到 `landing:suyen2027-caiyun-optin`（等欢迎讯息文字核准后才切）。
- 讯息：B/C/C2/F1-F3 已关；A 欢迎讯息 aigoal 关不掉。webinar_at 2027-01-08T20:30，community 同主 funnel。
- 旧的单独大会复制页 → suyen2027-caiyun-dahui-old；多出来的草稿 2027-6j1m（kwa1cqev）可删。
- aigoal 限制：funnel 只能用一次 import 建；没有「把现有页加进 funnel」的 API；funnel 页会剥 script / meta refresh。
- 2026-11-20 更新：funnel Opt-in（suyen2027-caiyun-optin）改放「无 script 版指南」（optin.html：点生肖看解读 + aigoal 报名弹窗，报名后自动去大会页并带 ft），补了 6 支影片；平台自动加的「留下资料」表单因此消失。
- 2026-11-20 选方案 1：funnel Opt-in（gzvyfwvf）改用 `suyen2027-caiyun` + 自订域名 https://2027shengxiaocaifu.suyenlim.com；完整版 raw 指南（lf1skpvx）移到 `suyen2027-caiyun-full` 当备份（它的表单仍报名到主 funnel suyen2027）。
- 欢迎讯息：reply_gate 开；A_GATE＝「你好 {name}👋 你的报名收到啦！🎉 / 2027奇门战略大会的线上分享会位置帮你锁好了。/ 回我一个「YES」…🎁」+ 按钮 YES；AY、A 照主 funnel；图片同主 funnel。其他 6 步全关。
- 2026-11-20 最终：入口改回完整版指南 lf1skpvx（`suyen2027-caiyun` + 2027shengxiaocaifu.suyenlim.com，有出生年份框、自动打开、PDF）。它的表单报名到 funnel「2027 生肖财运指南 · 林舒苑老师 (NEW)」(iyawii07) 的 Opt-in `landing:suyen2027-caiyun-optin`，拿 ft → 大会页 suyen2027-caiyun-dahui → VIP suyen2027-caiyun-vip。funnel 自己的 Opt-in 页（gzvyfwvf，无 script 版）留在 suyen2027-caiyun-optin，没有连结过去。

## 2026-11-20 定案：Webinar Funnel「2027 生肖财运指南 · 林舒苑老师 (NEW)」= 7xi22jze（照主 funnel 2027 Master Suyen 战略大会 · 报名 复制）
| 步骤 | 页 | 网址（经 2027shengxiaocaifu.suyenlim.com） |
|---|---|---|
| Opt-in | fjzxneaz：资料框（称呼/Email/WhatsApp/出生年份＝aigoal 报名表单）；4 项有效后指南用 CSS :has 显示在下面；所有「立即报名」= 送出这个表单 | `/`（suyen2027-caiyun） |
| Thank-you | k7b6bala：VIP 升级（RM104.76，tag vip，付款后去 vipok；不升级 → join） | /suyen2027-caiyun-vip |
| Sales | 6ks4fei9：登记成功（没升级 VIP） | /suyen2027-caiyun-join |
| Sales | gxf9zmmh：VIP 升级成功 | /suyen2027-caiyun-vipok |
- 设定：webinar_at 2027-01-08T20:30；community 同主 funnel；reply gate（A_GATE「你好 {name}👋 你的报名收到啦！…回我一个「YES」…」+ YES 钮；AY/A 同主 funnel）；B/C/C2/F1-F3 关。
- 旧的：iyawii07「(old)」、uvlroqgh「(old2)」的页都改成 *-old / *-old2；完整版 raw 指南 lf1skpvx 在 suyen2027-caiyun-full（备份，没连结）。生成器：`raw/funnel/build_v3.py`（读 rawsite/prod-live.html）。

## 2026-11-20 最终定案（改回 5 步，要先送出表单才看到指南）
「(NEW)」= **uvlroqgh**：Opt-in `/`（资料框，按「看我的 2027 财运 →」送出）→ `/suyen2027-caiyun-guide`（选出生年份 → 显示指南；26 个立即报名直接连 VIP + ft）→ `/suyen2027-caiyun-vip` → `/suyen2027-caiyun-join`（没升级）/ `/suyen2027-caiyun-vipok`（VIP）。网域 2027shengxiaocaifu.suyenlim.com。
7xi22jze 改名「(old3)」，页 *-old3。生成器 `raw/funnel/build_new.py`。
- 2026-11-20：第 2 页（suyen2027-caiyun-guide）选年份后，排名卡下面出现「下载我的 2027 指南 PDF ↓」（98 个按年份的连结，CSS 只显示选中那一年）→ 开 https://suyen2027-caiyun-full.aigoal.ai/?pdf=年份 → 完整版指南的下载画面，按「下载 PDF」生成那一年的 PDF（aigoal 不收 PDF 上传，所以用这个方式）。第 2 页的 WhatsApp 浮动按钮已藏。

## 2026-11-20 现行（同一个网域 2027shengxiaocaifu.suyenlim.com）
| 网址 | 页 |
|---|---|
| `/` | 完整版指南 lf1skpvx（slug suyen2027-caiyun）：资料框 → 同一页打开指南 + PDF；报名送到 (NEW) 的 Opt-in `landing:suyen2027-caiyun-optin`，拿 ft |
| `/suyen2027-caiyun-vip` | (NEW) VIP 升级（立即报名 26 个都连这里 +ft） |
| `/suyen2027-caiyun-join` | (NEW) 登记成功（没升级） |
| `/suyen2027-caiyun-vipok` | (NEW) VIP 升级成功 |
- (NEW)=uvlroqgh 的 Opt-in 页 nmsqus6s（suyen2027-caiyun-optin）和 guide 页 ljpbk7zh（suyen2027-caiyun-guide）不再有人进来，只是 funnel 里的步骤。
- make_raw.py：CONF_PAGE = 网域 /suyen2027-caiyun-vip；建法：`PDFZ=pdfz.json python3 make_raw.py ../optin.html lichun.json out.html suyen2027-caiyun-optin https://2027shengxiaocaifu.suyenlim.com/suyen2027-caiyun-vip suyen2027-caiyun`
- 2026-11-20：(NEW) 登记成功页 slug 改 `join` → https://2027shengxiaocaifu.suyenlim.com/join；VIP 页的「不用了，我先加入大会」原本写死主 funnel 的 suyen2027-join.aigoal.ai，已改成网域 /join；VIP 付款后转到网域 /suyen2027-caiyun-vipok。
- 2026-11-20：属虎 06 行动卡上线。Studio 两个版本都写成「更要能过度乐观」，我把「能」换成「防」（Noto Sans SC 400、54px，跟原字逐像素对齐），其余字跟 prompt 一致；PDF 也重拍。原图 photo-1794990990098。
- (NEW) 欢迎讯息 A_GATE 改成「你好 {name}👋 你的报名 【2027奇门战略大会】收到啦 ！🎉 …请点击下方「我会出席」…」，按钮「我会出席」。**WhatsApp 第一则要 Meta 审核模板**：API 改文字不会送审，要在 aigoal 漏斗编辑器「报名确认」那一步按保存/送审，审过前会发旧的预设模板。
- 2026-11-20：网域改挂 (NEW) 的 Opt-in（nmsqus6s，slug suyen2027-caiyun）→ aigoal 漏斗画面显示网域。流程：`/` 资料框 → 送出 → `/suyen2027-caiyun-guide`（选年份看指南，最后有 PDF）→ `/suyen2027-caiyun-vip` → `/join` 或 `/suyen2027-caiyun-vipok`。完整版指南 lf1skpvx 回到 suyen2027-caiyun-full（给 ?pdf=年份 下载用）。第 2 页补上属虎行动卡图片。
- 2026-11-20：PDF 最后的大会卡 QR（扫码参加奇门战略大会）+ 卡上「立即报名」连结 → https://2027qimenconference.suyenlim.com。
- 2026-11-20：PDF 加第 2 页＝赞助商（ABLE FARM 食油海报）：米色页、标题「特别鸣谢 · 赞助商」、海报 55% 宽置中（raw/sponsor/sponsor-page.jpg，pdfz.json 的 sponsor）。
- 2026-11-20：PDF 改成**现成档案**：98 个（每个出生年份 1 个，指南 + 赞助页）由 `build98.js` 用完整版指南的 ?pdf=年份 生成，上传到 WhatsApp bot（o1p8sl0r）的**档案库**（aigoal 只有这里收 PDF；从档案库删掉档案就会 404，所以要留着），标题「2027 生肖财运指南 · 属X · YYYY 年出生（PDF）」。网址表 `raw/pdf98-urls.json`。第 2 页按钮 = 直接下载该年份的档案（download 属性），不换页。**指南内容/图片/赞助页有改，要重跑 build98.js 再重传、换第 2 页连结。**

## 2026-11-20 定案 A（现行）
- 2027shengxiaocaifu.suyenlim.com `/` = 完整版指南 lf1skpvx（slug suyen2027-caiyun）：资料框 → 同一页显示「你是 X 年出生，生肖 属X」+ 指南 + PDF（页内直接下载，含赞助页）；报名进 (NEW) 的 Opt-in（landing:suyen2027-caiyun-optin），拿 ft → 立即报名 → /suyen2027-caiyun-vip → /join 或 /suyen2027-caiyun-vipok。
- (NEW) 漏斗画面的 Domain 卡会显示 Not set（网域挂在 lf1skpvx 上，这是唯一能做到「送出后同页直接看结果」的方式）。(NEW) 的 Opt-in（suyen2027-caiyun-optin）和第 2 页（suyen2027-caiyun-guide）没人会进去。
- 已证实 aigoal 漏斗页做不到的事：script / onerror 会被剥、meta refresh 被剥、frame-src 'none'、stage=draft 只是标签、下一页拿不到表单答案。
- 2026-11-20：VIP 页按付款钮 → 平台送 `initiate_checkout`（有 ft 就记在联系人活动里，`GET /api/crm/{id}/activity` 看得到），但 aigoal 联系人 Timeline 没有这个事件的标签所以不显示。变通：(NEW) 的 G1「弃单提醒」（立即发）加 beat tag `initiated_checkout` → 开了结账没付的人会被打上这个标签。(NEW) 的 G1–G3 弃单追单讯息是开着的（跟主 funnel 一样）。
- 2026-11-20：(NEW)=uvlroqgh 欢迎讯息 A 加 beat tag `lead_magnet_2027shengxiaocaifu` → 每个从生肖指南报名的人都会被打上（aigoal 没有「没有某标签」的条件，所以无法只限新客；看新客请在 CRM 筛 lead_magnet_2027shengxiaocaifu 且 没有 registered_webinar 的旧纪录 / 用建立日期）。
- 2026-11-20：IG「财运到」：bot o1p8sl0r 新增 au_cyd_comment（全部 IG 贴文、评论含「财运到」→ 公开回复 → DM 请先关注 @2027suyenlimconference 再回复「关注了」→ 10 分钟后、1 天后再提醒），au_cyd_send0/1（关键字「我已关注，发给我」/「关注了」→ 发指南连结 2027shengxiaocaifu.suyenlim.com + utm），au_cyd_tag0/1（同关键字 → tag got_caiyun_guide_ig）。aigoal 不保留没有网址的按钮，所以改成「回复关注了」。改前备份 backup-automation-2026-11-20/bots-before-caiyundao.json。
- 2026-11-20：标签 `lead_magnet_2027shengxiaocaifu` 改成**每次送出都贴**（不论新旧客）：新建表单页 s43bw0r7（slug suyen2027-caiyun-tag，「生肖财运指南 · 自动标签（勿删）」，form_tag=lead_magnet_2027shengxiaocaifu，不在任何漏斗、不发讯息），指南送出时多送一笔 register 到 landing:suyen2027-caiyun-tag。已用 Harvard 测试：标签有贴上。

## 2026-11-20 定案 A+（漏斗 Domain 卡显示 Set）
- 网域挂在漏斗 Opt-in nmsqus6s（slug suyen2027-caiyun-optin）→ 卡片显示网域。`/` = 介绍页（指南上半部 + 「看我的 2027 财运 →」，藏一个隐形 aigoal 表单避免平台塞预设表单）。
- 按钮 → `/suyen2027-caiyun#dobform` = 完整版指南 lf1skpvx（资料框 → 同页结果 + PDF；报名进漏斗 Opt-in + 标签页）→ 我会出席战略大会 → /suyen2027-caiyun-vip → /join 或 /suyen2027-caiyun-vipok。
- **完整版指南 lf1skpvx 必须保持 published**（之前在漏斗 Domain 卡按 Connect 会把它变成草稿，网站就挂）。
- 2026-11-20：指南表单改报名到**主 funnel**（FUNNEL_SLUG=suyen2027）：已在主 funnel 的人（registered_webinar）重复报名不会再收欢迎讯息（Harvard 06:12 后 9 次重复报名都没再发）；新客收主 funnel 的欢迎 + registered_webinar。标签页 suyen2027-caiyun-tag 照送（lead_magnet_2027shengxiaocaifu）。生肖 funnel 报名数会是 0。
- 2026-11-20：两段式。送出指南表单 → 只送 landing:suyen2027-caiyun-tag（贴 lead_magnet_2027shengxiaocaifu，存出生年份/生肖，不进漏斗、不发讯息）。按「我会出席战略大会」→ 才送 landing:suyen2027（主 funnel：registered_webinar + 欢迎讯息，已报名的不重发）→ 拿 ft 去 VIP。
- 2026-11-21：取消介绍页。网域改回完整版指南 lf1skpvx → 一打开就是资料框（漏斗 Domain 卡会显示 Not set，这是正常的，不要在那里按 Connect）。
- 2026-11-21：aigoal 新功能「skip if tag」（POST /api/landing/skip-if {id,tags,to}）：生肖 funnel VIP 页 oqcbkd0m 设 tags=[vip] → 转 https://2027shengxiaocaifu.suyenlim.com/join。需要网址带 ft（「我会出席」按钮会带）。另外 aigoal 也新增 after-submit（{id,to,pass}：表单送出后去哪、把哪些栏位带到下一页）。
- 2026-11-21：避免已报名的人重收欢迎讯息（主 funnel 重复报名会重发）。「我会出席战略大会」改送 landing:suyen2027-caiyun-attend（表单页 3uic2cl9，form_tag=registered_webinar，不在漏斗）。bot 规则 au_cyd_welcome：标签 registered_webinar「新贴上」时 → 发已核准模板 au1ushrl4_broadcast_zh（「你好 {name}，恭喜你，已经成功锁定…」+ 社群链接）；讯息步骤条件 has_tag lead_magnet_2027shengxiaocaifu（规则层条件对 label_added 会被存成 none，所以放在步骤上）。已有 registered_webinar 的人不会触发。代价：新报名者不在主 funnel，收不到主 funnel 之后的提醒。aigoal 现在也有「没有某个标签」条件（not_has_tag）。
- 2026-11-21：标签页 s43bw0r7 被删掉（API 回 bad secret）→ 重建 w8n2s0i4，同样 slug suyen2027-caiyun-tag、form_tag lead_magnet_2027shengxiaocaifu，标题加「删掉的话标签和欢迎讯息都会失效」。
- 2026-11-21：Google Sheet：标签页 w8n2s0i4 接「2027年奇门战略大会 Lead Magnet」（栏位 出生年份、生肖）；我会出席页 3uic2cl9 接主大会「Customer List」。VIP skip 用 Harvard 的 ft 测试会转去 /join，但按钮报名回 deduped 没 ft → 等 aigoal #7。
- 2026-11-21：VIP 页 oqcbkd0m 顶端加「已经是 VIP？👉 直接加入大会社群」→ /join（在 aigoal #7 上线前，VIP 一点就到社群页）。改前备份 backup-automation-2026-11-20/vip-page-before-banner.json。
- 2026-11-21：主 funnel VIP 页 4e411c3b（suyen2027-vip）也设 skip-if tags=[vip] → https://2027qimenconference.suyenlim.com/suyen2027-join。Harvard 的 ft 测试会转过去。同样受 aigoal #7 限制（已存在联系人报名没回 ft）。

## 2026-11-25 · Version 2（属鼠新版，独立页，不动 version 1）
- 新 raw 页 **hbmwuugd**，slug `suyen2027-caiyun-v2`：https://suyen2027-caiyun-v2.aigoal.ai ，也可走 https://2027shengxiaocaifu.suyenlim.com/suyen2027-caiyun-v2
- 内容 = 正式版（lf1skpvx）复制一份，只把属鼠那一段换成《1. Rat2027_Bilingual.docx》的内容（字不改）。其他 11 个生肖、表单、按钮跟 v1 一样（表单送出仍会真的贴标签）。
- 生成器：`rat-2027/build_mock.py` + `rat-2027/rt.css`；图片网址 `rat-2027/v2-img-urls.json`（p2/p3/rat 三张因 img_limit 直接嵌在 HTML 里）。
- version 1（lf1skpvx / 网域首页）完全没动。

## 2026-11-25 · version 1 更新（lf1skpvx）
- 「同样属X，财路不一样」中间加一行「YYYY 年的你，」：纯 CSS（跟年份卡一样用 #yN_YYYY:checked），没选年份时照旧两行。
- 每个生肖结果最下面（下载 PDF 下面）加「知道运势之后，下一步该怎么走？」战略大会区块（字照 Reagan 给的）。二维码 → https://2027qimenconference.suyenlim.com；二维码和「扫描二维码，立即报名」可点 = 我会出席（data-cta="whatsapp-attend"）。
- 上线前备份：scratchpad v1fix/backup-v1-before-1125.json。
- 印刷版 PDF：指南改回一整张长页，用 print/cap_year.js 按出生年份截（跟访客看到的一样）；后面接结语页。网站「下载 PDF」按钮还是旧截图（还没有新标题和下一步区块）。
- 2026-11-25：hero 奇门盘上面加 2027 八字表（9时 己巳 / 4日 甲寅 / Feb月 壬寅 / 2027年 丁未，HTML 做的），盘下面加「2027年的年度盘」。12 个生肖都有。
- 2026-11-25：hero 最上面加该生肖的玉雕照片（用「你的贵人」那张卡的上半部，CSS 背景裁切，没另外上传），下面八字表、奇门盘，三样同宽、同框。等 Reagan 给 iCloud 那份 PDF 的原图再换。
- 2026-11-25：玉雕生肖照拿掉（Reagan 不要这张）。等她给另外一张牛，放奇门盘下面。
- 2026-11-25：奇门盘 + 「2027年的年度盘」下面加该生肖的动物图（来自《2027丁未年12生肖 1岁到100岁》docx 的 image3、7–17，白底，裁成 1200×750，内嵌在 HTML 里）。原图存 zodiac-animals/za0–11.png（0=鼠…11=猪）。
- 2026-11-25：动物图改成透明背景（rembg isnet 抠图），去掉白卡框，只留淡阴影。透明原图 zodiac-animals/zt0–11.png。
- 2026-11-25：「下一步该怎么走」区块字放大：标题改成大标题（跟各段 h2 一样，后半句红色），问题、「真假混」那句、大会名、落实、日期、五大层面、结尾句都放大。字没改。
- 2026-11-25：**98 个年份完整版 PDF 上线**（封面、关于、前言、指南长页、结语、服务、Follow us、2 页赞助）。`print/all.sh` 生成，手机版（约 3.5 MB）上传到 bot 档案库，网址表 `raw/pdf98-book-urls.json`（旧的 `pdf98-urls.json` 档案还留着没删）。
  - 指南页 lf1skpvx「下载 PDF」按钮：`window.PDFBOOK[年份]` 直接下载完整版，同页不跳。
  - 漏斗第 2 页 ljpbk7zh：98 个下载连结全部换成新档。
  - 每年用哪组赞助：`print/pairs-98.txt`。
  - 上线前备份：scratchpad v1fix/backup-g-before-book.json、backup-p2-before-book.json。
