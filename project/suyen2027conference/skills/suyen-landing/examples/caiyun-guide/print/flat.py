import pypdfium2 as pdfium, io, sys
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
src,dst=sys.argv[1],sys.argv[2]
d=pdfium.PdfDocument(src); cv=canvas.Canvas(dst)
for i in range(len(d)):
    pg=d[i]; w,h=pg.get_size(); sc=200/72
    if h>2000: sc=min(sc,14000/h)
    im=pg.render(scale=sc).to_pil().convert('RGB'); b=io.BytesIO(); im.save(b,'JPEG',quality=82); b.seek(0)
    cv.setPageSize((w,h)); cv.drawImage(ImageReader(b),0,0,w,h); cv.showPage()
cv.save()
