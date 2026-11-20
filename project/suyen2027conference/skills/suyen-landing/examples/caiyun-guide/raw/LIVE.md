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
