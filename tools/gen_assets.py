# PJ116 资产生成器：生成 28 个主题(css/themes.css) + 36 张背景(bg/bgNN.svg) + js/catalog.js
# 运行：python tools/gen_assets.py   （全部原创生成，无版权问题；"参考"类只借鉴风格/配色思路，不复制对方素材）
import os, random, json, math
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def hx(c): c = c.lstrip('#'); return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))
def tohex(t): return '#%02x%02x%02x' % tuple(max(0, min(255, round(v))) for v in t)
def mix(a, b, t): A, B = hx(a), hx(b); return tohex(tuple(A[i] + (B[i] - A[i]) * t for i in range(3)))
def lum(c):
    def f(v): v /= 255; return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    r, g, b = hx(c); return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def cr(a, b): la, lb = lum(a), lum(b); hi, lo = max(la, lb), min(la, lb); return (hi + .05) / (lo + .05)
def ensure(fg, bg, target, toward):
    for i in range(40):
        if cr(fg, bg) >= target: return fg
        fg = mix(fg, toward, .06)
    return fg

# id, 名称, 分类, 类型(用=直接用/参=参考别人风格自己重做), 说明, bg, surface, text, brand, accent, dark
T = [
 ('办公蓝','商务科技','用','会议/办公/企业工具','#f4f7fb','#ffffff','#14233a','#1f6feb','#12a594',0),
 ('深海蓝','商务科技','用','稳重的企业后台','#eef3f8','#ffffff','#0b2540','#0b6bcb','#f59e0b',0),
 ('石墨灰','商务科技','用','中性、不抢内容','#f5f5f4','#ffffff','#1c1917','#44403c','#e11d48',0),
 ('暖米橙(参考 Weave)','商务科技','参','参考 workweave.dev：暖灰米底+深酒红字+橙色按钮；自己重新取色','#f4f2f0','#ffffff','#4a0f1c','#e8501f','#c9a86a',0),
 ('纸白蓝(参考 Vizcom)','商务科技','参','参考 vizcom.ai：纸白底+近黑字+蓝按钮+黑色圆角导航','#f7f4f1','#ffffff','#151515','#3b7ddd','#151515',0),
 ('浅灰深蓝(参考 Hunar)','商务科技','参','参考 hunar.ai：浅灰白底+深字+纯蓝按钮+彩色渐变卡片','#f9f9f8','#ffffff','#17181a','#0b5fe0','#6b4de6',0),
 ('午夜蓝','AI与技术','用','AI/开发者工具(深色)','#0e1424','#161e33','#e8edf9','#6ea8ff','#5eead4',1),
 ('霓虹紫','AI与技术','用','AI 产品感(深色)','#120d24','#1b1436','#efe9ff','#a78bfa','#f472b6',1),
 ('极客绿','AI与技术','用','终端/命令行风(深色)','#0b130e','#121d16','#e3f5e8','#4ade80','#fbbf24',1),
 ('冷光白','AI与技术','用','浅色 AI 工作台','#f6f8fb','#ffffff','#111827','#4f46e5','#06b6d4',0),
 ('森林绿','自然健康','用','健康/学习/户外','#f3f8f2','#ffffff','#17301f','#2b8a3e','#d9822b',0),
 ('薄荷','自然健康','用','清爽、医疗/健康','#effaf6','#ffffff','#0f2e27','#0f9f7a','#3b82f6',0),
 ('海岸','自然健康','用','旅行/海边','#eef7fb','#ffffff','#0b2f3f','#0b86b5','#f97316',0),
 ('沙漠','自然健康','用','暖沙色，温和','#faf4ea','#ffffff','#3a2a14','#b45309','#0f766e',0),
 ('日落橙','温暖创作','用','创作/娱乐/社区','#fff7f1','#ffffff','#3a1d12','#d9480f','#7048e8',0),
 ('玫瑰','温暖创作','用','生活方式/日记','#fff1f4','#ffffff','#3b1220','#d6336c','#7c3aed',0),
 ('蜂蜜黄','温暖创作','用','活泼、教育/儿童','#fffbea','#ffffff','#3a2f06','#b7791f','#2563eb',0),
 ('珊瑚','温暖创作','用','社交/轻松','#fff3f0','#ffffff','#3d1710','#e8590c','#0ca678',0),
 ('薰衣草','安静阅读','用','日记/冥想/阅读','#f7f5fc','#ffffff','#2a2145','#6741d9','#e64980',0),
 ('纸张米','安静阅读','用','长文阅读、博客','#f8f4ec','#fffdf8','#2b2418','#8b5e34','#2f6f6f',0),
 ('雾灰','安静阅读','用','文档/知识库','#f3f4f6','#ffffff','#1f2937','#374151','#2563eb',0),
 ('墨水黑白','安静阅读','用','极简、作品集','#ffffff','#fafafa','#0a0a0a','#0a0a0a','#e11d48',0),
 ('驼色时尚(参考 GANNI)','时尚电商','参','参考 ganni.com：白底+黑字+驼棕/豹纹色点缀，大图满铺','#ffffff','#f6f2ee','#111111','#111111','#9a5b2e',0),
 ('奶油粉','时尚电商','用','美妆/生活用品','#fff6f3','#ffffff','#3b1c1c','#be4b5f','#a16207',0),
 ('大地色','时尚电商','用','手作/有机','#f6f1ea','#ffffff','#2d2417','#6b4f2a','#3f6212',0),
 ('极简商店','时尚电商','用','纯黑白商品墙','#fcfcfc','#ffffff','#101010','#101010','#2563eb',0),
 ('深紫夜','深色','用','娱乐/游戏','#150f1f','#1f1630','#f0e9fb','#c084fc','#fb923c',1),
 ('炭黑橙','深色','用','工具/摄影','#141414','#1e1e1e','#f2f2f2','#fb923c','#38bdf8',1),
 ('日本红(参考 Japan Shorts)','内容媒体','参','参考 shorts.maysuns.uk：暖灰底+红色强调+橙色链接+深色大卡；自己重新取色','#f5f3f0','#ffffff','#1f1a1a','#c8102e','#f97316',0),
]

