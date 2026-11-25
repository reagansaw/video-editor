import re,html as H
src=open('rawsite/prod-live-c.html').read()
i=src.find('class="rd rd0'); i=src.rfind('<',0,i); j=src.find('class="rd rd1'); j=src.rfind('<',0,j)
old=src[i:j]
def cut(a,b):
    x=old.index(a); x=old.rfind('<section',0,x) if not a.startswith('<section') else x
    y=old.index(b,x); return old[x:y]
ydir=cut('id="z0-dir"','<section class="sec" id="z0-time"')
tail=old[old.index('<section class="close" id="z0-conf"'):]
IMG='/ratimg/'
def bi(cn,en,cls=''): return f'<p class="rt-cn {cls}">{cn}</p><p class="rt-en">{en}</p>'
def sec(id,no,lab,h,en,body): return f'''<section class="sec" id="z0-{id}"><p class="slab"><i>{no}</i>{lab}</p><h2 class="h2 rt-h2">{h}</h2><p class="rt-en rt-sub">{en}</p>{body}</section>'''
def h3(cn,en): return f'<h3 class="rt-h3">{cn}</h3><p class="rt-en">{en}</p>'
def rate(ic,cn,en,st): return f'<div class="rt-rate"><img src="{IMG}{ic}" alt=""><b>{cn} <small>{en}</small></b><span>{st}</span></div>'
hero=f'''<div class="prof rt-prof">
  <div>
    <p class="ey">2027 丁未年 · 十二生肖运势指南 / 2027 ZODIAC OUTLOOK</p>
    <h1 class="rt-h1">生肖鼠｜RAT</h1>
    <p class="rt-kw3">人缘旺 · 财易漏 · 守边界</p>
    <p class="rt-kw3en">Stronger Connections · Watch Money Leaks · Set Boundaries</p>
    <p class="hl">年度战略：守中求变，选对人、管好钱、养好身体。</p>
    <p class="rt-hlen">Annual strategy: Adapt carefully, choose your connections wisely, manage money and protect your wellbeing.</p>
  </div>
  <div class="rt-side">
    <div class="rt-rank"><b>8</b><div><span>年度排名第 8 名</span><small>RANKED NO. 8 IN 2027</small></div></div>
    <img class="rt-rat" src="{IMG}rat.jpg" alt="生肖鼠">
  </div>
</div>
<div class="wrap">
<div class="rt-rates">{rate('image13.png','事业','Career','★★★★☆')}{rate('image17.png','财富','Wealth','★★★☆☆')}{rate('image15.png','感情','Relationships','★★★★☆')}{rate('image18.png','健康','Health','★★☆☆☆')}</div>
<div class="rt-years"><p><b>出生年份</b> <small>Birth years</small></p><div>{''.join(f'<span>{y}</span>' for y in (1948,1960,1972,1984,1996,2008,2020))}</div>
<p class="rt-cn rt-s">年初出生者请核对生肖交界。</p><p class="rt-en">Confirm the zodiac year if born near its transition.</p></div>
'''
s1=sec('out','01','YEARLY OUTLOOK','年度总览｜人缘是机会，也是考验','Annual Outlook · Connections Bring Opportunity and Tests',
 f'''<div class="rt-3"><figure><img src="{IMG}p1.jpg" alt=""><figcaption><b>人脉与信任</b><small>Connections &amp; Trust</small></figcaption></figure><figure><img src="{IMG}p2.jpg" alt=""><figcaption><b>留意零碎开销</b><small>Watch Recurring Expenses</small></figcaption></figure><figure><img src="{IMG}p3.jpg" alt=""><figcaption><b>照顾身心</b><small>Care for Your Wellbeing</small></figcaption></figure></div>
 {h3('子未相害｜害太岁','Zi–Wei Harm · A Year to Manage Trust and Boundaries')}
 {bi('2027年生肖鼠排名第8，子未相害，传统上称为害太岁。此关系提醒人际信任、沟通误会与隐藏的矛盾，并不代表每件事都会不顺。','Rat ranks eighth in 2027. The Zi–Wei Harm is traditionally called Hai Tai Sui. It highlights trust, miscommunication and hidden tensions, rather than predicting inevitable misfortune.')}
 {bi('月德有贵人协助、问题缓解的象意；桃花代表魅力、人缘及客户缘。但小耗提醒零碎开销，六害提醒合作边界，死符提醒长期忽略的健康问题。','Yue De symbolises helpful support; Tao Hua relates to attraction, social connections and customer appeal. Xiao Hao highlights recurring expenses; Liu Hai, boundaries; and Si Fu, neglected wellbeing.')}
 <div class="rt-stars2"><div class="good"><img src="{IMG}image23.png" alt=""><small>吉星｜Auspicious Stars</small><b>月德 · 桃花</b><i>Yue De · Tao Hua</i></div><div class="bad"><img src="{IMG}image25.png" alt=""><small>凶星｜Cautionary Stars</small><b>小耗 · 死符 · 六害</b><i>Xiao Hao · Si Fu · Liu Hai</i></div></div>
 <div class="q rt-q"><p>舒苑老师提醒：有人缘，也要有边界；有人帮，也要懂得辨人。</p><p class="rt-en">Teacher Suyen’s reminder: Welcome connections, but maintain boundaries and good judgement.</p></div>''')
