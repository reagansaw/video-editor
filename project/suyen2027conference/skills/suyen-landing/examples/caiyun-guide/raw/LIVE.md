# 2027 生肖财运指南 · 上线记录（2026-11-18）

| 网址 | aigoal page id | 是什么 |
|---|---|---|
| https://suyen2027-caiyun.aigoal.ai | lf1skpvx | **正式版**（raw，含出生年份表单、PDF 下载） = `index-prod.html` |
| https://suyen2027-caiyun-v1.aigoal.ai | nsdxd10s | 旧 asis 版，**仍挂在 funnel pbme0shf 的 optin**；正式版的报名都送到这个 slug，自动化照常跑 |
| https://suyen2027-caiyun-test.aigoal.ai | lk70bgy3 | 测试版（报名送到自己，不跑 funnel） |
| https://suyen2027-caiyun-ok.aigoal.ai | x6xiwtve | 报名成功页 |

旧版原始码备份：`backup-suyen2027-caiyun-asis.json`。
重建正式版：`python3 make_raw.py ../optin.html lichun.json out.html suyen2027-caiyun-v1 https://suyen2027-caiyun-ok.aigoal.ai suyen2027-caiyun`，再把图片 src 换成 `img-urls.json` 里的 /avatars 网址。