def build_themes():
    css = ['/* 自动生成：python tools/gen_assets.py ——  用 <html data-theme="tNN"> 切换；NN 即主题编号 */']
    cat = []
    for i, (name, group, kind, note, bg, sf, tx, br, ac, dark) in enumerate(T, 1):
        tid = 't%02d' % i
        tx = ensure(tx, bg, 7, '#000000' if not dark else '#ffffff')
        muted = ensure(mix(tx, bg, .38), bg, 4.5, tx)
        brand_txt = ensure(br, bg, 4.5, '#000000' if not dark else '#ffffff')   # 用作链接文字的品牌色
        ink = '#ffffff' if cr('#ffffff', br) >= cr('#0b0b0b', br) else '#0b0b0b'
        if cr(ink, br) < 4.5: br = ensure(br, ink, 4.5, '#000000' if ink == '#ffffff' else '#ffffff')
        s2 = mix(bg, tx, .06); line = mix(bg, tx, .16)
        hf = mix(bg, br, .20 if not dark else .35)
        css.append('[data-theme="%s"]{--bg:%s;--surface:%s;--surface-2:%s;--text:%s;--muted:%s;--line:%s;--brand:%s;--brand-text:%s;--brand-ink:%s;--accent:%s;--hero-from:%s;--hero-to:%s;color-scheme:%s}' %
                   (tid, bg, sf, s2, tx, muted, line, br, brand_txt, ink, ac, hf, bg, 'dark' if dark else 'light'))
        cat.append(dict(id=tid, n=i, name=name, group=group, kind=kind, note=note, bg=bg, surface=sf, text=tx, brand=br, accent=ac, dark=dark,
                        contrast=round(cr(tx, bg), 1)))
    open(os.path.join(ROOT, 'css', 'themes.css'), 'w', encoding='utf-8').write('\n'.join(css) + '\n')
    return cat

# ---------- 背景 ----------
W, H = 1920, 1080
def svg(body, defs=''): return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice"><defs>%s</defs>%s</svg>' % (W, H, defs, body)

def mesh(rnd, cols, base):
    d = '<filter id="b" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="120"/></filter>'
    b = '<rect width="%d" height="%d" fill="%s"/><g filter="url(#b)">' % (W, H, base)
    for _ in range(6): b += '<circle cx="%d" cy="%d" r="%d" fill="%s" opacity=".75"/>' % (rnd.randint(0, W), rnd.randint(0, H), rnd.randint(250, 480), rnd.choice(cols))
    return svg(b + '</g>', d)
