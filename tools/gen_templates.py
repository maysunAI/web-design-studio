# 生成 templates/*.html（共 10 个）。运行：python tools/gen_templates.py
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = '''<!doctype html>
<html lang="zh" data-default-bg="%(bg)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="stylesheet" href="../css/tokens.css">
<link rel="stylesheet" href="../css/themes.css">
<link rel="stylesheet" href="../css/bgs.css">
<link rel="stylesheet" href="../css/layout.css">
<link rel="stylesheet" href="../css/motion.css">
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
'''
FOOT = '''
<script src="../js/catalog.js"></script>
<script src="../js/studio.js"></script>
</body>
</html>
'''
NAV = lambda logo, items, cta, cls='': '<header class="nav %s"><div class="wrap"><a class="logo" href="#">%s</a>%s<a class="btn primary" href="#">%s</a></div></header>' % (cls, logo, ''.join('<a class="item" href="#"%s>%s</a>' % (' aria-current="page"' if i == 0 else '', x) for i, x in enumerate(items)), cta)
SIDE = lambda brand, groups: '<nav class="side" aria-label="主菜单"><a class="brand" href="#">%s</a>%s</nav>' % (brand, ''.join('<h4>%s</h4>%s' % (g, ''.join('<a class="mi" href="#"%s>%s</a>' % (' aria-current="page"' if (gi == 0 and i == 0) else '', it) for i, it in enumerate(its))) for gi, (g, its) in enumerate(groups)))

P = {}
# 01_meeting 默认背景 01=办公室天际线（用户 req52 指定）
P['01_meeting'] = ('视频会议首页', '01', NAV('📹 MeetNow', ['功能', '怎么用', '安全'], '开始会议') + '''
<main id="main">
<section class="hero"><div class="wrap">
 <div><span class="badge" data-reveal>无需安装 · 手机电脑都能用</span>
 <h1 data-reveal data-delay="1">一个链接，<span class="shimmer">马上开会</span></h1>
 <p class="lead" data-reveal data-delay="2">点一下生成会议链接，发给对方就能进。画面清楚，声音稳定，需要时一键共享屏幕。</p>
 <div class="cta" data-reveal data-delay="3"><a class="btn primary" href="#">新建会议</a><a class="btn" href="#">输入会议号加入</a></div></div>
 <div data-reveal="right"><div class="stage"><div class="tile speaking">王经理</div><div class="tile">Sato</div><div class="tile">Li</div><div class="tile">我</div></div>
 <div class="controls"><button class="btn" aria-label="静音">🎤</button><button class="btn" aria-label="摄像头">📷</button><button class="btn" aria-label="共享屏幕">🖥️</button><button class="btn primary">离开</button></div></div>
</div></section>
<section class="section"><div class="wrap"><h2 data-reveal>开会需要的，都在这里</h2><p class="sub" data-reveal>电脑上多列铺开，手机上自动变单列。</p>
 <div class="grid g4">
  <article class="card lift" data-reveal><div class="ico">🔗</div><h3>一键链接</h3><p class="muted">不用注册，复制链接发出去。</p></article>
  <article class="card lift" data-reveal data-delay="1"><div class="ico">🌐</div><h3>实时字幕与翻译</h3><p class="muted">中日英互相听得懂。</p></article>
  <article class="card lift" data-reveal data-delay="2"><div class="ico">🖥️</div><h3>共享屏幕</h3><p class="muted">演示文件、网页。</p></article>
  <article class="card lift" data-reveal data-delay="3"><div class="ico">🔒</div><h3>浏览器直连</h3><p class="muted">画面不经过服务器。</p></article>
 </div></div></section>
</main>''')

