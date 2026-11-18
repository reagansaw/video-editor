"""Master Suyen · 2027 生肖财运指南 · 第 05 段「答应之前，先问清楚」配图（12 生肖各 1 张，图里没有字）
5 个问题留在网页上当真文字，图只做气氛。只搭画布，不 Run（Run 花 Reagan 的点数，他自己按）。
用法：python3 suyen_zodiac_check_build.py            新建
      python3 suyen_zodiac_check_build.py --update   原地改（已跑出的结果保留）"""
import json, sys
from studio_api import call

WORKFLOW_ID = 'b7aedd45-7340-4b98-b480-f1373f859a3b'   # 11-18 建好，之后用 --update
NAME = 'Suyen · 2027 生肖财运指南 · 05「答应之前，先问清楚」配图 ×12 · 20261118'

SUBJECT = ("A small, finely carved pale-jade {animal} figurine stands in the centre of a dark rosewood desk, as if quietly watching over a closed "
           "folder of contract papers tied with a crimson silk cord. Around it: a traditional brush pen resting on a jade brush rest, an unpressed "
           "red cinnabar seal beside an open seal-paste box, an antique wooden abacus slightly out of focus, and a small cup of tea with a thin wisp of steam. ")
FRAMING = ("Wide still-life shot at eye level with the desk, slightly left of centre, leaving calm empty space on the right third. "
           "Soft warm window light from the left with natural gentle shadows, shallow depth of field. ")
STYLE = ("Premium editorial photograph for a Chinese metaphysics strategy brand, refined, calm and trustworthy; the mood says: pause and check the "
         "terms before you agree. Colour palette strictly rose crimson #D03F58, deep wine #3B0F18, warm beige #EFDFB3 and soft cream #FAF5E6, "
         "with small touches of antique gold. Real photo texture, natural materials, not a 3D render. 16:9. "
         "No people, no hands, no faces. No text, no letters, no Chinese characters, no numbers, no logos, no watermark. No purple, no blue.")

ANIMALS = [('rat', '鼠'), ('ox', '牛'), ('tiger', '虎'), ('rabbit', '兔'), ('dragon', '龙'), ('snake', '蛇'),
           ('horse', '马'), ('goat', '羊'), ('monkey', '猴'), ('rooster', '鸡'), ('dog', '狗'), ('pig', '猪')]

NOTE = ("用法\n1. 每一行是一个生肖：左边是提示，右边按 Run 出图（16:9，2K）。\n2. 图里不要有字：5 个问题留在网页上当真文字。\n"
        "3. 出好的图下载，档名照 check_鼠.jpg … check_猪.jpg，交回给 Claude 放进落地页第 05 段。\n4. 只搭画布，Claude 不按 Run。")