s2=sec('cw','02','CAREER &amp; WEALTH','事业与财富｜客户缘旺，更要堵住漏财','Career &amp; Wealth · Build Relationships, Stop Financial Leaks',
 f'''<div class="pt rt-pt">{h3('事业运 ★★★★☆｜机会来自人与人之间','Career ★★★★☆ · Opportunities Through People')}
 {bi('月德象征遇到问题时得到协助；桃花有助于人缘、曝光与客户关系。销售、服务、顾问、教育、美业及媒体从业者，可主动建立高质量的人脉。','Yue De represents help when challenges arise. Tao Hua symbolises visibility, rapport and client appeal. Sales, services, consulting, education, beauty and media professionals may benefit from purposeful networking.')}
 {bi('六害提醒：合作要写清楚责任、交付与利益分配，不要只凭口头承诺。','Liu Hai reminds you to document responsibilities, deliverables and profit sharing rather than rely on verbal promises.')}</div>
 <div class="pt rt-pt">{h3('财富运 ★★★☆☆｜小耗不是大亏，而是慢慢漏','Wealth ★★★☆☆ · Small Expenses Can Add Up')}
 {bi('社交、家庭、购物、订阅、信用卡及应酬开销，看似每笔不多，却可能持续侵蚀储蓄。每月检查自动扣款、现金流与预算。','Socialising, family costs, shopping, subscriptions and credit-card spending may quietly reduce savings. Review recurring charges, cash flow and your monthly budget.')}</div>
 <div class="q rt-q"><p>财富战略：小钱管得住，大钱才守得住。</p><p class="rt-en">Wealth strategy: Manage the small outflows so you can protect the larger gains.</p></div>''')
s3=sec('rh','03','RELATIONSHIPS &amp; HEALTH','感情与健康｜桃花要选，身体要顾','Relationships &amp; Health · Choose Carefully, Rest Regularly',
 f'''<div class="pt rt-pt">{h3('感情人际 ★★★★☆｜有吸引力，更要有界限','Relationships ★★★★☆ · Attraction Needs Boundaries')}
 {bi('桃花象征社交与感情机会。单身者可多认识新朋友，但不要急于投入；已有伴侣者应避免暧昧、第三者干扰或让旁人的意见主导关系。','Tao Hua suggests opportunities to meet people. Singles can broaden their circle without rushing commitment; couples should guard against ambiguity and outside interference.')}
 {bi('六害提醒把话说清楚，不让不满长期累积；月德象征愿意沟通时仍有转圜空间。','Liu Hai encourages clear communication rather than silent resentment; Yue De symbolises room for reconciliation.')}</div>
 <div class="pt rt-pt">{h3('健康运 ★★☆☆☆｜小问题不要一直拖','Health ★★☆☆☆ · Address Concerns Early')}
 {bi('死符在传统上提醒注意体力消耗、压力与长期忽视的小毛病，也应多关心家中长辈。睡眠与恢复需要优先安排；若有持续不适，应咨询正规医疗专业人士。','Si Fu is traditionally used as a prompt to pay attention to fatigue, stress and neglected symptoms, including the wellbeing of older family members. Prioritise sleep and seek qualified medical care for persistent concerns.')}</div>''')
