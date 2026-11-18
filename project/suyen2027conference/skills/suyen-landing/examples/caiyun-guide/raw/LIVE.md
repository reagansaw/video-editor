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
