#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
整合所有页面内容，生成统一的社区门户网站
"""

import json
from pathlib import Path

def load_all_pages():
    """加载所有页面数据"""
    pages_data = []
    pages_dir = Path('website_data_named')  # 使用带名称的数据
    
    for page_dir in sorted(pages_dir.glob('page_*')):
        page_data = {'page_num': int(page_dir.name.split('_')[1])}
        
        # 读取英文文本
        en_file = page_dir / 'texts' / 'en.txt'
        if en_file.exists():
            with open(en_file, 'r', encoding='utf-8') as f:
                page_data['en_content'] = f.read()
        
        # 读取中文文本
        cn_file = page_dir / 'texts' / 'cn.txt'
        if cn_file.exists():
            with open(cn_file, 'r', encoding='utf-8') as f:
                page_data['cn_content'] = f.read()
        
        # 获取图片（现在使用有意义的文件名）
        images_dir = page_dir / 'images'
        page_data['images'] = []
        if images_dir.exists():
            for img in sorted(images_dir.glob('*')):
                page_data['images'].append(str(img.relative_to(page_dir)))  # 使用相对路径
        
        pages_data.append(page_data)
    
    return pages_data

def extract_key_info(pages_data):
    """提取关键信息"""
    
    # 提取基本信息
    hero = {
        'title_en': '3am Club',
        'subtitle_en': 'A community found by loyal crypto investor',
        'title_cn': '3am Club',
        'subtitle_cn': '由忠诚加密投资者创立的社群'
    }
    
    # 关于部分
    about = {
        'en': '',
        'cn': ''
    }
    
    # 联系方式
    contact = {
        'website': 'https://my3am.xyz',
        'twitter': 'https://twitter.com/my3amclub',
        'discord': 'https://discord.gg/VFt89f7Snp',
        'telegram': 'https://t.me/my3amclub'
    }
    
    # 服务/价值
    values = []
    services = []
    
    # 从页面数据中提取信息
    for page in pages_data:
        en_text = page.get('en_content', '')
        cn_text = page.get('cn_content', '')
        
        # 提取关于信息
        if 'About 3am Club' in en_text or '关于3am Club' in cn_text:
            about['en'] = en_text
            about['cn'] = cn_text
        
        # 提取服务信息
        if 'value' in en_text.lower() or '我们的' in cn_text:
            if len(en_text) > 50:
                values.append({
                    'en': en_text,
                    'cn': cn_text
                })
    
    return {
        'hero': hero,
        'about': about,
        'contact': contact,
        'values': values,
        'services': services,
        'pages': pages_data
    }

def generate_html(info):
    """生成HTML"""
    
    # 格式化关于文本
    about_en = info['about']['en'].replace('--- Text Block', '').replace('---', '').strip() if info['about']['en'] else '3am Club is a community founded by crypto followers.'
    about_cn = info['about']['cn'].replace('--- 文本块', '').replace('---', '').strip() if info['about']['cn'] else '3am Club是一个由加密爱好者创立的社区。'
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3am Club - 社区门户</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <div class="nav-brand">🌙 3am Club</div>
            <ul class="nav-menu">
                <li><a href="#home" onclick="showSection('home')">首页</a></li>
                <li><a href="#about" onclick="showSection('about')">关于</a></li>
                <li><a href="#services" onclick="showSection('services')">服务</a></li>
                <li><a href="#community" onclick="showSection('community')">社区</a></li>
                <li><a href="#contact" onclick="showSection('contact')">联系</a></li>
            </ul>
            <div class="lang-switch">
                <button class="lang-btn active" onclick="switchLang('cn')">中文</button>
                <button class="lang-btn" onclick="switchLang('en')">EN</button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero section">
        <div class="hero-content">
            <h1 class="hero-title" data-lang="both">3am Club</h1>
            <p class="hero-subtitle cn-text">由忠诚加密投资者创立的社群</p>
            <p class="hero-subtitle en-text" style="display: none;">A community found by loyal crypto investor</p>
            <div class="hero-cta">
                <a href="#about" class="btn btn-primary" onclick="showSection('about')">了解更多</a>
                <a href="#contact" class="btn btn-secondary" onclick="showSection('contact')">联系我们</a>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="section">
        <div class="container">
            <h2 class="section-title" data-lang="both">关于 3am Club</h2>
            <div class="about-content">
                <div class="about-text cn-text">
                    <p>{about_cn}</p>
                    <p>3am Club又叫麻音俱乐部，是一个由加密追随者共同创立的社群。3am Club社群是华语加密社群最具潜力的社群之一，现在3am Club已经集聚了华语加密圈100多位一线KOL，DiFi Degens、NFT 收藏家、项目Mod，优质赛道的投研专员，以及粉丝辐射总量超百万的海量加密爱好者。</p>
                </div>
                <div class="about-text en-text" style="display: none;">
                    <p>{about_en}</p>
                    <p>3am Club, also known as Mayin club, is a community co-founded by crypto followers. We have gathered more than 100 crypto KOLs, with over 1 million followers including DeFi degens, NFT collectors, project mods, researchers in the crypto field.</p>
                </div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">100+</div>
                        <div class="stat-label cn-text">KOL数量</div>
                        <div class="stat-label en-text" style="display: none;">Crypto KOLs</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">1M+</div>
                        <div class="stat-label cn-text">粉丝总量</div>
                        <div class="stat-label en-text" style="display: none;">Followers</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number cn-text">全球</div>
                        <div class="stat-number en-text" style="display: none;">Global</div>
                        <div class="stat-label cn-text">社区</div>
                        <div class="stat-label en-text" style="display: none;">Community</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Services Section -->
    <section id="services" class="section bg-dark">
        <div class="container">
            <h2 class="section-title" data-lang="both">我们的服务</h2>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">📢</div>
                    <h3 class="cn-text">行业资讯</h3>
                    <h3 class="en-text" style="display: none;">Industry Info</h3>
                    <p class="cn-text">分享加密行业最新信息</p>
                    <p class="en-text" style="display: none;">Share latest crypto industry information</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">👥</div>
                    <h3 class="cn-text">创始团队</h3>
                    <h3 class="en-text" style="display: none;">Founding Team</h3>
                    <p class="cn-text">经验丰富的行业专家</p>
                    <p class="en-text" style="display: none;">Experienced industry experts</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">⭐</div>
                    <h3 class="cn-text">社区KOL</h3>
                    <h3 class="en-text" style="display: none;">Community KOLs</h3>
                    <p class="cn-text">顶尖加密影响者网络</p>
                    <p class="en-text" style="display: none;">Top crypto influencers network</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🤝</div>
                    <h3 class="cn-text">合作伙伴</h3>
                    <h3 class="en-text" style="display: none;">Partners</h3>
                    <p class="cn-text">领先项目战略合作</p>
                    <p class="en-text" style="display: none;">Strategic partnerships</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">💰</div>
                    <h3 class="cn-text">投资孵化</h3>
                    <h3 class="en-text" style="display: none;">Investment</h3>
                    <p class="cn-text">支持早期项目发展</p>
                    <p class="en-text" style="display: none;">Support early-stage projects</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🚀</div>
                    <h3 class="cn-text">项目合作</h3>
                    <h3 class="en-text" style="display: none;">Cooperation</h3>
                    <p class="cn-text">全面支持区块链项目</p>
                    <p class="en-text" style="display: none;">Comprehensive project support</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Contact Section -->
    <section id="contact" class="section">
        <div class="container">
            <h2 class="section-title" data-lang="both">联系我们</h2>
            <div class="contact-grid">
                <a href="{info['contact']['website']}" target="_blank" class="contact-card">
                    <div class="contact-icon">🌐</div>
                    <h3>Website</h3>
                    <p class="cn-text">官方网站</p>
                    <p class="en-text" style="display: none;">Official Website</p>
                    <p>{info['contact']['website']}</p>
                </a>
                <a href="{info['contact']['twitter']}" target="_blank" class="contact-card">
                    <div class="contact-icon">🐦</div>
                    <h3>Twitter</h3>
                    <p class="cn-text">官方推特</p>
                    <p class="en-text" style="display: none;">Official Twitter</p>
                    <p>@my3amclub</p>
                </a>
                <a href="{info['contact']['discord']}" target="_blank" class="contact-card">
                    <div class="contact-icon">💬</div>
                    <h3>Discord</h3>
                    <p class="cn-text">加入社区</p>
                    <p class="en-text" style="display: none;">Join Community</p>
                    <p>Discord Server</p>
                </a>
                <a href="{info['contact']['telegram']}" target="_blank" class="contact-card">
                    <div class="contact-icon">📱</div>
                    <h3>Telegram</h3>
                    <p class="cn-text">电报群</p>
                    <p class="en-text" style="display: none;">Telegram Group</p>
                    <p>@my3amclub</p>
                </a>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 3am Club. All rights reserved.</p>
        </div>
    </footer>

    <script>
        // 语言切换
        function switchLang(lang) {{
            if (lang === 'cn') {{
                document.querySelectorAll('.cn-text').forEach(el => el.style.display = '');
                document.querySelectorAll('.en-text').forEach(el => el.style.display = 'none');
                document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
            }} else {{
                document.querySelectorAll('.cn-text').forEach(el => el.style.display = 'none');
                document.querySelectorAll('.en-text').forEach(el => el.style.display = '');
                document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
            }}
        }}
        
        // 显示section
        function showSection(id) {{
            document.querySelectorAll('.section').forEach(section => {{
                section.classList.remove('active');
            }});
            document.getElementById(id).classList.add('active');
        }}
        
        // 初始化第一个section
        document.getElementById('home').classList.add('active');
    </script>
</body>
</html>'''
    
    return html

def generate_css():
    """生成CSS样式"""
    return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #667eea;
    --secondary: #764ba2;
    --dark: #1a1a2e;
    --darker: #0f0f1e;
    --light: #e0e0e0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--darker);
    color: var(--light);
    line-height: 1.6;
}

/* Navbar */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    z-index: 1000;
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
}

.nav-container {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.nav-menu {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-menu a {
    color: var(--light);
    text-decoration: none;
    transition: all 0.3s;
}

.nav-menu a:hover {
    color: var(--primary);
}

.lang-switch {
    display: flex;
    gap: 0.5rem;
}

.lang-btn {
    padding: 0.5rem 1rem;
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    color: var(--light);
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s;
}

.lang-btn.active {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
}

/* Hero */
.hero {
    margin-top: 70px;
    min-height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
}

.hero-content {
    text-align: center;
    max-width: 800px;
    padding: 2rem;
}

.hero-title {
    font-size: 5rem;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.hero-cta {
    display: flex;
    gap: 1rem;
    justify-content: center;
}

.btn {
    padding: 1rem 2rem;
    text-decoration: none;
    border-radius: 50px;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
}

.btn-secondary {
    background: transparent;
    border: 2px solid var(--primary);
    color: var(--light);
}

.btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
}

/* Section */
.section {
    padding: 5rem 2rem;
    display: none;
}

.section.active {
    display: block;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.section-title {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 3rem;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.bg-dark {
    background: var(--dark);
}

/* About */
.about-content {
    max-width: 900px;
    margin: 0 auto;
}

.about-text {
    font-size: 1.2rem;
    line-height: 1.8;
    margin-bottom: 3rem;
    opacity: 0.9;
}

.about-text p {
    margin-bottom: 1rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
}

.stat-card {
    background: rgba(102, 126, 234, 0.1);
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s;
}

.stat-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.stat-number {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}

.stat-label {
    opacity: 0.8;
}

/* Services */
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}

.service-card {
    background: rgba(102, 126, 234, 0.05);
    padding: 2.5rem;
    border-radius: 20px;
    border: 1px solid rgba(102, 126, 234, 0.2);
    text-align: center;
    transition: all 0.3s;
}

.service-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    border-color: var(--primary);
}

.service-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.service-card h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--light);
}

.service-card p {
    opacity: 0.8;
    line-height: 1.6;
}

/* Contact */
.contact-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.contact-card {
    background: rgba(102, 126, 234, 0.05);
    padding: 2.5rem;
    border-radius: 20px;
    text-align: center;
    text-decoration: none;
    color: var(--light);
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s;
    display: block;
}

.contact-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    border-color: var(--primary);
}

.contact-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.contact-card h3 {
    margin-bottom: 1rem;
    color: var(--light);
}

.contact-card p {
    opacity: 0.7;
}

/* Footer */
.footer {
    text-align: center;
    padding: 3rem 2rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    opacity: 0.6;
}

/* Responsive */
@media (max-width: 768px) {
    .hero-title {
        font-size: 3rem;
    }
    
    .nav-menu {
        display: none;
    }
    
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .services-grid,
    .contact-grid {
        grid-template-columns: 1fr;
    }
}

'''

def main():
    print("🚀 开始生成统一的社区门户网站...")
    
    # 加载所有页面数据
    pages_data = load_all_pages()
    print(f"✓ 已加载 {len(pages_data)} 页数据")
    
    # 提取关键信息
    info = extract_key_info(pages_data)
    print("✓ 已提取关键信息")
    
    # 生成HTML和CSS
    html = generate_html(info)
    css = generate_css()
    
    # 保存文件
    portal_dir = Path('website')
    portal_dir.mkdir(exist_ok=True)
    
    with open(portal_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ 已生成: index.html")
    
    with open(portal_dir / 'style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("✓ 已生成: style.css")
    
    print("\n" + "="*60)
    print("✅ 完成！统一的社区门户网站已生成")
    print("="*60)
    print(f"📁 网站目录: {portal_dir.absolute()}")
    print(f"\n访问方式: open website/index.html")

if __name__ == "__main__":
    main()