months=[('01','JAN','稳住基础 • HEALTH &amp; FINANCES','先守住健康与财务，整理账务并减少不必要消费。','Review health and finances; reduce unnecessary spending.'),
('02','FEB','人脉打开 • RECONNECT','人脉开始打开；见客户、联络旧朋友，但别急着答应。','Reconnect with clients and friends; avoid rushed commitments.'),
('03','MAR','魅力提升 • SOCIAL APPEAL','桃花与人气提升；适合曝光及社交，关系先观察。','Social appeal grows; network while assessing trust carefully.'),
('04','APR','主动求助 • SEEK SUPPORT','月德解围：遇到难题主动请教前辈与专业人士。','Seek guidance from experienced people when challenges arise.'),
('05','MAY','养好身体 • REST &amp; RECOVERY','关注睡眠、精神疲劳与身体检查，不要长期透支。','Prioritise sleep, recovery and appropriate health checks.'),
('06','JUN','管好开销 • MANAGE SPENDING','财来财去：控制应酬、家庭与消费升级开销。','Monitor lifestyle, family and entertainment expenses.')]
s4=sec('mon','04','MONTHLY OUTLOOK','关键月份｜2027上半年','Monthly Highlights · January to June 2027',
 bi('以下月份重点依实体书整理，实际流月交界以节气为准。','Monthly themes follow the Chinese manuscript; exact transitions are based on the solar terms.')+
 '<ol class="rt-tl">'+''.join(f'<li><i><b>{n}</b><small>{m}</small></i><div><h4>{t}</h4><p>{c}</p><p class="rt-en">{e}</p></div></li>' for n,m,t,c,e in months)+'</ol>'+
 f'''<div class="q rt-q">{h3('上半年四个关键提醒','Four Key Reminders for the First Half')}<p>3月有人缘｜4月有解围｜5月顾健康｜6月管好钱。</p><p class="rt-en">March: connect · April: seek support · May: care for health · June: manage spending.</p></div>''')
