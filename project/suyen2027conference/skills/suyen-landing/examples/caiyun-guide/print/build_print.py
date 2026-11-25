import os
"""Print PDF per birth year: Master Book p1-3 → guide → p74-75 → 特别鸣谢 (random sponsor pair)."""
import sys, json, random, io
from PIL import Image
from pypdf import PdfReader, PdfWriter, Transformation, PageObject
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

S='/tmp/claude-0/-home-user-video-editor/047dda4a-83c9-547c-814b-a439d5ed871f/scratchpad'
A='/home/user/video-editor/project/suyen2027conference/skills/suyen-landing/examples/caiyun-guide/print-assets'
ABLE='/root/.claude/uploads/047dda4a-83c9-547c-814b-a439d5ed871f/d9878629-FINAL_POSTER_A2_ABLE_FARM_SOFT_OIL.pdf'
ADS={'ALCP':A+'/ALCP Ad (Right Side) (2).pdf','Golden Palm Tree':A+'/Golden Palm Tree.pdf','SSF':A+'/SSF ChineseMagazine_185x255mm(3mmBleed+5mm) (1).pdf',
     'ABLE':ABLE,'KLH':A+'/KLH BOOK V2 (2).pdf','Tayago':A+'/Tayago （cover）.pdf','Bharu':A+'/Bahru Stainless Advertisement MISIF latest 3 (1).pdf'}
PAIRS=[('ALCP','Golden Palm Tree'),('SSF','ABLE'),('KLH','Tayago'),('SSF','Bharu')]
PW,PH=420,595   # A5, same as Master Book
CREAM=(251/255,244/255,232/255)
QYBG=(1,246/255,238/255)
pdfmetrics.registerFont(TTFont('H700',S+'/sponsor/h700.ttf'))

def guide_page(year):
    """one long page = the guide exactly as that birth year sees it on the site"""
    zy=S+f'/print/zy/{year}.jpg'
    if os.path.exists(zy):
        from reportlab.lib.utils import ImageReader
        im=Image.open(zy).convert('RGB'); h_pt=PW*im.size[1]/im.size[0]
        b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,h_pt)); cv.drawImage(ImageReader(zy),0,0,PW,h_pt); cv.showPage(); cv.save(); b.seek(0)
        return [PdfReader(b).pages[0]]
    return guide_page_old(year)

def guide_page_old(year):
    zi=(year-4)%12; P=S+'/print/z'
    meta={}
    for f in ('meta.json','meta-part.json'):
        if os.path.exists(P+'/'+f): meta.update(json.load(open(P+'/'+f)))
    if str(zi) in meta:
        g=dict(meta[str(zi)]); im=Image.open(P+f'/z{zi}.jpg').convert('RGB')
    else:
        g=json.load(open(S+'/pdfz.json'))[str(zi)]; im=Image.open(S+f'/pdfz/z{zi}.jpg').convert('RGB')
    g['w']=im.size[0]; k=g['w']/g['W']
    card=g['cards'][str(year)]
    parts=[(0,g['top']),tuple(card),(g['bottom'],g['H'])]
    crops=[im.crop((0,int(a*k),g['w'],int(b*k))) for a,b in parts]
    conf=Image.open(S+'/pdfz/conf2.jpg').convert('RGB'); crops.append(conf.resize((g['w'],int(conf.size[1]*g['w']/conf.size[0]))))
    H=sum(c.size[1] for c in crops); out=Image.new('RGB',(g['w'],H),(251,244,232)); y=0
    for c in crops: out.paste(c,(0,y)); y+=c.size[1]
    cuts=[]
    sp=P+'/sections.json'
    if os.path.exists(sp):
        sec=json.load(open(sp)).get(str(zi),{}).get('tags',[])
        h0=int(g['top']*k); hc=int(card[1]*k)-int(card[0]*k)
        for tag,t in sec:
            if not tag.startswith('SECTION'): continue
            if t<=g['top']: cuts.append(int(t*k))
            elif t>=g['bottom']: cuts.append(h0+hc+int((t-g['bottom'])*k))
    cuts.append(H-crops[-1].size[1])   # conference card starts a page
    return split_a5(out,cuts=sorted(cuts))

def split_a5(out, top_pt=22, bot_pt=30, cuts=()):
    """cut the long guide into A5 pages at blank rows between sections"""
    import numpy as np
    from reportlab.lib.utils import ImageReader
    W,H=out.size; k=W/PW; avail=int((PH-top_pt-bot_pt)*k)
    a=np.asarray(out.convert('L')).astype(np.int16)
    blank=(a.max(1)-a.min(1)<10)          # rows with no content
    pages=[]; y=0
    while y<H:
        # skip leading blank rows
        while y<H and blank[y]: y+=1
        if y>=H: break
        end=min(H,y+avail)
        if end<H:
            # blank runs inside the window; prefer the lowest big gap (between sections)
            runs=[]; r=y+int(avail*.3)
            while r<end:
                if blank[r]:
                    q=r
                    while q<H and blank[q]: q+=1
                    runs.append((r,q)); r=q
                else: r+=1
            runs=[(p,q) for p,q in runs if p<end]
            big=[(p,q) for p,q in runs if q-p>=95]
            sc=[c for c in cuts if y+int(avail*.3)<c<=end]
            if sc: end=sc[-1]-2; runs=[]
            pick=None if sc else ([(p,q) for p,q in runs if q-p>=6] or [None])[-1]
            if pick and not sc: end=min((pick[0]+pick[1])//2, end) if pick[1]>end else (pick[0]+pick[1])//2
        sl=out.crop((0,y,W,end)); y=end
        b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH)); cv.setFillColorRGB(*CREAM); cv.rect(0,0,PW,PH,fill=1,stroke=0)
        jb=io.BytesIO(); sl.save(jb,'JPEG',quality=88); jb.seek(0); hp=sl.size[1]/k
        cv.drawImage(ImageReader(jb),0,PH-top_pt-hp,PW,hp); cv.showPage(); cv.save(); b.seek(0)
        pages.append(PdfReader(b).pages[0])
    return pages