def waves(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base)
    for k in range(4):
        y = H * (.5 + k * .13); a = rnd.randint(40, 110); p = ['M0 %d' % y]
        for x in range(0, W + 1, 160): p.append('L%d %d' % (x, y + math.sin(x / 260 + k + rnd.random()) * a))
        b += '<path d="%s L%d %d L0 %d Z" fill="%s" opacity=".55"/>' % (' '.join(p), W, H, H, cols[k % len(cols)])
    return svg(b)
def blobs(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base)
    for _ in range(5):
        cx, cy, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(150, 320); pts = []
        for a in range(0, 360, 45):
            rr = r * rnd.uniform(.7, 1.15); pts.append((cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))))
        d = 'M%.0f %.0f ' % pts[0] + ' '.join('Q%.0f %.0f %.0f %.0f' % (pts[i][0], pts[i][1], (pts[i][0] + pts[(i + 1) % 8][0]) / 2, (pts[i][1] + pts[(i + 1) % 8][1]) / 2) for i in range(8)) + 'Z'
        b += '<path d="%s" fill="%s" opacity=".5"/>' % (d, rnd.choice(cols))
    return svg(b)
def grid(rnd, cols, base):
    d = '<pattern id="p" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke="%s" stroke-opacity=".25"/></pattern><radialGradient id="r" cx="%.2f" cy="%.2f" r=".6"><stop offset="0" stop-color="%s" stop-opacity=".5"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (cols[0], rnd.random(), rnd.random() * .6, cols[1], cols[1])
    return svg('<rect width="%d" height="%d" fill="%s"/><rect width="%d" height="%d" fill="url(#p)"/><rect width="%d" height="%d" fill="url(#r)"/>' % (W, H, base, W, H, W, H), d)
def dots(rnd, cols, base):
    d = '<pattern id="p" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="2.2" fill="%s" fill-opacity=".45"/></pattern>' % cols[0]
    return svg('<rect width="%d" height="%d" fill="%s"/><rect width="%d" height="%d" fill="url(#p)"/><circle cx="%d" cy="%d" r="380" fill="%s" opacity=".18"/>' % (W, H, base, W, H, rnd.randint(300, 1600), rnd.randint(200, 800), cols[1]))
def stripes(rnd, cols, base):
    d = '<pattern id="p" width="60" height="60" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><rect width="30" height="60" fill="%s" fill-opacity=".14"/></pattern>' % cols[0]
    return svg('<rect width="%d" height="%d" fill="%s"/><rect width="%d" height="%d" fill="url(#p)"/>' % (W, H, base, W, H), d)
def topo(rnd, cols, base):
    cx, cy = rnd.randint(500, 1400), rnd.randint(300, 800); b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base)
    for k in range(1, 22): b += '<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-opacity=".28" stroke-width="2" transform="rotate(%d %d %d)"/>' % (cx, cy, k * 48, k * 30, cols[k % len(cols)], rnd.randint(-6, 6), cx, cy)
    return svg(b)
def circles(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base)
    for _ in range(14): b += '<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="%.2f"/>' % (rnd.randint(0, W), rnd.randint(0, H), rnd.randint(30, 220), rnd.choice(cols), rnd.uniform(.12, .4))
    return svg(b)