def prod(img,name,qr): return f'<div class="rt-prod"><img class="ph" src="{IMG}{img}" alt="{name}"><b>{name}</b>'+(f'<img class="qr" src="{IMG}{qr}" alt="QR">' if qr else '<span class="qr none">二维码 待补</span>')+'</div>'
plan='''<svg class="rt-plan" viewBox="0 0 320 250" role="img" aria-label="平面图：北方大门"><rect x="20" y="34" width="280" height="196" rx="6" fill="#FFFDF7" stroke="#8E2438" stroke-width="3"/><path d="M20 120H140V34M140 120V170M200 230V150H300" fill="none" stroke="#8E2438" stroke-width="2"/><rect x="118" y="30" width="84" height="38" rx="6" fill="#F6DCE1" stroke="#C93B55" stroke-width="2" stroke-dasharray="5 4"/><rect x="140" y="30" width="40" height="8" fill="#FBF4E8"/><path d="M140 34a40 40 0 0 0 40 0" fill="none" stroke="#C93B55" stroke-width="2"/><text x="160" y="58" text-anchor="middle" font-size="11" font-weight="700" fill="#8E2438">北方 · 大门</text><circle cx="135" cy="84" r="5" fill="#A8782B"/><circle cx="160" cy="84" r="5" fill="#A8782B"/><circle cx="185" cy="84" r="5" fill="#A8782B"/><text x="160" y="104" text-anchor="middle" font-size="9.5" fill="#6b5a4e">镇元龙龟 · 九星乾卦 · 五黄柱</text><text x="160" y="22" text-anchor="middle" font-size="13" font-weight="900" fill="#C93B55">N 北</text><text x="160" y="246" text-anchor="middle" font-size="11" fill="#9a8a7c">S 南</text><text x="10" y="136" text-anchor="middle" font-size="11" fill="#9a8a7c">W</text><text x="311" y="136" text-anchor="middle" font-size="11" fill="#9a8a7c">E</text></svg>'''
s6=sec('fs','06','FENG SHUI','风水开运｜方位、生肖与幸运象征','Feng Shui · Directions, Zodiac Allies &amp; Lucky Symbols',
 f'''<div class="rt-fs"><p class="t">2027 流年风水提醒 / ANNUAL FENG SHUI</p><div><div><i>!</i><b>北方 · 五黄</b><small>NORTH · FIVE YELLOW</small><p>宜静 · 避免不必要的大型动土</p></div><div><i>!</i><b>西方 · 二黑、三煞</b><small>WEST · TWO BLACK &amp; THREE KILLINGS</small><p>谨慎评估装修与敲墙施工</p></div></div></div>
 {h3('2027年流年方位｜Annual Flying-Star Directions','North and West: Traditional Feng Shui Notes')}
 {bi('北方：2027年五黄位。传统上建议保持安静，避免不必要的大型动土、敲墙及装修。','North: The annual Five Yellow sector. Traditionally kept calm, avoiding unnecessary major renovations or drilling.')}
 {bi('西方：2027年二黑位，亦须留意三煞；大型施工应先审慎评估。','West: The annual Two Black sector, with the Three Killings also noted traditionally. Assess major works carefully.')}
 <h3 class="rt-h3 rt-big">北方：以稳为先，寓意守护</h3>{plan}
 <p class="rt-cn">2027年北方为五黄所在。本方案以“安定、守护、谨慎”为主题，将三件摆件作为趋吉避煞的象征，减少波折、稳住生活节奏的心愿。</p>
 <p class="rt-cn">属鼠的朋友可借此提醒自己：遇事先核实、行动留余地，不因一时急躁而打乱计划。</p>
 <p class="rt-cn"><b>布置方案：在北方摆放《镇元龙龟》，《九星乾卦》与《五黄柱》</b></p>
 <div class="rt-prods">{prod('image33.png','镇元龙龟',None)}{prod('image34.png','九星乾卦','image35.png')}{prod('image36.png','五黄柱','image37.png')}</div>
 <p class="note">**扫描二维码了解更多产品详情</p>
 <p class="rt-cn rt-tip">温馨提示：把三件摆件放在稳当、不容易被碰倒的地方，周围收拾干净，彼此留一点空位，不要挤在一起。属鼠的朋友应将这三件摆件放在北方。摆好之后，平时也要注意安全，做事多想一步、安排妥当。</p>
 {h3('三合、六合与相冲生肖','Zodiac Harmony and Clash')}
 <div class="rt-harm"><div><small>三合生肖</small><i>Three Harmony Allies:</i><span class="ic a"></span><b>猴、龙</b><i>Monkey and Dragon.</i><em>（申子辰三合）。</em></div><div><small>六合生肖</small><i>Six Harmony Ally:</i><span class="ic b"></span><b>牛</b><i>Ox.</i><em>（子丑六合）。</em></div><div class="x"><small>相冲生肖</small><i>Clashing Zodiac Sign:</i><span class="ic c"></span><b>马</b><i>Horse.</i><em>（子午相冲）。</em></div></div>
 {h3('幸运颜色与数字｜文化参考','Lucky Colours &amp; Numbers · Cultural References')}
 <div class="rt-lucky"><span><i style="background:#1F4E8C"></i><b>深蓝</b><small>Deep blue</small></span><span><i style="background:#141F3D"></i><b>海军蓝</b><small>Navy</small></span><span><i style="background:#17503F"></i><b>墨绿</b><small>Dark green</small></span><span class="n"><b>数字</b><small>Numbers</small><u>1</u><u class="g">6</u></span></div>
 <p class="note">源于传统五行象义，并非根据个人完整八字计算的专属结果。<br>These are general Five-Element associations, not personalised BaZi findings</p>''')
