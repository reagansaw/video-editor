"""竖版内容片只贴「下 banner」（还没有首页海报时用；有海报改用 cover_banner.py）。
用法（repo 根目录）：python3 pipeline/add_banner.py <成片.mp4> <输出.mp4> [--phone]
- banner：remotion/public/suyenc/banner_bottom_2027.png（原图 2170×725 → 缩成 1080 宽 ≈ 361 高，贴最底；旧的 banner_bottom.webp 留着备份）
- 新 banner 比较高：任何贴底的元件（片尾「正能量」）要收在 y≤1540，banner 从 y1559 开始
- --phone：另外出手机版（crf 25、maxrate 6M）
"""
import argparse, os, subprocess
ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('out'); ap.add_argument('--phone', action='store_true')
a = ap.parse_args()
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
banner = f'{R}/remotion/public/suyenc/banner_bottom_2027.png'   # 2026-11-16 起广告和内容片一律用这张（2170×725 → 1080 宽 ≈ 361 高，盖住 y1559 以下）
fc = '[1]scale=1080:-2[b];[0][b]overlay=0:H-h:shortest=1[v]'
subprocess.run(['nice', '-n', '19', 'ffmpeg', '-nostdin', '-v', 'error', '-y', '-threads', '2', '-i', a.src, '-loop', '1', '-i', banner,
                '-filter_complex', fc, '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-crf', '20', '-preset', 'medium',
                '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', a.out], check=True)
print('done', a.out)
if a.phone:
    p = a.out.replace('.mp4', '-手机.mp4')
    subprocess.run(['nice', '-n', '19', 'ffmpeg', '-nostdin', '-v', 'error', '-y', '-threads', '2', '-i', a.out, '-c:v', 'libx264', '-crf', '25',
                    '-maxrate', '6M', '-bufsize', '12M', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', p], check=True)
    print('done', p)
