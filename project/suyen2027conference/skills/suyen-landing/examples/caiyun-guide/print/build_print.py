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
pdfmetrics.registerFont(TTFont('H700',S+'/sponsor/h700.ttf'))

def guide_page(year):
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
    b=io.BytesIO(); h_pt=PW*H/g['w']
    cv=canvas.Canvas(b,pagesize=(PW,h_pt)); 
    from reportlab.lib.utils import ImageReader
    jb=io.BytesIO(); out.save(jb,'JPEG',quality=88); jb.seek(0)
    cv.drawImage(ImageReader(jb),0,0,PW,h_pt); cv.showPage(); cv.save(); b.seek(0)
    return PdfReader(b).pages[0]

def sponsor_page(name, first):
    # cream A5 with header, ad placed vector-scaled below
    b=io.BytesIO(); cv=canvas.Canvas(b,pagesize=(PW,PH)); cv.setFillColorRGB(*CREAM); cv.rect(0,0,PW,PH,fill=1,stroke=0)
    cv.setFillColorRGB(184/255,50/255,74/255); cv.setFont('H700',15)
    cv.drawCentredString(PW/2,PH-30,'特别鸣谢 · 赞助商'); cv.showPage(); cv.save(); b.seek(0)
    base=PdfReader(b).pages[0]
    ad=PdfReader(ADS[name]).pages[0]; aw,ah=float(ad.mediabox.width),float(ad.mediabox.height)
    top=46; box_w,box_h=PW-28,PH-top-14
    sc=min(box_w/aw,box_h/ah); x=(PW-aw*sc)/2; yb=(PH-top-ah*sc)
    yb=14+(box_h-ah*sc)/2
    base.merge_transformed_page(ad,Transformation().scale(sc).translate(x-float(ad.mediabox.left)*sc,yb-float(ad.mediabox.bottom)*sc))
    return base

def build(year,out,pair=None):
    pair=pair or random.Random(year).choice(PAIRS)
    m=PdfReader(A+'/master-pages.pdf'); w=PdfWriter()
    for i in (0,1,2): w.add_page(m.pages[i])
    w.add_page(guide_page(year))
    for i in (3,4): w.add_page(m.pages[i])
    for j,n in enumerate(pair): w.add_page(sponsor_page(n,j==0))
    w.compress_identical_objects() if hasattr(w,'compress_identical_objects') else None
    with open(out,'wb') as f: w.write(f)
    return pair

if __name__=='__main__':
    y=int(sys.argv[1]); print(build(y,sys.argv[2]))
