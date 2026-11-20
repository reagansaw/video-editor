# aigoal 需求：按钮 / 链接「点了就贴标签」（给 aigoal 开发）

> 来源：《玄学群英会》funnel（`grcg4e5g`，supremecommunity.suyenlim.com）2026-11-19 搭建时发现的平台限制。
> 页面都是 asis 导入、不能写 `<script>`，所以下面全部要在平台的 `aigoal-hooks` 运行时 + 后端做。

## 0. 要达成的 4 条规则

| # | 客人动作 | 要贴的标签 | 现在能不能 |
|---|---|---|---|
| 1 | VIP OTO 付款成功（Stripe 或 Xendit） | `vip` + 状态「成交 won」+ 金额 + 付款方式 | 标签 `vip` 有（pay offer 的 tag）；won / 金额 / 付款方式**没验证过** |
| 2 | 在 `/2027-qimen-conference` 点「我会出席」 | `attend_2027conference` | ❌ 不能 |
| 3 | 点《玄学群英会》WhatsApp Community 链接 | `joined_supremecommunity` | ⚠️ 只有带 `ft` 才贴（funnel community_tag） |
| 4 | 点 2027奇门战略大会 WhatsApp 社群链接 | `joined_2027conferencecommunity` | ❌ 一个 funnel 只有一个 community |

所有 WhatsApp 链接要保留 UTM。

## 1. 现在平台的行为（从 aigoal-hooks 读出来的）

- `a[data-cta]` 只认这几种：`next / order / addcal / community / magnet / pay / booking`。
- 只有 `data-cta="community"` 会走追踪链：有 `ft` 时改成 `/r/ft/community?s=<slug>&ft=<FT>`，后端贴 funnel 的 `community_tag` 再跳 `community_url`。**没有 ft 就直接跳原链接，不贴标签。**
- `C.next`（`__AIGOAL__.next`）**只有 funnel 第 1 页（opt-in）有值**，后面每一页都是空字符串 → 后面页的表单送出后不跳页，只显示「收到！」。
- 表单 `type="hidden"` 的栏位在前端被丢掉（`if(t==='hidden')return`），所以没办法用隐藏栏位带标签。
- `ft` 只在 `C.next` / `pay` 的链接上自动带（`withFt`）。页面里写死的 `href`（例：OTO 的「不用了」→ `/xuanxue-ok`）**不会带 ft**，下一页就认不出是谁。

## 2. 要做的改动

### 2.1 新的 CTA：`data-cta="go"` + `data-tag`（核心）

页面写法：

```html
<a data-cta="go" data-tag="attend_2027conference"
   href="https://supremecommunity.suyenlim.com/2027-qimen-conference-confirm">我会出席</a>

<a data-cta="go" data-tag="joined_2027conferencecommunity"
   href="https://chat.whatsapp.com/Ix6Y5Mkia0x1hPGSmExlTh?utm_source=supremecommunity&utm_medium=landing&utm_campaign=2027conference">加入 WhatsApp 社群</a>
```

**前端（aigoal-hooks）**：有 `FT` 且有 `C.slug` 时，把 href 改成

```
/r/ft/go?s=<C.slug>&ft=<FT>&i=<这颗按钮在页面里的序号>
```

- 没有 FT → href 不动（照样能跳，只是不贴标签）。
- 外部链接（chat.whatsapp.com、wa.me）照 community 的做法加 `target=_blank rel=noopener`。

**后端 `GET /r/ft/go`**：

1. 用 `s` 找到已发布的页面（同 tenant），用 `ft` 找到联系人。
2. **标签和目的地不要从网址读**（防止有人乱改网址替任何人贴标签 / 拿去当 open redirect）。页面存档时就把每颗 `data-cta="go"` 的 `{i, tag, href}` 解析出来存在 page 上（例：`page.go_ctas`），`/r/ft/go` 用 `i` 去查。
3. 联系人 + 标签都有 → 贴标签（重复点不重复贴）、journey 记一笔 `cta_click`（页面 slug、标签、时间），并且触发「贴上标签」的自动化链条（跟手动贴标签一样）。
4. `302` 跳到存好的 `href`。如果是本网站的页面，**把 ft 接在后面**（`?ft=`），下一页才认得人。
5. 找不到联系人 / ft 过期 → 不贴，照样 302 到 href（客人体验不能断）。

这一个功能就能同时解决规则 2、3、4（Community 链接也改用 `data-cta="go"`，每条链接自己的标签，UTM 原样保留）。

### 2.2 一路带着 ft

- **付款成功跳转**：Stripe 和 Xendit 付完跳回 offer 的 `redirect_url` 时都要带 `?ft=`（现在不确定有没有，要测两种）。
- **页面里写死的本站链接**：hooks 对 `href` 是同一个网域 / 同一个 funnel 页面的 `<a>`，自动补 `ft`（跟 `withFt` 一样）。至少 `data-cta="next"` 但 `C.next` 是空、所以留着写死 href 的那种要补。

