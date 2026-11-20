import re
src=open('rawsite/prod-live.html').read()
h=re.sub(r'<script\b[^>]*>.*?</script>','',src,flags=re.S)
i=h.find('<div id="signup" class="modal"'); j=h.find('<footer',i); h=h[:i]+h[j:]
CONF='<a class="btn" href="https://suyen2027-caiyun-dahui.aigoal.ai/" data-cta="whatsapp-attend">'
# turn every 立即报名 link into a submit button for the box form
n=0
def sub(m):
    global n; n+=1
    cls=re.search(r'class="([^"]*)"',m.group(1)).group(1)
    return f'<button type="submit" form="dobform" class="{cls}">{m.group(2)}</button>'
h=re.sub(r'<a ([^>]*href="https://suyen2027-caiyun-dahui\.aigoal\.ai/"[^>]*)>(.*?)</a>',sub,h,flags=re.S)
# box: aigoal sign-up form, no own button
h=h.replace('<form class="dob" id="dobform" novalidate>','<form class="dob" id="dobform" data-aigoal-lead>')
h=h.replace('<input id="dob-name" name="name"','<input id="dob-name" name="name" required')
h=h.replace('<input id="dob-email" name="email" type="email"','<input id="dob-email" name="email" type="email" required')
h=h.replace('<input id="dob-phone" name="phone" type="tel"','<input id="dob-phone" name="phone" type="tel" required pattern="\\+?[0-9 -]{9,18}"')
h=h.replace('<select id="dob-y" autocomplete="bday-year">','<select id="dob-y" name="birth_year" data-label="出生年份" autocomplete="bday-year" required>')
b=h.find('<button type="submit" class="btn" id="dob-go" disabled>'); e=h.find('</button>',b)+9
h=h[:b]+'<p class="dob-hint">填好 4 项，你的 2027 指南会马上出现在下面 ↓</p>'+h[e:]
cards=dict((y,int(z)) for z,y in re.findall(r'class="yc yc(\d+)_(\d{4})"',h))
ok='body:has(#dobform:valid)'
rules=[f'{ok}:has(#dob-y option[value="{y}"]:checked) #read .rd{z},{ok}:has(#dob-y option[value="{y}"]:checked) #read .yc{z}_{y},{ok}:has(#dob-y option[value="{y}"]:checked) #read .yd{z}{{display:block!important}}' for y,z in cards.items()]
css=('<style>/* NEW funnel opt-in: guide appears under the box once valid; 立即报名 submits the box */'
 '#read .rd{display:none}#read .yc{display:none}#read .ychips,#read .back,#dob-err,#dobres,.pdfwrap{display:none!important}'
 '.dob-hint{margin:14px 0 0;font-weight:700;color:var(--crimson-600,#B8324A)}'
 f'{ok} .dob-hint{{color:#2E7D4F}}'
 'button.btn{font:inherit;cursor:pointer;border:0}\n'+'\n'.join(rules)+
 f'\n{ok} .after,{ok} .mbar{{display:block!important}}</style>')
h=h.replace('</head>',css+'</head>',1)
open('fnl/new-optin-v3.html','w').write(h)
print('size',len(h),'submit buttons',n,'years',len(cards),'leftover dahui links',h.count('caiyun-dahui'))
