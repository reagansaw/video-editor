import re,sys
src=open('rawsite/prod-live.html').read()
def strip_scripts(h): return re.sub(r'<script\b[^>]*>.*?</script>','',h,flags=re.S)
def cut(h,a,b):
    i=h.find(a); j=h.find(b,i); assert i>=0 and j>i,(a,b); return h[:i]+h[j:]
def drop_modal(h):
    i=h.find('<div id="signup" class="modal"'); j=h.find('<footer',i); assert i>0 and j>i; return h[:i]+h[j:]
CONF='href="https://suyen2027-caiyun-dahui.aigoal.ai/" data-cta="whatsapp-attend"'
base=strip_scripts(src)
assert base.count(CONF)>=20, base.count(CONF)
# ---------- STEP 1: opt-in with the box as aigoal's sign-up form ----------
s1=base
s1=cut(s1,'<div id="read">','<div class="after">')
s1=drop_modal(s1)
s1=s1.replace(CONF,'href="#dobform"')
s1=s1.replace('<form class="dob" id="dobform" novalidate>','<form class="dob" id="dobform" data-aigoal-lead>')
s1=s1.replace('<input id="dob-name" name="name"','<input id="dob-name" name="name" required')
s1=s1.replace('<input id="dob-email" name="email" type="email"','<input id="dob-email" name="email" type="email" required')
s1=s1.replace('<input id="dob-phone" name="phone" type="tel"','<input id="dob-phone" name="phone" type="tel" required pattern="\\+?[0-9 -]{9,18}"')
s1=s1.replace('<select id="dob-y" autocomplete="bday-year">','<select id="dob-y" name="birth_year" data-label="出生年份" autocomplete="bday-year" required>')
s1=s1.replace('<button type="submit" class="btn" id="dob-go" disabled>','<button type="submit" class="btn" id="dob-go">')
css1='<style>/* NEW funnel step 1 */#dobform:has(:invalid) #dob-go{opacity:.45;pointer-events:none;filter:grayscale(.4)}.after{display:block!important}.mbar{display:none!important}#dob-err,#dobres{display:none!important}</style>'
s1=s1.replace('</head>',css1+'</head>',1)
for t in ('data-aigoal-lead','required pattern','name="birth_year"'): assert t in s1,t
open('fnl/new-step1.html','w').write(s1)
# ---------- STEP 2: year dropdown opens the guide ----------
s2=base
i=s2.find('<form class="dob" id="dobform"'); j=s2.find('</form>',i)+7
years=re.findall(r'<option value="(\d{4})">',s2[i:j])
cards=dict((y,int(z)) for z,y in re.findall(r'class="yc yc(\d+)_(\d{4})"',s2))
opts=''.join(f'<option value="{y}">{y}</option>' for y in years if y in cards)
box=('<div class="dob" id="yrbox"><b>打开你的 2027 求财指南</b><p>选你的出生年份，马上看到你的生肖指南，和你那一年出生的求财路线。</p>'
     '<div class="dob-row"><label for="yr">出生年份<select id="yr" data-aigoal-select><option value="" selected>选你的出生年份</option>'+opts+'</select></label></div>'
     '<p class="fine2">选好后往下看 ↓</p></div>')
s2=s2[:i]+box+s2[j:]
s2=drop_modal(s2)
s2=s2.replace(CONF,'href="#" data-cta="order"')
rules=[]
for y,z in cards.items():
    sel=f'body:has(#yr option[value="{y}"]:checked)'
    rules.append(f'{sel} #read .rd{z},{sel} #read .yc{z}_{y},{sel} #read .yd{z}{{display:block!important}}')
any_='body:has(#yr option:checked:not([value=""]))'
css2=('<style>/* NEW funnel step 2: year → guide, no scripts */#read .rd{display:none}#read .yc{display:none}#read .ychips{display:none!important}#read .back{display:none!important}'
      +'\n'.join(rules)+f'\n{any_} .after,{any_} .mbar{{display:block!important}}</style>')
s2=s2.replace('</head>',css2+'</head>',1)
open('fnl/new-step2.html','w').write(s2)
print('step1',len(s1),'step2',len(s2),'years',len(cards),'order buttons',s2.count('data-cta="order"'),'step1 anchors',s1.count('href="#dobform"'))