# 方案 2：5 个问题直接写进图（GPT Image 2 写字最稳，但中文仍可能错字，先 Run 属鸡试一张，逐字检查）
CHECKS = {"鼠": [["人缘带来什么？","这是可跟进的客户机会，还是单纯的社交邀约？"],["是不是在漏小钱？","上个月我为类似事项一共花了多少钱？"],["合作分工清楚吗？","谁承诺、谁跟进、谁承担额外费用？"],["关键条件求证了吗？","我问过当事人，还是只听别人转述？"],["可以先做哪一步？","能否先约一次电话、发一份报价，或取消一个重复扣款？"]],"牛": [["为什么现在要变？","我解决的是真问题，还是被催着作决定？"],["一共会花多少？","定金、后续付款、运行和退出成本算清了吗？"],["收入能兑现吗？","预算是谁确认的？预计什么时候到账？"],["回款延误怎么办？","如果需要先垫钱，我能承受多少？"],["能否先小规模试做？","什么结果值得继续，什么情况应该暂停？"]],"虎": [["贵人能帮什么？","对方能做具体引荐、提供专业意见，还是只有口头鼓励？下一步由谁跟进？"],["权责对等吗？","谁能批预算、调人和确认验收？新增责任是否有相应的权限？"],["收入可兑现吗？","薪资调整何时确认？项目由谁付款，满足什么条件才结算？"],["扩大后接得住吗？","人手和交付会不会超负荷？收入未到账前，新增开销能撑多久？"],["成果留得下来吗？","这一笔做成后，哪些资源可以累积？哪些支出不必跟着增加？"]],"兔": [["有责也有权吗？","谁能拍板？我获准调配什么资源？"],["这笔收入算得清吗？","扣掉额外人手、时间与交付成本，还剩多少？"],["钱什么时候进来？","首款、验收与尾款有没有写清楚？"],["成果怎样留住？","是否有固定复盘日，以及可执行的留存安排？"],["执行会不会太赶？","设备、人员和时间是否足够？能否预留缓冲？"]],"龙": [["客户需求明确吗？","客户本人确认了吗？谁有决定权？"],["外出值得吗？","这次拜访要达成什么？如果没谈成，时间与费用是否可控？"],["谁负责交付？","客户找谁？变更范围时，谁确认费用与时间？"],["怎么算钱？","谁开单、谁收款、佣金或分账按什么条件结算？"],["口头约定有记录吗？","报价、分工和跟进日期，是否已发给各方确认？"]],"蛇": [["需求真实吗？","谁来买单？是否和对方确认过需求及预算？"],["值得出发吗？","此行要带回来什么？能否先用一次通话验证？"],["成本算过了吗？","交通、人手、时间和售后算进去，还剩多少？"],["合作有记录吗？","报价、责任、验收和付款节点是否写清楚？"],["节奏安全吗？","是否留了交通、休息和交付缓冲？"]],"马": [["机会是真的？","有没有明确需求？谁说了算？"],["资源真的到位？","预算、人手、权限，哪一项已经确认？"],["责任说清了？","谁负责交付？如果变更范围或延误，谁处理？"],["钱能兑现？","谁付钱、什么时候付、达到什么条件才付？"],["我接得住？","这件事会占用多少时间？如果成果比预期少，我能不能承受？"]],"羊": [["我为什么想变？","看到了真实需求，还是只想离开眼前的压力？"],["底盘稳吗？","现有收入、必要开支与待付款项列清楚了吗？"],["新方向有人买单吗？","我问过实际客户吗？能否先做一次小测试？"],["旧承诺怎么处理？","要交给谁？未完成的工作和款项怎么结？"],["什么时候再决定？","我用什么结果判断继续、暂停或调整？"]],"猴": [["推荐有根据吗？","介绍人亲自验证过，还是也只听别人说？"],["资源能用吗？","人手、预算、渠道何时到位，有谁负责？"],["收入真到账了吗？","我核对过自己的收款记录，还是只看了截图？"],["我替谁承担风险？","有没有借名、代付、垫款、担保或不清楚的分账？"],["能先验证一小步吗？","哪些条件还没证实？能否用一次小试单核对？"]],"鸡": [["学了可以用在哪里？","哪个真实任务能让我验证新能力？"],["旧规则还适用吗？","有没有新审批、交付或付款要求？"],["谁能帮我查漏？","哪个专业人士能指出我没注意到的条件？"],["承诺有没有写清楚？","范围、责任、验收、付款是否一致？"],["还有多少余地？","如果出现延迟或额外开支，项目还能按计划进行吗？"]],"狗": [["这是协助还是接手？","从何时开始，到哪里结束，谁对结果负责？"],["钱由谁承担？","谁先付、谁报销、何时结算、凭什么记录？"],["遇到分歧找谁？","谁是当事人，谁有权限确定处理方式？"],["旧问题能先解吗？","哪笔应收、哪份文件或哪项交接可以先完成？"],["试做有边界吗？","能否写清费用上限、交付范围和结束条件？"]],"猪": [["谁真正有决定权？","介绍人能牵线，谁能确认预算和签约？"],["客户需要什么？","我问过当事人，还是只听了转述？"],["责任落在谁身上？","谁交付、谁验收、谁处理变更？"],["钱怎么结？","由谁收款？分账按成交还是到账计算？"],["有什么不能对外说？","客户资料、价格、内部消息，哪些必须保密？"]]}