### 2.3 （顺便）funnel 每一步都给 `C.next`

后端按 funnel steps 的顺序，每一页的 `C.next` = 下一步页面的网址（现在只有 opt-in 有）。这样后面页面的表单送出后也能跳页。

### 2.4 付款成功写进 CRM（规则 1）

付款 webhook（Stripe、Xendit 都要）成功后对联系人：

- 贴 offer 的 `tag`（`vip`）→ 触发「贴上标签」链条（VIP automation）
- `status = won`
- `purchase_amount` = 实收金额（含 SST，例 104.76），`purchase_date` = 付款时间
- 记下付款方式：`stripe` / `xendit`（+ 渠道，例 card / fpx / tng），放 journey 或新栏位 `purchase_provider`
- 同一个人付第二次：金额要累加还是覆盖，请定一个规则

### 2.5 Google Sheet 要看得到付款方式

现在 Sheet 的栏位只有固定 9 栏（`GET /api/landing/sheet/fields` 的 `base`：时间、姓名、电话、Email、来源、标签、状态、成交金额、成交日期）＋ 表单栏位，**没有付款方式可以选**，所以 Reagan 在 Sheet 看不到客人是用 Stripe 还是 Xendit 付的。

要加：
- `base` 多一栏 **「付款方式」**，值例：`Stripe · card`、`Xendit · FPX`、`Xendit · TNG`（从 2.4 的 `purchase_provider` 来）。最好再加 **「付款单号」**（Stripe PaymentIntent / Xendit invoice id），对账用。
- 付款成功时，**更新这个人在 Sheet 原本那一行**（用电话 / email 对到报名那行），填 状态 = 成交、成交金额、成交日期、付款方式；对不到才新增一行。
- 已经绑好的 Sheet（《玄学群英会》opt-in 页 `enk7ph4p` → 试算表「玄学群英会」）新栏位要能自动加到表头，不用重绑。

### 2.6 Google Sheet「参加奇门战略大会」栏

Reagan 要在 Sheet 看到谁报了 2027奇门战略大会。规则：**付了 OTO（贴 `vip`）或在 `/2027-qimen-conference` 点「我会出席」（贴 `attend_2027conference`）= 参加**。

- `base` 多一栏 **「参加奇门战略大会」**，值 `是` / 空白。
- 最好做成通用的：Sheet 设定里可以加「标签栏」——选一个或几个标签（这里是 `vip`、`attend_2027conference`），联系人有其中一个就写 `是`。之后别的活动也能用。
- 联系人**之后**才贴上标签（付款、点按钮都是报名之后的事），要回头**更新他原本那一行**，不是只在报名当下写一次。`标签` 栏也一样要跟着更新（现在不确定会不会）。

## 3. 验收（用 supremecommunity.suyenlim.com 真机跑一次）

1. 填 `/` 的表单 → 跳到 `/vip-2027-vwi3?ft=…`。
2. 点「不用了」→ `/xuanxue-ok?ft=…`（网址要带 ft）。点「加入 Community」→ CRM 出现 `joined_supremecommunity`，WhatsApp 打开的链接带 UTM。
3. 另一个号：在 OTO 用 FPX（Xendit）付 → 回到 `/2027-qimen-conference?ft=…`；CRM：`vip`、won、104.76、xendit/fpx。再用卡（Stripe）测一次。
4. 在 `/2027-qimen-conference` 点「我会出席」→ 到 `/2027-qimen-conference-confirm?ft=…`；CRM 有 `attend_2027conference`，journey 有 `cta_click`。
5. 在 confirm 页点「加入 WhatsApp 社群」→ CRM 有 `joined_2027conferencecommunity`，链接带 UTM。
6. 把网址里的 `i` 改成别的数字 / 拿掉 ft 再点 → 不能贴到不该贴的标签，页面照样能跳。
7. 「贴上标签」链条（例：`vip` → VIP automation）有被触发。
8. 第 3 步那两笔付款：Google Sheet「玄学群英会」同一个人那一行出现 成交 / 104.76 / 付款日期 / 「Xendit · FPX」和「Stripe · card」。
9. 第 3、4 步的人：Sheet 同一行「参加奇门战略大会」= 是；只填了第 1 步、没付也没点的人 = 空白。

## 4. 平台做好之后，页面这边要改的（我来改）

- `/2027-qimen-conference`：7 颗「我会出席」加 `data-cta="go" data-tag="attend_2027conference"`。
- `/2027-qimen-conference-confirm`：2027 社群链接加 `data-cta="go" data-tag="joined_2027conferencecommunity"`。
- `/xuanxue-ok`：3 颗 Community 按钮改成 `data-cta="go" data-tag="joined_supremecommunity"`（或保留现在的 funnel community_tag）。
- OTO 的「不用了」链接：确认有带 ft。
