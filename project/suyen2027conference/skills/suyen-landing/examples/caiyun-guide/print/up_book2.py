import json,subprocess,os,urllib.parse,glob
S='/tmp/claude-0/-home-user-video-editor/047dda4a-83c9-547c-814b-a439d5ed871f/scratchpad'
os.chdir(S)
ys=json.load(open('pdf98/years.json')); ZOD='鼠牛虎兔龙蛇马羊猴鸡狗猪'
OUT='print/all2/urls.json'
out=json.load(open(OUT)) if os.path.exists(OUT) else {}
tok=open('.tok').read().strip()
for y in ys:
    if y in out: continue
    z=ZOD[(int(y)-4)%12]; f=f'print/all2/phone/2027生肖财运指南-属{z}-{y}-手机版.pdf'
    if not os.path.exists(f): print('missing',y); continue
    cap=f'2027 生肖财运指南 · 属{z} · {y} 年出生（完整版 PDF）'
    q=urllib.parse.urlencode({'kind':'auto','caption':cap})
    r=subprocess.run(['curl','-sS','-m','180','-X','POST',f'https://app.aigoal.ai/api/wa/bots/o1p8sl0r/asset/upload?{q}','-H',f'Authorization: Bearer {tok}','-H','x-impersonate-tenant: 6d4a02f6-2165-49da-bf8c-ab4434ca9d72','-H','content-type: application/pdf','--data-binary',f'@{f}'],capture_output=True,text=True)
    try:
        j=json.loads(r.stdout); a=j['asset']; out[y]={'id':a['id'],'u':a['url']}
    except Exception as e: print('FAIL',y,r.stdout[:200],r.stderr[:200]); continue
    json.dump(out,open(OUT,'w'))
print('uploaded',len(out),'of',len(ys))