def card_prompt(en, zh):
    lines = ''.join(f'第 {i+1} 行：玫红小圆圈里写数字「{i+1}」，旁边粗体大字写「{q}」，下面一行小一点的灰褐色字写「{d}」。' for i, (q, d) in enumerate(CHECKS[zh]))
    return ("一张直式 4:5 的高级资讯卡，给奇门战略品牌的落地页用。米白色 #FAF5E6 背景，干净、留白多、排版整齐。"
            f"最上面一行深酒红色 #3B0F18 粗体标题写「属{zh} · 答应之前，先问清楚」。标题右上角放一尊小小的浅玉雕{zh}，写实质感，不带任何字。"
            "标题下面是 5 张白色圆角卡片，从上到下排成一列，每张一行问题：" + lines +
            "数字圆圈用玫红 #D03F58，问题用深酒红 #3B0F18 粗黑体，说明用灰褐色 #5E4A4C 一般字重，全部是简体中文黑体，字要清楚好读。"
            "画面上只出现上面「」引号里的字，一字不差（包括里面的问号和逗号）；引号以外不要再加任何中文、英文、数字或标志。No watermark. No extra text. 4:5。")
# 收尾段「生肖，只是第一步」两个痛点（12 生肖共用 1 张）
CLOSE_POINTS = [('只看生肖，看不到全年的局', '生肖讲的是你个人的重点；大环境往哪里走、哪个月该推进，要放进全年趋势一起看。'),
                ('靠感觉拍板，一年都在补救', '一个看错的决定，往往要用一整年去绕路、补洞。')]

def close_prompt():
    rows = ''.join(f'第 {i+1} 张卡片：左边一个玫红 #D03F58 实心小圆圈，里面是白色的简单线条图标（第 1 张是一只眼睛，第 2 张是一个向下的箭头），圆圈里不要有字；'
                   f'右边粗体大字写「{q}」，下面一行小一点的灰褐色字写「{d}」。' for i, (q, d) in enumerate(CLOSE_POINTS))
    return ("一张正方形 1:1 的高级资讯卡，给奇门战略品牌的落地页用。米白色 #FAF5E6 背景，干净、留白多、排版整齐。"
            "画面里只有 2 张白色圆角卡片，从上到下排成一列，置中，卡片之间留一点空隙，每张卡片顶边有一条细细的玫红色线。" + rows +
            "问题用深酒红 #3B0F18 粗黑体，说明用灰褐色 #5E4A4C 一般字重，全部是简体中文黑体，字要清楚好读，说明可以自动换行。"
            "画面上只出现上面「」引号里的字，一字不差（包括里面的逗号、分号、顿号和句号）；引号以外不要再加任何中文、英文、数字、标题或标志。No watermark. No extra text. 1:1。")

