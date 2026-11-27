import json,re
S='/tmp/claude-0/-home-user-video-editor/047dda4a-83c9-547c-814b-a439d5ed871f/scratchpad/'
new=json.load(open(S+'print/all2/urls.json')); old=json.load(open(S+'print/all/urls.json'))
assert len(new)==98
g=json.load(open(S+'v1fix/g-src2.json')); h=g['html']
m=re.search(r'window\.PDFBOOK=(\{.*?\});</script>',h); assert m
h=h[:m.start(1)]+json.dumps({y:v['u'] for y,v in new.items()})+h[m.end(1):]
json.dump({'html':h,'updated':g['updated']},open(S+'v1fix/g-post2.json','w'),ensure_ascii=False)
open(S+'v1fix/v1-book2.html','w',encoding='utf8').write(h)
p=json.load(open(S+'v1fix/p2-src2.json')); t=p['html']; n=0
for y,v in old.items():
    if v['u'] in t: t=t.replace(v['u'],new[y]['u']); n+=1
json.dump({'html':t,'updated':p['updated']},open(S+'v1fix/p2-post2.json','w'),ensure_ascii=False)
print('guide PDFBOOK replaced; page2 links swapped',n)
