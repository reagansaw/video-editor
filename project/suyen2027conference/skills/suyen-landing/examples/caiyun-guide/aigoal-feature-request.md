# 给 aigoal 团队的功能需求 · 2027 生肖财运指南（2026-11-21）

户口：2027 Master Suyen 战略大会
相关：漏斗「2027 Master Suyen 战略大会 · 报名」(ix2g7pr9)、「2027 生肖财运指南 · 林舒苑老师」(uvlroqgh)
网域：2027shengxiaocaifu.suyenlim.com（挂在 raw 页 suyen2027-caiyun）

## 1. 已经买 VIP 的人，不要再看到 VIP 升级页（最急）
**现况**：客户已付款（有 `vip` 标签、有 payment_received），再次报名或按「我会出席」，还是会进 VIP 升级页，看到 RM97 的升级推销。页面拿不到客户的标签或购买纪录，我们没办法在页面上判断。
**希望**（任一即可）：
- A. VIP / 销售页加一个设定：「已有标签 `vip`（或已买过这个 offer）的人，直接转去 ___ 页」（例如 /join 或 VIP 升级成功页）。
- B. `/api/track` 的 register 回应里，除了 `ft`，也回传这个联系人的标签（或 `is_vip` / `bought: [...]`），让页面自己导去对的页。

## 2. 欢迎讯息：已有某标签的人不要发
**现况**：漏斗的「报名确认」(A) 关不掉，也没有条件；已经有 `registered_webinar` 的人在另一个漏斗报名，会再收到一次欢迎讯息。
**希望**：漏斗每一步讯息可设「已有标签 X 就跳过」；或自动化条件加「没有标签 X」(目前只有 none / not_purchased / not_attended / has_tag)。

## 3. 漏斗页可以用 raw（可跑 script）的页面
**现况**：漏斗里的页一律剥掉 `<script>`、onload/onerror、meta refresh。我们的生肖指南要用 script 做「填表 → 同一页马上显示结果 + 下载 PDF」，所以只能放在漏斗外的 raw 页。
**希望**（任一即可）：
- 允许 raw 页当漏斗步骤（或「把现有页加进漏斗」）；
- 或表单送出后，把表单答案带到下一页（例如 `?birth_year=1985` 或可读取的 `{field}` 变数）。

## 4. 漏斗 Domain 卡可以接受挂在漏斗外页面的网域
**现况**：网域挂在 raw 页上，漏斗的 Domain 卡永远显示 Not set；在卡上按 Connect 会回 `cf_failed` / `domain_taken`，**而且会把原本挂网域的页变成草稿，整个网站掉线**（11-20 发生两次，要手动重新发布才恢复）。
**希望**：Connect 失败时不要动到原来的页；Domain 卡能显示「此网域已挂在本户口的 ___ 页」。

## 5. 联系人 Timeline 显示「开了结账」
**现况**：VIP 页按付款钮会记 `initiate_checkout`（`/api/crm/{id}/activity` 看得到），但 Timeline 没有这个事件的标签所以不显示。
**希望**：Timeline 显示「开始结账 · 2027 奇门战略大会 · VIP 升级 MYR 104.76」。

## 6. 其他
- 落地页可上传 PDF 档（目前只有 bot 档案库能放 PDF，删掉档案库项目档案就失效）。
- 11-21 10:26–10:29 所有落地页回「页面载入中…」(503)，请确认原因。

## 7. 重复报名也要回传 ft（让「skip if tag」对 VIP 生效）— 11-21 补充
谢谢上线 skip-if！我们已在 VIP 页（suyen2027-caiyun-vip）设定 tags=[vip] → /join。
**问题**：已经报名过的人再次报名，`/api/track` register 只回 `{"ok":true,"deduped":true}`，**没有 `ft`**。VIP 一定是已报名的人，所以他们到 VIP 页时网址没有 ft，`/r/ft/skip` 查不到人，skip 永远不会触发，VIP 还是看到升级推销。
**希望**：deduped 的 register 也回传这个联系人的 `ft`（例如 `{"ok":true,"deduped":true,"ft":"..."}`）。

## 8. 「表单送出后带资料到下一页」也要能带 name / phone / email — 11-21 补充
谢谢上线 after-submit（to + pass）！目前 `pass` 只带「其他栏位」(fields)，**name / phone / email 不会带**。我们要把网域挂在漏斗 Opt-in（Domain 卡显示 Set），送出后带去我们的指南页；指南页之后按「我会出席」要再报名（贴 registered_webinar），但拿不到 name/phone/email 就认不出是谁。
**希望**（任一即可）：
- A. `pass` 也可以选 `name` / `phone` / `email`；
- B. 或 `/api/track` register 接受只带 `ft`（用 ft 认人），不用再传 name/phone/email。（测试：只带 ft 送 register 回 ok，但没有记到联系人上）

## 9. VIP 页选 FPX / Touch 'n Go 付不到钱（11-26，急）
**现况**：VIP 页（suyen2027-caiyun-vip、suyen2027-vip）按付款 → 选「网上银行 FPX」或 TNG，网址没有 `ft` 的话，`/api/pay/checkout-session` 回 `409 need_contact`，弹窗只显示「没发出去，再试一次或直接 WhatsApp 我们」，客户付不了。信用卡（Stripe）没问题，因为 Stripe 自己收 email。
没有 ft 的人：重复报名的人（register deduped 不回 ft，见第 7 项）、从 WhatsApp / IG 直接点 VIP 连结进来的人。
**希望**：回 `need_contact` 时，弹窗不要直接报错，改成请客户填电话或 email（平台文字里已经有 `needContact`「请留电话或 email…」），带着再开 Xendit 付款单；或 checkout-session 接受 `phone` / `email` 栏位。