P['02_dashboard'] = ('工具后台（左侧菜单）', '16', '''<div class="shell">
''' + SIDE('⚙️ ToolBox', [('工作区', ['📊 概览', '🗂️ 项目', '📈 报表']), ('管理', ['👥 成员', '⚙️ 设置'])]) + '''
<main class="main" id="main">
 <h1 style="margin-top:0">概览</h1>
 <div class="grid g4">
  <div class="card" data-reveal><div class="muted">今日访问</div><div class="stat">1,284</div><div class="grow-bar" style="--v:72%"><i></i></div></div>
  <div class="card" data-reveal data-delay="1"><div class="muted">新用户</div><div class="stat">86</div><div class="grow-bar" style="--v:45%"><i></i></div></div>
  <div class="card" data-reveal data-delay="2"><div class="muted">错误率</div><div class="stat">0.4%</div><div class="grow-bar" style="--v:8%"><i></i></div></div>
  <div class="card" data-reveal data-delay="3"><div class="muted">响应时间</div><div class="stat">182 ms</div><div class="grow-bar" style="--v:30%"><i></i></div></div>
 </div>
 <section class="section"><div class="grid g2">
  <div class="card" data-reveal><h3>最近活动 <span class="pulse-dot"></span></h3><p class="muted">这里放列表或图表。电脑上两列并排，手机上叠成一列。</p></div>
  <div class="card" data-reveal data-delay="1"><h3>待办</h3><p class="muted">侧栏在手机上变成顶部横向滚动条。</p></div>
 </div></section>
</main></div>''')

P['03_ai_workspace'] = ('AI 工作台（左菜单+对话+右侧栏）', '17', '''<div class="shell three">
''' + SIDE('✨ Workspace', [('对话', ['💬 新对话', '🕘 历史']), ('工具', ['📄 文档', '🧩 模板', '⚙️ 设置'])]) + '''
<main class="main ws" id="main">
 <h1 style="margin-top:0">今天想做什么？</h1>
 <div class="chips" data-reveal><span class="chip on">写文案</span><span class="chip">总结文档</span><span class="chip">翻译</span><span class="chip">画图</span></div>
 <div class="chat" style="margin-top:20px">
  <div class="msg me" data-reveal="right">帮我把这份会议纪要整理成三条待办。</div>
  <div class="msg" data-reveal="left">好的。我读完了，整理如下：<br>1. 周五前交报价<br>2. 下周一排会议室<br>3. 联系日方确认时间</div>
 </div>
 <div class="composer"><input aria-label="输入消息" placeholder="输入你的问题…"><button class="btn primary">发送</button></div>
</main>
<aside class="rail"><h3 style="margin-top:0">上下文</h3><div class="card" data-reveal><b>会议纪要.docx</b><p class="muted">3 页 · 已读取</p></div><div class="card" data-reveal data-delay="1" style="margin-top:12px"><b>用量</b><div class="grow-bar" style="--v:38%;margin-top:8px"><i></i></div><p class="muted">本月 38%</p></div></aside>
</div>''')

P['04_bento'] = ('Bento 便当格首页', '03', NAV('◆ Bento', ['特点', '价格', '客户'], '免费试用') + '''
<main id="main">
<section class="hero center"><div class="wrap"><h1 data-reveal>把一切放进<span class="shimmer">一个格子</span></h1><p class="lead" data-reveal data-delay="1">便当格布局：不同大小的卡片拼成一面，电脑上铺满，手机上叠成一列。</p><div class="cta" data-reveal data-delay="2"><a class="btn primary" href="#">开始</a><a class="btn" href="#">看演示</a></div></div></section>
<section class="section"><div class="wrap"><div class="bento">
 <div class="card b2 r2 tint g-a lift" data-reveal><h3>主打功能</h3><p class="muted">最大的格子放最重要的事。</p><div class="float" style="font-size:4rem">🚀</div></div>
 <div class="card lift" data-reveal data-delay="1"><h3>快</h3><p class="muted">秒开。</p></div>
 <div class="card lift" data-reveal data-delay="2"><h3>稳</h3><p class="muted">99.9%。</p></div>
 <div class="card b2 lift" data-reveal data-delay="1"><h3>数据一眼看清</h3><div class="grow-bar" style="--v:80%"><i></i></div></div>
 <div class="card lift" data-reveal><h3>三语</h3><p class="muted">中日英。</p></div>
 <div class="card lift tint g-b" data-reveal data-delay="1"><h3>安全</h3></div>
 <div class="card b2 lift" data-reveal data-delay="2"><h3>客户说</h3><p class="muted">"用起来很顺手。"</p></div>
</div></div></section>
</main>''')