# 06 行动卡（每个生肖内容不同，12 张）
ACTION = {"鼠": {"kw": ["人缘旺", "财易漏", "守边界"], "money": "主动见客户，经营销售、服务和专业转介，把接触变成明确的需求或报价。", "people": "留意愿意帮忙协调、给具体建议，或把你介绍给真实客户的人。", "go": "2月段打开人脉，3月段增加曝光，4月段主动求助，8月段重启有基础的项目。", "care": "6月段管好支出，7月段少介入纠纷，10月段把重要沟通和条款写清楚。"}, "牛": {"kw": ["主动变", "防大耗", "破旧局"], "money": "用已有专业争取有清楚职责的岗位或项目；保留稳定收入，再验证新的经营方式。", "people": "留意能看出成本漏洞、帮助重整流程或提供专业意见的人。", "go": "2月段接触新领域，8月段重谈合作或找资源，9月段用专业争取机会。", "care": "4月段谨慎处理大额支出；7月段重大决定留后路；10月段核对合同；11月段把注意力放回现金流。"}, "虎": {"kw": ["贵人起", "权位升", "防盛转衰"], "money": "有机会通过升职、争取重点项目或提高专业服务价值带动收入。谈职责时，也把待遇及评估标准谈清楚。", "people": "留意愿意给你机会、位置、资讯或关键建议的上司、行业前辈和专业人士。", "go": "5月段适合留意谈薪资、价格和项目回报；9月段虽仍有机会，更要防过度乐观。流月以节气交接为参考。", "care": "有财要积，有赚要留。增加固定支出之前，先看看新增收入是否能持续。"}, "兔": {"kw": ["掌权", "聚财", "防伤"], "money": "争取与新职责相称的薪资、服务价格或项目费用；先说清楚权责和考核标准。", "people": "遇到卡点，可留意能解决流程问题、给清晰反馈或提供专业协助的人。", "go": "3月段展现专业，4月段整理储蓄与资产，7月段整合资源，12月段盘点成果。", "care": "5月段少赶行程，10月段把合同与分工谈清楚。流月以节气交接为参考。"}, "龙": {"kw": ["走出去", "贵人扶", "防口舌"], "money": "通过出差、跨区服务、接触新客户或拓展线上业务，增加工作与生意的收入来源。", "people": "留意愿意分享可靠资讯、引荐关键客户，或在遇到难题时提供实际协助的人。", "go": "5月段可关注出差、客户拜访和跨区合作；8月段可留意新市场与事业连接。流月以节气交接为参考。", "care": "9月段尤其注意口舌与利益纠纷。把报价、佣金、分账和责任写下来，避免各自理解。"}, "蛇": {"kw": ["动中求机", "贵人助力", "安全第一"], "money": "关注外地客户、跨区服务、新平台或新岗位；用可验证的专业能力争取更好的条件。", "people": "留意能介绍真实客户、指出市场门槛或给具体专业建议的人。", "go": "3月段展示专业，5月段考察新环境，8月段关注外部收入，10月段谈项目或合作方式。", "care": "6月段谈判别硬碰硬；9月段行程与安全优先。不要为了赶进度，跳过成本、付款和交付核对。"}, "马": {"kw": ["贵人合", "财禄进", "养精蓄锐"], "money": "整理工作成果，争取与贡献相称的待遇；做生意的人，可检视服务定价与稳定收入。", "people": "留意愿意引荐客户、补足你的能力，或能和你一起完成交付的人。", "go": "未月值得留意合作进展。节气月与公历月份并不完全重合。", "care": "有人介绍，不等于已经成交；收入有增长，也别急着把开销和承诺一起加上去。"}, "羊": {"kw": ["本命重整", "守住自己", "先稳后进"], "money": "把现有专长做深，优先稳住已经有客户、有交付经验的收入来源。", "people": "可请有实务经验、能指出方案盲点的人帮你检视选择；最后自己做判断。", "go": "4月段学习与沉淀，8月段整理现金流与债务，10月段集中资源，12月段复盘成果。", "care": "7月段是本命月，先观察变化，别急着承诺大笔开支；9月段遇到合作误解及时沟通。"}, "猴": {"kw": ["贵人照", "喜事来", "防财劫"], "money": "让主管、客户或新平台看见你可验证的成绩，争取职责、客户或合作条件升级。", "people": "能给具体反馈、引荐决策者或帮你解决实际问题的主管、前辈、客户或专业人士。", "go": "3月段展示专业，4月段观察资源升级，8月段争取项目，10月段交付及收款。", "care": "5月段防虚假机会，7月段守住财务边界，12月段清理未收账款。"}, "鸡": {"kw": ["专业升级", "谨言守规", "先守后进"], "money": "把知识、资格或新技能用在一个实际任务上，用成果争取更好的岗位或服务价格。", "people": "能指出程序漏洞、复核关键文件，或让你看懂新行业要求的人。", "go": "2月段学习，3月段主动请教，8月段展示成果与谈价，11月段集中资源。", "care": "1月段整理文件；5月段仔细核对条款；7月段预留现金应对计划外开支；12月段收成果。"}, "狗": {"kw": ["关系考验", "破旧重整", "守界避争"], "money": "优先维护付款与交付稳定的工作或客户。接手新职责前，把范围、期限和报酬谈清楚。", "people": "留意细心务实的女性前辈、幕后决策者或财务人员；能帮你看清细节的人特别有价值。", "go": "3月段请教贵人，4月段处理旧账和旧合作，9月段寻求专业协助。", "care": "5月段核对合约与付款，7月段少争少冒险，8月段整理现金流和共同资金，12月段收尾。"}, "猪": {"kw": ["贵人聚", "福气升", "防是非"], "money": "关注职位、客户和专业价值带来的收入，主动争取更适合的平台或项目。", "people": "找愿意介绍合适客户、给具体建议，或能让你接触到决策者的人。", "go": "3月段请教前辈，7月段整合人脉，8月段把合作谈成收入，10月段争取事业进阶。", "care": "要小心文件和手续出错；也要少传话、多求证，防人在背后说闲话。5月段查文件，9月段守边界。"}}