book=f'''<section class="sec" id="z0-book"><div class="rt-book"><img src="{IMG}book.png" alt="《2027年运势大破解》"><div>
<h3>2027丁未年三大关键字：「真、假、混」！</h3><p class="l">真假难辨，局势混乱，机会与风险交错！</p>
<ul><li>💥 2027年究竟会发生什么变化？</li><li>💰 下一波财富机会在哪里？</li><li>⚠️ 哪些风险值得提前防范？</li><li>🐎 哪些生肖有机会脱颖而出？</li><li>🏡 2027年居家风水又该如何布局？</li></ul>
<p class="a">📖 答案就在《2027年运势大破解》！</p><p>✨ 一本年刊，带你提前了解2027年世界趋势、十二生肖运势、十大天干日主、事业财富、九运风水及年度开运指南！</p>
<p class="pr">🎁 现在抢购，只需 <b>RM89</b>！</p><p>✅ 获得《2027年运势大破解》实体年刊一本<br>✅ 免费加赠《2027奇门遁甲战略大会》门票！</p></div></div></section>'''
acts=[('01','辨人｜建立高质量的连接','Choose Well · Build Meaningful Connections','p1.jpg','主动参加有价值的聚会、课程及行业交流；认识新朋友，也要核对人品、执行力和合作条款。','Attend worthwhile gatherings, classes and professional events. Meet people, but verify reliability, follow-through and terms.'),
('02','守财｜每月安排财务检查日','Protect · Set a Monthly Money Review','p2.jpg','检查信用卡、自动扣款、订阅、银行流水及不必要消费；对熟人借贷与合作金钱往来尤其要清楚。','Review credit cards, direct debits, subscriptions and bank statements. Keep loans and financial arrangements with friends transparent.'),
('03','养气｜规律休息，亲近自然','Restore · Rest and Spend Time Outdoors','p3.jpg','适当走进森林、公园与自然环境，减少持续消耗；出现身体不适时及时求医。','Take restorative walks in parks or nature, reduce prolonged stress and seek medical advice when needed.')]
qs=[('身边的人是在帮助我成长，还是持续消耗我？','Do my relationships support my growth or drain me?'),('我赚的钱去了哪里？有哪些支出可以停止？','Where does my money go, and what can I stop spending on?'),('哪些健康或关系问题，我已经发现却一直拖着？','Which health or relationship concerns have I postponed?')]
s7=sec('act','07','PRACTICAL GUIDE','三项开运行动｜辨人、守财、养气','Three Practical Actions · People, Money &amp; Wellbeing',
 ''.join(f'<div class="rt-act"><img src="{IMG}{p}" alt=""><div><h3 class="rt-h3">{n} {t}</h3><p class="rt-en">{n} · {te}</p><p class="rt-cn">{c}</p><p class="rt-en">{e}</p></div></div>' for n,t,te,p,c,e in acts)+
 h3('问自己三个问题','Three Questions for Your Year')+'<ol class="rt-qs">'+''.join(f'<li><b>{k+1}</b><div><p>{c}</p><p class="rt-en">{e}</p></div></li>' for k,(c,e) in enumerate(qs))+'</ol>'+
 f'''<div class="rt-bless">{h3('舒苑老师的祝福','A Closing Wish from Teacher Suyen')}<p class="w">愿你2027遇见对的人，远离消耗你的人；钱赚得到、福守得住，身体也有足够的能量走得更远。</p><p class="rt-en">May you meet the right people, protect your earnings and enjoy the energy and wellbeing to go further in 2027.</p><p class="rt-cn rt-s">个人运势仍须结合完整八字、大运、奇门布局与现实情况；更多内容参阅《2027年运势大破解》。</p><p class="rt-en">Personalised guidance requires a full BaZi chart, timing and real-life context. See 2027 Fortune Outlook for more.</p></div>''')
ydir=ydir.replace('<i>03</i>你的出生年份','<i>★</i>你的出生年份')
new='<div class="rd rd0">'+hero+s1+s2+s3+ydir+s4+s6+book+s7+tail
css=open('rat/rt.css').read()
out=src[:i]+new+src[j:]
out=out.replace('</head>','<style>'+css+'</style></head>',1)
open('rat/mock.html','w').write(out); print(len(new))