P['05_bigtype'] = ('大字排版首页（参考 Vizcom 风格）', '05', NAV('vizlike', ['产品', '方案', '价格'], '试一试', 'pill') + '''
<main id="main">
<section class="hero center" style="min-height:78vh;display:grid;align-items:center"><div class="wrap">
 <p class="bigtype" data-reveal="zoom">Make it <span class="shimmer">real</span></p>
 <p class="lead" data-reveal data-delay="2">超大标题 + 一行说明 + 两个按钮。留白多，一眼就知道这是什么。</p>
 <div class="cta" data-reveal data-delay="3"><a class="btn primary" href="#">开始</a><a class="btn" href="#">预约演示</a></div>
 <div class="float" style="font-size:3rem;position:absolute;left:6%;top:24%">✏️</div><div class="float b" style="font-size:3rem;position:absolute;right:7%;top:58%">🧊</div></div></section>
<section class="section"><div class="wrap"><div class="grid"><div class="card lift" data-reveal><div class="ph wide">图 1</div><h3>草图</h3></div><div class="card lift" data-reveal data-delay="1"><div class="ph wide">图 2</div><h3>渲染</h3></div><div class="card lift" data-reveal data-delay="2"><div class="ph wide">图 3</div><h3>成品</h3></div></div></div></section>
</main>''')

P['06_shop'] = ('商品墙（左侧筛选+大图，参考 GANNI 风格）', '23', '''<header class="nav"><div class="wrap"><a class="logo" href="#" style="font-size:1.8rem;letter-spacing:-.04em">BRAND</a><a class="item" href="#">新品</a><a class="item" href="#">包</a><a class="item" href="#">服装</a><a class="item" href="#">鞋</a><a class="item" href="#">🔍</a><a class="item" href="#">🛍️</a></div></header>
<main id="main">
<section class="shop-hero"><div><h1 data-reveal>BRAND</h1><a class="btn primary" href="#" data-reveal data-delay="1">查看新品 →</a></div></section>
<div class="wrap section"><div class="shell" style="min-height:0;grid-template-columns:220px minmax(0,1fr);gap:var(--gap)">
 <nav class="side" style="height:auto;position:sticky;top:76px;border:0;background:transparent;padding:0" aria-label="筛选"><h4>分类</h4><a class="mi" href="#" aria-current="page">全部</a><a class="mi" href="#">包</a><a class="mi" href="#">服装</a><a class="mi" href="#">鞋</a><h4>价格</h4><a class="mi" href="#">¥0-500</a><a class="mi" href="#">¥500+</a></nav>
 <div class="grid g4">''' + ''.join('<article class="lift" data-reveal data-delay="%d"><div class="ph tall">商品图</div><b>商品 %d</b><div class="muted">¥%d</div></article>' % (i % 4, i + 1, 299 + i * 40) for i in range(8)) + '''</div>
</div></div></main>''')

P['07_docs'] = ('文档/知识库（左导航+正文+目录）', '20', NAV('📚 Docs', ['指南', '参考', '更新'], '搜索') + '''
<div class="wrap section"><div class="docs">
 <aside><nav class="toc" aria-label="文档导航"><b>入门</b><a href="#">简介</a><a href="#">安装</a><a href="#">第一步</a><b style="display:block;margin-top:14px">进阶</b><a href="#">配置</a><a href="#">常见问题</a></nav></aside>
 <article id="main"><h1 data-reveal>简介</h1><p class="lead muted" data-reveal>左边是菜单，中间是正文，右边是本页目录。电脑上三栏，手机上只剩正文。</p><h2 id="a">这是什么</h2><p>正文行宽限制在约 78 个字符，长文章读起来不累。</p><h2 id="b">怎么用</h2><p>每个标题都能在右侧目录里点到。</p></article>
 <aside class="toc"><b>本页</b><a href="#a">这是什么</a><a href="#b">怎么用</a></aside>
</div></div>''')