def action_prompt(en, zh):
    a = ACTION[zh]
    kws = '、'.join(f'「{k}」' for k in a['kw'])
    secs = [('今年的财，往这里找', a['money']), ('我要主动接近的人', a['people']), ('主动出手的时段', a['go']), ('要仔细的地方', a['care'])]
    rows = ''.join(f'第 {i+1} 段：玫红色粗体小标题写「{t}」，下面深色一般字重写「{v}」。' for i, (t, v) in enumerate(secs))
    return ("一张直式 4:5 的高级行动卡，像一张精致的米黄色卡片，给奇门战略品牌的落地页用。卡片底色是暖米黄 #FFFAEB，四周有细细的金褐色边框和圆角，"
            "放在更浅的米白 #FAF5E6 背景上，有柔和阴影。卡片里面排版整齐、留白多、左对齐：\n"
            "最上面一行小小的玫红 #D03F58 粗体英文字母，字距拉开，写「2027 · MY ACTION CARD」。"
            f"下面一行深酒红 #3B0F18 粗体大标题写「属{zh}的我，先落实这一步」。"
            f"接着玫红色粗体小标题写「我的 2027 关键词」，下面是 3 个米黄色 #EFDFB3 的圆角胶囊标签，标签里深酒红粗体字分别写 {kws}。"
            "然后用细细的金褐色虚线把下面 4 段分开，" + rows +
            f"卡片右上角放一尊小小的浅玉雕{zh}，写实质感，不带任何字。"
            "中文全部是简体黑体，字要清楚好读，长句可以自动换行。"
            "画面上只出现上面「」引号里的字，一字不差（包括里面的逗号、顿号、句号和数字）；引号以外不要再加任何中文、英文、数字或标志。No watermark. No extra text. 4:5。")

NOTE2 = ("方案 2：5 个问题直接写进图\n1. 先只 Run「属鸡 · 文字卡」一张（约 1 点）。\n2. 出图后逐字对：标题 + 5 个问题 + 5 行说明，错一个字就重 Run。\n"
         "3. 鸡对了再 Run 其他 11 张。档名照 card_鼠.jpg … card_猪.jpg 交回给 Claude。\n4. Claude 只搭画布，不按 Run。")

OUTH = {'aiImage': 'result', 'aiVideo': 'result', 'fileUpload': 'output'}

