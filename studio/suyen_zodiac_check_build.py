"""Master Suyen · 2027 生肖财运指南 · 第 05 段「答应之前，先问清楚」配图（12 生肖各 1 张，图里没有字）
5 个问题留在网页上当真文字，图只做气氛。只搭画布，不 Run（Run 花 Reagan 的点数，他自己按）。
用法：python3 suyen_zodiac_check_build.py            新建
      python3 suyen_zodiac_check_build.py --update   原地改（已跑出的结果保留）"""
import json, sys
from studio_api import call

WORKFLOW_ID = None   # 第一次建好后把 workflow_id 填在这里，之后用 --update
NAME = 'Suyen · 2027 生肖财运指南 · 05「答应之前，先问清楚」配图 ×12 · 20261118'

STYLE = ("Premium editorial still life for a Chinese metaphysics strategy brand, refined and calm. Palette strictly: rose crimson #D03F58, "
         "deep wine #3B0F18, warm beige #EFDFB3 and soft cream #FAF5E6, with small touches of antique gold. Soft warm window light from the left, "
         "gentle shadows, shallow depth of field, photorealistic, high detail, clean uncluttered composition with calm empty space on the right third. "
         "No people, no hands, no faces, no text, no letters, no Chinese characters, no numbers, no logos, no watermark. No purple, no blue.")

SCENE = ("A wide still life on a dark rosewood desk: a closed folder of contract papers tied with a crimson silk cord, a traditional brush pen "
         "resting on a jade brush rest, an unpressed red cinnabar seal beside an open seal-paste box, an antique wooden abacus slightly out of focus, "
         "and a small cup of tea with a thin wisp of steam. In the centre of the desk stands a small, beautifully carved {animal} figurine in pale "
         "jade, as if quietly watching over the papers. The mood: pause and check the terms carefully before agreeing. ")

ANIMALS = [('rat', '鼠'), ('ox', '牛'), ('tiger', '虎'), ('rabbit', '兔'), ('dragon', '龙'), ('snake', '蛇'),
           ('horse', '马'), ('goat', '羊'), ('monkey', '猴'), ('rooster', '鸡'), ('dog', '狗'), ('pig', '猪')]

NOTE = ("用法\n1. 每一行是一个生肖：左边是提示，右边按 Run 出图（16:9，2K）。\n2. 图里不要有字：5 个问题留在网页上当真文字。\n"
        "3. 出好的图下载，档名照 check_鼠.jpg … check_猪.jpg，交回给 Claude 放进落地页第 05 段。\n4. 只搭画布，Claude 不按 Run。")

OUTH = {'aiImage': 'result', 'aiVideo': 'result', 'fileUpload': 'output'}

def build():
    nodes, edges, types = [], [], {}
    def node(i, t, x, y, label, config, w=None, h=None):
        n = {'id': i, 'type': t, 'position': {'x': x, 'y': y}, 'data': {'label': label, 'config': config}}
        if w: n['width'] = w; n['height'] = h; n['style'] = {'width': w, 'height': h}
        nodes.append(n); types[i] = t
    def edge(src, tgt, th):
        edges.append({'id': f'e_{src}_{tgt}_{th}', 'source': src, 'sourceHandle': OUTH.get(types.get(src)), 'target': tgt,
                      'targetHandle': th, 'type': 'deletable'})
    node('note', 'stickyNote', 0, -420, '使用说明', {'text': NOTE}, 820, 300)
    for k, (en, zh) in enumerate(ANIMALS):
        y = k * 420
        node(f'{en}_txt', 'textInput', 0, y, f'{zh} · 05 配图提示',
             {'text': 'A wide 16:9 image. ' + SCENE.format(animal=en) + STYLE})
        node(f'{en}_img', 'aiImage', 420, y, f'属{zh} · 答应之前，先问清楚',
             {'model': 'gpt-image-2', 'gptImage2Mode': 't2i', 'imageInputCount': 0, 'aspectRatio': '16:9', 'resolution': '2K',
              'gptImage2Quality': 'high', 'status': 'idle'})
        edge(f'{en}_txt', f'{en}_img', 'prompt')
    return nodes, edges

if __name__ == '__main__':
    nodes, edges = build()
    wid = WORKFLOW_ID if '--update' in sys.argv else None
    if wid:
        cur = call('get_workflow', workflow_id=wid); cur = cur.get('workflow', cur)
        old = {n['id']: n for n in cur['nodes']}
        if any(n['data']['config'].get('status') == 'running' for n in old.values()) and '--force' not in sys.argv:
            sys.exit('还在跑，等跑完再改')
        for n in nodes:
            o = old.get(n['id']); oc = o['data']['config'] if o else {}
            if o and (oc.get('resultUrl') or oc.get('historyId') or oc.get('status') == 'running'):
                n['data']['config'] = oc; n['position'] = o.get('position', n['position'])
    res = call('save_workflow', **({'workflow_id': wid} if wid else {}), name=NAME, nodes=nodes, edges=edges)
    print(json.dumps({k: v for k, v in res.items() if k in ('workflow_id', 'created', 'edit_url', 'node_count', 'edge_count', 'error', 'body')}, ensure_ascii=False))
    if 'workflow_id' in res:
        v = call('validate_workflow', workflow_id=res['workflow_id'])
        print('ready_to_run', v.get('ready_to_run'), 'errors', v.get('validation', {}).get('errors'), 'warnings', v.get('validation', {}).get('warnings'))