P['08_saas_cards'] = ('工具首页：标题+客户滚动条+三张彩色卡片（参考 Hunar 风格）', '06', NAV('◈ Tool', ['方案', '产品', '客户', '资源'], '预约演示') + '''
<main id="main">
<section class="hero"><div class="wrap"><div><h1 data-reveal>把对话变成<br>更好的结果。</h1><p class="lead" data-reveal data-delay="1">左对齐大标题，一句说明，一个按钮。下面是客户 Logo 滚动条和三张彩色卡片。</p><div class="cta" data-reveal data-delay="2"><a class="btn primary square" href="#">预约演示 ›</a></div></div><div class="card" data-reveal="right"><div class="ph wide">演示视频</div></div></div></section>
<section class="section" style="padding-block:20px"><div class="wrap marquee"><div class="track"><div class="logos"><span>indigold</span><span>croma</span><span>TATA</span><span>Rupeek</span><span>PhonePe</span><span>BASIC</span></div><div class="logos" aria-hidden="true"><span>indigold</span><span>croma</span><span>TATA</span><span>Rupeek</span><span>PhonePe</span><span>BASIC</span></div></div></div></section>
<section class="section"><div class="wrap grid"><div class="card tint g-a lift" data-reveal><h3>招聘</h3><p class="muted">自动初筛。</p><div class="ph wide" style="background:rgba(255,255,255,.18)">界面截图</div></div><div class="card tint g-b lift" data-reveal data-delay="1"><h3>入职</h3><p class="muted">材料自动收集。</p><div class="ph wide" style="background:rgba(255,255,255,.18)">界面截图</div></div><div class="card tint g-c lift" data-reveal data-delay="2"><h3>培训</h3><p class="muted">小测验。</p><div class="ph wide" style="background:rgba(255,255,255,.18)">界面截图</div></div></div></section>
</main>''')

P['09_gallery'] = ('作品集瀑布流', '21', NAV('◐ Studio', ['作品', '关于', '联系'], '合作') + '''
<main id="main"><section class="section"><div class="wrap"><h1 style="font-size:var(--fs-hero);margin:0 0 .3em" data-reveal>作品</h1><p class="sub" data-reveal>瀑布流：电脑 4 列，平板 2 列，手机 1 列，图片高矮不一也不留空。</p>
<div class="masonry">''' + ''.join('<div class="ph %s lift" data-reveal data-delay="%d">作品 %d</div>' % (['', 'tall', 'wide', 'tall'][i % 4], i % 3, i + 1) for i in range(12)) + '''</div></div></section></main>''')

P['10_learning'] = ('学习与记录（进度+标签）', '11', NAV('🌱 每日一点', ['今天', '复习', '记录'], '开始') + '''
<main id="main">
<section class="hero"><div class="wrap"><div><span class="badge" data-reveal>连续学习 12 天</span><h1 data-reveal data-delay="1">每天一点点，<br>不用打字</h1><p class="lead" data-reveal data-delay="2">选一选、拖一拖就能完成今天的学习记录。</p><div class="cta"><a class="btn primary" href="#">开始今天的 5 分钟</a></div></div>
 <div class="card" data-reveal="right"><h3>今日进度</h3><p class="muted">日语单词 8 / 20 · 英语 3 / 10</p><div class="grow-bar" style="--v:40%"><i></i></div></div></div></section>
<section class="section"><div class="wrap"><h2 data-reveal>想法分类</h2><p class="sub">用标签筛选，比长长一列更好找。</p><div class="chips" style="margin-bottom:18px"><span class="chip on">全部</span><span class="chip">工作</span><span class="chip">学习</span><span class="chip">生活</span></div>
<div class="grid g4">''' + ''.join('<article class="card lift" data-reveal data-delay="%d"><span class="badge">%s</span><h3>想法标题 %d</h3><p class="muted">一两行摘要。</p></article>' % (i % 4, ['工作', '学习', '生活'][i % 3], i + 1) for i in range(8)) + '''</div></div></section></main>''')

