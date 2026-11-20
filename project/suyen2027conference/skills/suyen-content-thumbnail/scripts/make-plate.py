#!/usr/bin/env python3
"""把样板海报的字擦掉，做成「无字底图」（plate）。只给本 skill 用。
用法：python3 -I scripts/make-plate.py <样板图> <输出.png> <区域 json>
区域 json：{"poly":[[x,y],...], "boxes":[[x0,y0,x1,y1],...], "person_x":480, "fade_top":[y0,y1]}
  poly/boxes = 要擦掉的地方（字、红条、底线、贴纸）；person_x 右边的深色（头发）不擦也不拿来补；
  fade_top = 擦掉区上缘用多长的渐层接回原图（避免硬切）。需要 opencv-python-headless。
"""
import sys, json, cv2, numpy as np
src, dst, spec = sys.argv[1], sys.argv[2], json.load(open(sys.argv[3]))
im = cv2.imread(src).astype(np.float32); H, W = im.shape[:2]
m = np.zeros((H, W), np.uint8)
if spec.get("poly"): cv2.fillPoly(m, [np.array(spec["poly"], np.int32)], 255)
for x0, y0, x1, y1 in spec.get("boxes", []): m[y0:y1, x0:x1] = 255
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV)
hair = np.zeros_like(m); px = spec.get("person_x", W)
hair[:, px:] = (hsv[:, px:, 2] < 80).astype(np.uint8) * 255
hair = cv2.dilate(hair, np.ones((9, 9), np.uint8))
m_inp = cv2.bitwise_or(m, hair)                     # 头发不当补色来源
m_out = cv2.bitwise_and(m, cv2.bitwise_not(hair))   # 头发保留原图
k = 6
small = cv2.resize(im.astype(np.uint8), (W // k, H // k), interpolation=cv2.INTER_AREA)
ms = cv2.dilate(cv2.resize(m_inp, (W // k, H // k), interpolation=cv2.INTER_NEAREST), np.ones((3, 3), np.uint8))
fill = cv2.GaussianBlur(cv2.inpaint(small, ms, 8, cv2.INPAINT_TELEA), (0, 0), 3)
fill = cv2.resize(fill, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32)
fill += np.random.default_rng(1).normal(0, 1.6, fill.shape)
a = cv2.GaussianBlur(m_out.astype(np.float32) / 255, (0, 0), 6)
if spec.get("fade_top"):
    y0, y1 = spec["fade_top"]; ramp = np.clip((np.arange(H) - y0) / max(1, y1 - y0), 0, 1)[:, None]
    a = np.where(np.arange(H)[:, None] < y1, np.maximum(a * ramp, 0) , a)
    a[: y1] = np.maximum(a[: y1], ((m_out[: y1] > 0) * ramp[: y1]))
out = im * (1 - a[..., None]) + fill * a[..., None]
cv2.imwrite(dst, np.clip(out, 0, 255).astype(np.uint8))
print("✓", dst)