def sponsor_page(name, first):
    # cream A5 with header, ad placed vector-scaled below
    b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH)); cv.setFillColorRGB(*CREAM); cv.rect(0,0,PW,PH,fill=1,stroke=0)
    cv.setFillColorRGB(184/255,50/255,74/255); cv.setFont('H700',15)
    cv.drawCentredString(PW/2,PH-30,'特别鸣谢 · 赞助商'); cv.showPage(); cv.save(); b.seek(0)
    base=PdfReader(b).pages[0]
    ad=PdfReader(ADS[name]).pages[0]; aw,ah=float(ad.mediabox.width),float(ad.mediabox.height)
    top=46; box_w,box_h=PW-28,PH-top-34
    sc=min(box_w/aw,box_h/ah); x=(PW-aw*sc)/2; yb=(PH-top-ah*sc)
    yb=34+(box_h-ah*sc)/2
    base.merge_transformed_page(ad,Transformation().scale(sc).translate(x-float(ad.mediabox.left)*sc,yb-float(ad.mediabox.bottom)*sc))
    return base


def jieyu_page(m):
    """结语: 前言 page design, header + body replaced"""
    jy=S+'/print/qy/jy.pdf'
    if not os.path.exists(jy): return None
    w=PdfWriter(); w.append(m,pages=[2]); pg=w.pages[0]
    b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH))
    cv.setFillColorRGB(187/255,38/255,73/255); cv.rect(22,PH-96,140,72,stroke=0,fill=1)   # old 前言/FOREWORDS
    cv.setFillColorRGB(*QYBG); cv.rect(36,PH-570,370,456,stroke=0,fill=1)                   # old body + signature
    cv.rect(384,4,30,26,stroke=0,fill=1)                                                    # old page number 3
    cv.showPage(); cv.save(); b.seek(0)
    pg.merge_page(PdfReader(b).pages[0]); pg.merge_page(PdfReader(jy).pages[0])
    return pg

def build(year,out,pair=None):
    pair=pair or random.Random(year).choice(PAIRS)
    m=PdfReader(A+'/master-pages.pdf'); w=PdfWriter()
    fp=A+'/front-pages.pdf'   # new 目录/关于/前言 version, pages 1-3
    f=PdfReader(fp) if os.path.exists(fp) else m
    cov=A+'/cover-2027.jpg'   # new page 1 (2027 十二生肖运势锦囊 cover)
    if os.path.exists(cov) and not os.path.exists(fp):
        b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH)); cv.drawImage(cov,0,0,PW,PH); cv.showPage(); cv.save(); b.seek(0)
        w.add_page(PdfReader(b).pages[0]); first=1
    else: first=0
    for i in range(first,3):
        pg=f.pages[i]
        qy=S+'/print/qy/qy.pdf'
        if i==2 and f is m and os.path.exists(qy):   # 前言 rewritten for 2027 丁未年
            b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH)); cv.setFillColorRGB(*QYBG)
            cv.rect(40,PH-499,365,380,stroke=0,fill=1); cv.showPage(); cv.save(); b.seek(0)
            pg.merge_page(PdfReader(b).pages[0]); pg.merge_page(PdfReader(qy).pages[0])
        w.add_page(pg)
    for gp in guide_page(year): w.add_page(gp)
    jp=jieyu_page(m)
    if jp is not None: w.add_page(jp)   # 结语 after the guide
    for i in (3,4): w.add_page(m.pages[i])
    for j,n in enumerate(pair): w.add_page(sponsor_page(n,j==0))
    for n,pg in enumerate(w.pages,1):
        if n in (1,2,3): continue   # cover: no number; Master Book pages already carry 2, 3
        pw,ph=float(pg.mediabox.width),float(pg.mediabox.height)
        b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(pw,ph))
        cx,cy,r=pw-22,16.5,5.6
        if n==1: cv.setFillColorRGB(*CREAM)
        else: cv.setFillColorRGB(184/255,50/255,74/255)
        cv.circle(cx,cy,r,stroke=0,fill=1)
        cv.setFillColorRGB(*((184/255,50/255,74/255) if n==1 else (1,1,1))); cv.setFont('Helvetica-Bold',6.2)
        cv.drawCentredString(cx,cy-2.2,str(n)); cv.showPage(); cv.save(); b.seek(0)
        pg.merge_page(PdfReader(b).pages[0])
    w.compress_identical_objects() if hasattr(w,'compress_identical_objects') else None
    with open(out,'wb') as f: w.write(f)
    return pair

if __name__=='__main__':
    y=int(sys.argv[1]); print(build(y,sys.argv[2]))