P['11_stats_hero'] = ('统计大卡首页（参考 Japan Shorts）', '30', '''<header class="topline"><div class="wrap"><a class="logo" href="#">Japan Shorts</a><a class="item" href="#" aria-current="page">首页</a><a class="item" href="#">精选短片</a><a class="item" href="#">学习法</a><a class="item" href="#">版权</a></div></header>
<main id="main" class="wrap">
 <section class="hero-dark" data-reveal><h1>用真实日语视频，练一双能听懂的耳朵</h1><p>左边看真实视频，右边跟实时字幕。日语原文 + 假名 + 中文翻译。</p><a class="go" href="#">看已经做好的短片 →</a>
  <div class="stats"><div class="st"><b>1</b><span>已完整制作</span></div><div class="st"><b>2</b><span>已产出成片</span></div><div class="st"><b>700+</b><span>可用的 CC 授权视频</span></div><div class="st"><b>CC BY</b><span>素材授权类型</span></div></div></section>
 <section class="section"><div class="grid">
  <article class="card fcard lift" data-reveal><h3>🎬 精选短片</h3><p>真实日语视频，配原文+假名+译文字幕。</p><a class="more" href="#">查看短片 →</a></article>
  <article class="card fcard lift" data-reveal data-delay="1"><h3>📖 精听学习法</h3><p>"左边看视频、右边跟字幕"具体怎么用。</p><a class="more" href="#">了解方法 →</a></article>
  <article class="card fcard lift" data-reveal data-delay="2"><h3>📄 素材与版权</h3><p>视频来源、授权类型、识别可能有误的地方。</p><a class="more" href="#">查看说明 →</a></article>
 </div></section></main>''')

P['12_video_grid'] = ('视频卡片网格（参考 Japan Shorts）', '30', '''<header class="topline"><div class="wrap"><a class="logo" href="#">Japan Shorts</a><a class="item" href="#">首页</a><a class="item" href="#" aria-current="page">精选短片</a><a class="item" href="#">学习法</a></div></header>
<main id="main" class="wrap"><div class="titlebar" data-reveal><h2>精选短片</h2><p>点击卡片进入详情；灰色卡片是排队中的素材。</p></div>
<div class="vgrid" style="margin-top:18px">''' + ''.join('<article class="vcard" data-reveal data-delay="%d"><div class="thumb"><div class="l"></div><div class="r"><i></i><i></i><i></i><i></i></div></div><div class="body"><h3>已完成的短片标题 %d</h3><span class="pill ok">✅ 已完整制作</span><span class="pill lic">CC BY 3.0</span><div class="meta">时长 21分45秒 · 字幕 495 段</div></div></article>' % (i % 3, i + 1) for i in range(3)) + ''.join('<article class="vcard" data-reveal data-delay="%d"><div class="thumb wait">⏳</div><div class="body"><h3>排队中的短片标题 %d</h3><span class="pill wait">⏳ 排队中</span><span class="pill lic">CC BY 3.0</span><div class="meta">时长 12分1秒</div></div></article>' % (i % 3, i + 1) for i in range(6)) + '''</div></main>''')

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'templates'), exist_ok=True)
    meta = []
    for k, (title, bg, body) in P.items():
        open(os.path.join(ROOT, 'templates', k + '.html'), 'w', encoding='utf-8').write(HEAD % dict(title=title, bg=bg) + body + FOOT)
        meta.append(dict(n=int(k[:2]), file='templates/%s.html' % k, name=title))
    import json
    open(os.path.join(ROOT, 'js', 'templates.js'), 'w', encoding='utf-8').write('window.PJ116T=' + json.dumps(meta, ensure_ascii=False) + ';\n')
    print(len(P), 'templates')