def tri(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base)
    for _ in range(16):
        x, y, s = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(80, 300)
        b += '<polygon points="%d,%d %d,%d %d,%d" fill="%s" opacity="%.2f"/>' % (x, y, x + s, y + rnd.randint(-40, 40), x + s // 2, y - s, rnd.choice(cols), rnd.uniform(.1, .35))
    return svg(b)
def skyline(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/>' % (W, H, base); x = 0
    while x < W:
        w, h = rnd.randint(90, 200), rnd.randint(200, 620); b += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"/>' % (x, H - h, w, h, rnd.choice(cols), rnd.uniform(.18, .4))
        for wy in range(H - h + 30, H - 20, 46):
            for wx in range(x + 16, x + w - 24, 34): b += '<rect x="%d" y="%d" width="14" height="22" fill="#fff" opacity=".25"/>' % (wx, wy)
        x += w + rnd.randint(4, 24)
    return svg(b)
def hills(rnd, cols, base):
    b = '<rect width="%d" height="%d" fill="%s"/><circle cx="%d" cy="%d" r="120" fill="%s" opacity=".5"/>' % (W, H, base, rnd.randint(300, 1600), rnd.randint(150, 350), cols[-1])
    for k in range(4):
        y = 560 + k * 110; p = 'M0 %d' % y
        for x in range(0, W + 1, 240): p += ' Q%d %d %d %d' % (x + 120, y - rnd.randint(60, 200), x + 240, y)
        b += '<path d="%s L%d %d L0 %d Z" fill="%s" opacity="%.2f"/>' % (p, W, H, H, cols[k % len(cols)], .35 + k * .12)
    return svg(b)
def paper(rnd, cols, base):
    d = '<filter id="n"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="%d"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .08 0"/></filter>' % rnd.randint(1, 99)
    return svg('<rect width="%d" height="%d" fill="%s"/><rect width="%d" height="%d" filter="url(#n)"/><ellipse cx="%d" cy="%d" rx="520" ry="90" fill="%s" opacity=".12"/>' % (W, H, base, W, H, W // 2, H - 150, cols[0]), d)
def aurora(rnd, cols, base):
    d = '<filter id="b" x="-30%%" y="-60%%" width="160%%" height="220%%"><feGaussianBlur stdDeviation="70"/></filter>'
    b = '<rect width="%d" height="%d" fill="%s"/><g filter="url(#b)">' % (W, H, base)
    for k, c in enumerate(cols[:3]): b += '<path d="M-100 %d C 400 %d 900 %d 1300 %d S 1900 %d 2100 %d L2100 %d C1600 %d 1100 %d 600 %d S 100 %d -100 %d Z" fill="%s" opacity=".6"/>' % (260 + k * 150, 100 + k * 100, 500 + k * 80, 300 + k * 120, 200 + k * 100, 350 + k * 130, 520 + k * 130, 700 + k * 80, 450 + k * 100, 650 + k * 90, 600 + k * 110, 480 + k * 130, c)
    return svg(b + '</g>', d)

KINDS = {'mesh': mesh, 'waves': waves, 'blobs': blobs, 'grid': grid, 'dots': dots, 'stripes': stripes, 'topo': topo, 'circles': circles, 'tri': tri, 'skyline': skyline, 'hills': hills, 'paper': paper, 'aurora': aurora}
# 名称, 分类, 类型, 说明, 生成方式, base, 配色
BG = [
 ('办公室天际线','办公','用','窗外城市楼群','skyline','#e4eefc',['#1f6feb','#5b8def','#12a594']),
 ('明亮会议室','办公','用','浅蓝柔光','mesh','#f1f6fd',['#9cc2ff','#c9defc','#b7ead9']),
 ('商务网格','办公','用','淡网格+光斑','grid','#f3f6fb',['#1f6feb','#7aa7f5']),
 ('蓝灰条纹','办公','用','斜条纹，克制','stripes','#eef2f7',['#1f3b66']),
 ('蓝色圆点','办公','用','点阵+光晕','dots','#f4f7fb',['#1f6feb','#12a594']),
 ('晨雾山丘','自然','用','绿色层叠山丘','hills','#e8f4e4',['#8fc486','#6fb06a','#4f9a58','#2f7d46']),
 ('绿色波浪','自然','用','平缓波浪','waves','#e6f3e1',['#b9dcb0','#8fc486','#6fb06a']),
 ('海岸蓝波','自然','用','蓝色海浪','waves','#e8f5fb',['#9fd3ea','#6bb9dc','#3a9cc8']),
 ('等高线','自然','用','地形等高线','topo','#f2f7ef',['#4f7a4a','#8aa77f']),
 ('沙丘','自然','用','暖沙色山丘','hills','#faf1e0',['#e6c89a','#d9a96a','#c78b45','#a76a2c']),
 ('日落色块','暖色','用','橙粉色块','blobs','#fff4ec',['#ffb98f','#ff9f80','#ffd36e']),
 ('玫瑰雾','暖色','用','粉紫柔光','mesh','#fff1f4',['#ffb3c7','#e9b5ff','#ffd6a5']),
 ('蜂蜜圆点','暖色','用','黄色大圆点','circles','#fffbea',['#f6c453','#f59e0b','#fbbf24']),
 ('珊瑚波浪','暖色','用','珊瑚橙波浪','waves','#fff3f0',['#ffb199','#ff8f70','#ffd0bf']),
 ('暖色三角','暖色','用','几何三角','tri','#fff6ee',['#f97316','#f59e0b','#ef4444']),
 ('午夜网格','深色','用','深蓝网格+蓝光','grid','#0e1424',['#6ea8ff','#4f7cff']),
 ('极光','深色','用','绿紫极光','aurora','#0b1020',['#34d399','#818cf8','#22d3ee']),
 ('紫夜光斑','深色','用','深紫光斑','mesh','#150f1f',['#7c3aed','#db2777','#4f46e5']),
 ('炭黑点阵','深色','用','炭黑底橙点','dots','#141414',['#fb923c','#38bdf8']),
 ('深色等高线','深色','用','暗底等高线','topo','#0f1520',['#6ea8ff','#5eead4']),
 ('薰衣草色块','抽象','用','紫粉色块','blobs','#f7f5fc',['#c9a8ff','#e9b5ff','#ffc2e2']),
 ('彩色圆圈','抽象','用','随机圆圈','circles','#f8f9fb',['#6741d9','#e64980','#12a594','#f59e0b']),
 ('冷色三角','抽象','用','蓝绿几何','tri','#eef5fb',['#1f6feb','#12a594','#7048e8']),
 ('柔光网格','抽象','用','浅色渐变网格','mesh','#fbfbfd',['#c7d2fe','#fbcfe8','#bae6fd']),
 ('彩虹光斑','抽象','用','多色柔光','mesh','#ffffff',['#a5b4fc','#f9a8d4','#fde68a','#86efac']),
 ('纸张纹理','纹理','用','米色纸+噪点','paper','#f8f4ec',['#8b5e34']),
 ('白纸','纹理','用','白纸+轻噪点','paper','#fbfbfb',['#999999']),
 ('灰纸','纹理','用','灰纸质感','paper','#eceeef',['#555555']),
 ('斜纹米色','纹理','用','米色斜纹','stripes','#f6efe3',['#8b5e34']),
 ('点阵灰','纹理','用','极淡灰点阵','dots','#f6f6f6',['#888888','#bbbbbb']),
 ('暖灰漂浮(参考 Weave)','参考风格','参','暖灰底+柔和脚下阴影+漂浮圆形，自己重画','circles','#f4f2f0',['#e8501f','#c9a86a','#4a0f1c']),
 ('草图方格(参考 Vizcom)','参考风格','参','纸白底+淡方格，像设计草图','grid','#f7f4f1',['#151515','#3b7ddd']),
 ('玻璃渐变(参考 Hunar)','参考风格','参','蓝紫黄渐变光斑，像毛玻璃卡片背景','mesh','#f9f9f8',['#2563eb','#7c3aed','#a3a82a']),
 ('米色大留白(参考 GANNI)','参考风格','参','极简暖白，配大图用','paper','#f6f2ee',['#9a5b2e']),
 ('蓝紫波浪','抽象','用','蓝紫渐变波浪','waves','#eef0ff',['#a5b4fc','#818cf8','#6366f1']),
]
def build_bgs():
    cat = []
    os.makedirs(os.path.join(ROOT, 'bg'), exist_ok=True)
    css = ['/* 自动生成：<html data-bg="NN"> 切换背景图 */']
    for i, (name, group, kind, note, how, base, cols) in enumerate(BG, 1):
        rnd = random.Random(1000 + i)
        s = KINDS[how](rnd, cols, base)
        fn = 'bg%02d.svg' % i
        open(os.path.join(ROOT, 'bg', fn), 'w', encoding='utf-8').write(s)
        css.append('[data-bg="%02d"]{--bg-img:url("../bg/%s")}' % (i, fn))
        cat.append(dict(n=i, id='%02d' % i, name=name, group=group, kind=kind, note=note, file='bg/' + fn, base=base, cols=cols))
    css.append('[data-bg="none"]{--bg-img:none}')
    open(os.path.join(ROOT, 'css', 'bgs.css'), 'w', encoding='utf-8').write('\n'.join(css) + '\n')
    return cat

if __name__ == '__main__':
    th, bg = build_themes(), build_bgs()
    low = [t for t in th if t['contrast'] < 7]
    open(os.path.join(ROOT, 'js', 'catalog.js'), 'w', encoding='utf-8').write('window.PJ116=' + json.dumps(dict(themes=th, bgs=bg), ensure_ascii=False) + ';\n')
    print('themes', len(th), 'bgs', len(bg), 'low-contrast(<7):', [t['id'] for t in low])