def build():
    nodes, edges, types = [], [], {}
    def node(i, t, x, y, label, config, w=None, h=None):
        n = {'id': i, 'type': t, 'position': {'x': x, 'y': y}, 'data': {'label': label, 'config': config}}
        if w: n['width'] = w; n['height'] = h; n['style'] = {'width': w, 'height': h}
        nodes.append(n); types[i] = t
    def edge(src, tgt, th):
        edges.append({'id': f'e_{src}_{tgt}_{th}', 'source': src, 'sourceHandle': OUTH.get(types.get(src)), 'target': tgt,
                      'targetHandle': th, 'type': 'deletable'})
    node('note', 'stickyNote', 0, -420, '使用说明', {'text': NOTE}, 820, 300)
    for k, (en, zh) in enumerate(ANIMALS):
        y = k * 420
        node(f'{en}_txt', 'textInput', 0, y, f'{zh} · 05 配图提示',
             {'text': SUBJECT.format(animal=en) + FRAMING + STYLE})
        node(f'{en}_img', 'aiImage', 420, y, f'属{zh} · 答应之前，先问清楚',
             {'model': 'gpt-image-2', 'gptImage2Mode': 't2i', 'imageInputCount': 0, 'aspectRatio': '16:9', 'resolution': '2K',
              'gptImage2Quality': 'high', 'status': 'idle'})
        edge(f'{en}_txt', f'{en}_img', 'prompt')
    node('note2', 'stickyNote', 1100, -420, '方案 2 · 字写进图', {'text': NOTE2}, 820, 300)
    for k, (en, zh) in enumerate(ANIMALS):
        y = k * 420
        node(f'{en}_card_txt', 'textInput', 1100, y, f'{zh} · 文字卡提示（5 个问题写进图）', {'text': card_prompt(en, zh)})
        node(f'{en}_card', 'aiImage', 1520, y, f'属{zh} · 文字卡（4:5）',
             {'model': 'gpt-image-2', 'gptImage2Mode': 't2i', 'imageInputCount': 0, 'aspectRatio': '4:5', 'resolution': '2K',
              'gptImage2Quality': 'high', 'status': 'idle'})
        edge(f'{en}_card_txt', f'{en}_card', 'prompt')
    y = len(ANIMALS) * 420 + 120
    node('close_txt', 'textInput', 1100, y, '收尾段 · 两个痛点 · 文字卡提示', {'text': close_prompt()})
    node('close_card', 'aiImage', 1520, y, '收尾段 · 只看生肖 / 靠感觉拍板（1:1，12 生肖共用）',
         {'model': 'gpt-image-2', 'gptImage2Mode': 't2i', 'imageInputCount': 0, 'aspectRatio': '1:1', 'resolution': '2K',
          'gptImage2Quality': 'high', 'status': 'idle'})
    edge('close_txt', 'close_card', 'prompt')
    for k, (en, zh) in enumerate(ANIMALS):
        y = k * 420
        node(f'{en}_act_txt', 'textInput', 2200, y, f'{zh} · 06 行动卡提示', {'text': action_prompt(en, zh)})
        node(f'{en}_act', 'aiImage', 2620, y, f'属{zh} · 06 行动卡（4:5）',
             {'model': 'gpt-image-2', 'gptImage2Mode': 't2i', 'imageInputCount': 0, 'aspectRatio': '4:5', 'resolution': '2K',
              'gptImage2Quality': 'high', 'status': 'idle'})
        edge(f'{en}_act_txt', f'{en}_act', 'prompt')
    return nodes, edges

if __name__ == '__main__':
    nodes, edges = build()
    wid = WORKFLOW_ID if '--update' in sys.argv else None
    if wid:
        cur = call('get_workflow', workflow_id=wid); cur = cur.get('workflow', cur)
        old = {n['id']: n for n in cur['nodes']}
        if any(n['data']['config'].get('status') == 'running' for n in old.values()) and '--force' not in sys.argv:
            sys.exit('还在跑，等跑完再改')
        for n in nodes:
            o = old.get(n['id']); oc = o['data']['config'] if o else {}
            if o and (oc.get('resultUrl') or oc.get('historyId') or oc.get('status') == 'running'):
                n['data']['config'] = oc; n['position'] = o.get('position', n['position'])
    res = call('save_workflow', **({'workflow_id': wid} if wid else {}), name=NAME, nodes=nodes, edges=edges)
    print(json.dumps({k: v for k, v in res.items() if k in ('workflow_id', 'created', 'edit_url', 'node_count', 'edge_count', 'error', 'body')}, ensure_ascii=False))
    if 'workflow_id' in res:
        v = call('validate_workflow', workflow_id=res['workflow_id'])
        print('ready_to_run', v.get('ready_to_run'), 'errors', v.get('validation', {}).get('errors'), 'warnings', v.get('validation', {}).get('warnings'))
