set -e
cd /tmp/claude-0/-home-user-video-editor/047dda4a-83c9-547c-814b-a439d5ed871f/scratchpad
YS=$(python3 -c "import json;print(' '.join(map(str,json.load(open('pdf98/years.json')))))")
nice -n 10 node print/cap_year.js $YS
cd print; mkdir -p all2/print all2/phone
ZN=(鼠 牛 虎 兔 龙 蛇 马 羊 猴 鸡 狗 猪)
for y in $YS; do z=$(( ((y-4)%12+12)%12 )); n="2027生肖财运指南-属${ZN[$z]}-$y"
  ONE_SPONSOR=1 python3 build_print.py $y "all2/print/$n.pdf" >> all2/pairs.txt && echo "$y" >> all2/pairs.txt
  python3 flat.py "all2/print/$n.pdf" "all2/phone/$n-手机版.pdf"
done
echo ALLDONE
