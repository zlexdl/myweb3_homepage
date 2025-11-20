import json
import re

# Load raw data
try:
    with open('portal/data.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
except FileNotFoundError:
    print("Error: portal/data.json not found. Run build_site.py first.")
    exit(1)

# Helper to find slide by ID
def get_slide(slide_id):
    for s in raw_data:
        if s['id'] == slide_id:
            return s
    return None

# Helper to extract text lines excluding empty ones
def get_lines(text):
    if not text: return []
    return [line.strip() for line in text.split('\n') if line.strip()]

def process_hero():
    s = get_slide('slide_01')
    cn_lines = get_lines(s['content']['cn'])
    en_lines = get_lines(s['content']['en'])
    
    return {
        "title": "3am Club",
        "subtitle": {
            "cn": cn_lines[1] if len(cn_lines) > 1 else "",
            "en": en_lines[1] if len(en_lines) > 1 else ""
        },
        "bg_image": s['images'][0] if s['images'] else ""
    }

def process_about():
    s4 = get_slide('slide_04')
    s6 = get_slide('slide_06') # Stats
    
    # Extract stats manually based on known content
    stats = [
        {"value": "37k+", "label": {"cn": "推特粉丝", "en": "Twitter Followers"}},
        {"value": "12k+", "label": {"cn": "Discord成员", "en": "Discord Members"}},
        {"value": "100+", "label": {"cn": "KOL", "en": "KOLs"}},
        {"value": "1M+", "label": {"cn": "辐射用户", "en": "Reach"}}
    ]

    # Clean up About text (remove links for separate display if needed, but keeping simple for now)
    # Extract just the intro paragraphs
    cn_text = s4['content']['cn'].split('关于3am Club')[0].strip()
    en_text = s4['content']['en'].split('About  3am Club')[0].strip()

    links = {
        "website": "https://my3am.xyz",
        "twitter": "https://twitter.com/my3amclub",
        "discord": "http://discord.gg/VFt89f7Snp",
        "telegram": "https://t.me/my3amclub"
    }

    return {
        "intro": {
            "cn": cn_text,
            "en": en_text
        },
        "stats": stats,
        "links": links,
        "images": s4['images']
    }

def process_services():
    s14 = get_slide('slide_14')
    
    # Hardcoded service extraction based on slide 14 text structure
    # This is a bit hacky but effective for this specific content
    services = [
        {
            "title": {"cn": "项目推动", "en": "Project Promotion"},
            "desc": {"cn": "参与多个项目的大使，来帮项目提供建议以及制定推广方案", "en": "Act as ambassadors to provide advice and promotion plans."}
        },
        {
            "title": {"cn": "项目媒介", "en": "Media Relations"},
            "desc": {"cn": "运用3amClub的资源优势，帮助优质项目，完成私募/融资情况", "en": "Help quality projects with fundraising using our resources."}
        },
        {
            "title": {"cn": "媒体衔接", "en": "Media Connection"},
            "desc": {"cn": "帮项目方以及媒体做衔接，寻找到适合的媒体以及KOL", "en": "Connect projects with suitable media and KOLs."}
        },
        {
            "title": {"cn": "活动推广", "en": "Event Marketing"},
            "desc": {"cn": "通过社区媒体宣发，KOL转发抽奖，AMA，以及表单抽奖等形式", "en": "Promotion via community media, KOL retweets, AMAs, lucky draws."}
        },
        {
            "title": {"cn": "项目代运营", "en": "Operation"},
            "desc": {"cn": "根据项目特点，定制独有的运营方案 (DC, Twitter等)", "en": "Customized operation plans for Discord, Twitter, etc."}
        }
    ]
    return services

def process_team():
    s8 = get_slide('slide_08')
    
    # The text in slide 8 is a bit messy. 
    # We will structure it manually based on the names visible in the text.
    # To be safe and robust, we might just provide the list of names and let frontend render a grid of cards 
    # mapping to the images (which are usually in order).
    
    # Images in slide 8 are KOL/Team images.
    # Let's try to map them.
    
    members = [
        {"name": "刘社长.eth", "role": "Founder", "desc": {"cn": "3amClub创始人，深耕Gamefi赛道", "en": "Founder of My 3am Club, GameFi expert"}},
        {"name": "sanyi", "role": "Web3 KOL", "desc": {"cn": "多个Web3项目的大使、推动者", "en": "Ambassador of multiple Web3 projects"}},
        {"name": "超级罗杰斯", "role": "Investor", "desc": {"cn": "15年+类金融行业投资者", "en": "15+ years in finance investing"}},
        {"name": "暴躁的希爷", "role": "Core Member", "desc": {"cn": "社区核心成员", "en": "Core Community Member"}},
        {"name": "雪球", "role": "Researcher", "desc": {"cn": "基金定投研究者", "en": "Funds investments researcher"}},
        {"name": "lilili.eth", "role": "Core Member", "desc": {"cn": "Web3探寻者", "en": "Web3 Explorer"}},
        {"name": "Calman", "role": "Growth", "desc": {"cn": "专注于Web3项目用户增长", "en": "Focus on user growth"}},
        {"name": "zlexdl.eth", "role": "GameFi", "desc": {"cn": "链游领域专家", "en": "GameFi Specialist"}},
        {"name": "charles", "role": "Tech Lead", "desc": {"cn": "3am Club技术总监", "en": "Technical Director"}},
        {"name": "捡个大西瓜", "role": "Art Director", "desc": {"cn": "3am Club艺术总监", "en": "Art Director"}}
    ]
    
    # Assign images linearly to members (careful about count matching)
    team_images = s8['images']
    for i, member in enumerate(members):
        if i < len(team_images):
            member['image'] = team_images[i]
        else:
            member['image'] = "" # Placeholder needed
            
    return members

def process_cases():
    # Aggregate case studies from slides 16-22
    cases = []
    
    # Helper to add case
    def add_case(slide_id, title_cn, title_en):
        s = get_slide(slide_id)
        if s and s['images']:
            cases.append({
                "title": {"cn": title_cn, "en": title_en},
                "images": s['images'],
                "desc": {"cn": s['content']['cn'], "en": s['content']['en']} # simplified
            })

    add_case('slide_16', "Galaxy Brain", "Galaxy Brain Case")
    add_case('slide_17', "Ultiverse", "Ultiverse Case")
    add_case('slide_20', "CryptoSimeji", "CryptoSimeji Case")
    
    return cases

def process_contact():
    s29 = get_slide('slide_29')
    return {
        "text": {
            "cn": "3am Club 拥有一群追随加密世界的Degens... 感谢您愿意了解3am Club",
            "en": "3am Club has a group of Degens following the crypto world... Thank you for knowing us."
        },
        "email": "my3amclub@gmail.com",
        "twitter": "@My3amclub",
        "bd": "@xiaoxiaozhangsm"
    }

def main():
    site_content = {
        "hero": process_hero(),
        "about": process_about(),
        "services": process_services(),
        "team": process_team(),
        "cases": process_cases(),
        "contact": process_contact(),
        "gallery": get_slide('slide_26')['images'] if get_slide('slide_26') else [] # Investment slide has many logos/images
    }
    
    with open('portal/site_content.json', 'w', encoding='utf-8') as f:
        json.dump(site_content, f, ensure_ascii=False, indent=2)
    
    print("Successfully generated portal/site_content.json")

if __name__ == "__main__":
    main()

