import os
import json
import shutil
from pathlib import Path
from PIL import Image

# Configuration
BASE_DIR = Path(os.getcwd())
SOURCE_IMG_DIR = BASE_DIR / "images/kol"
DEST_IMG_DIR = BASE_DIR / "portal/assets/images/kol"
DATA_FILE = BASE_DIR / "portal/site_content.json"

# Ensure dest dir exists
if os.path.exists(DEST_IMG_DIR):
    shutil.rmtree(DEST_IMG_DIR)
os.makedirs(DEST_IMG_DIR, exist_ok=True)

# Team Data
team_list = [
    {
        "name": "刘社长.eth",
        "desc": "3amClub创始人，操盘上百款app流量数据深耕Gamefi赛道，专注链游项目及投研",
        "twitter": "https://x.com/liushezhang",
        "followers": "70K+",
        "icon_name": "liushezhang.png"
    },
    {
        "name": "暴躁的希爷丶",
        "desc": "Bayc持有者，投资人，创业者，web3工作室创始人，专注最新项目机会。",
        "twitter": "https://x.com/yaking168",
        "followers": "57K+",
        "icon_name": "yaking168.png"
    },
    {
        "name": "sanyi.eth",
        "desc": "Web3 KOL，多个Web3项目的大使、推动者，互联网大厂运营管理",
        "twitter": "https://x.com/sanyi_eth_",
        "followers": "25.8K+",
        "icon_name": "sanyi.png"
    },
    {
        "name": "Calman",
        "desc": "Web3探寻者，专注于Web3项目用户增长；社区建设、品牌塑造",
        "twitter": "https://x.com/Calman16910515",
        "followers": "75K+",
        "icon_name": "Calman.png"
    },
    {
        "name": "超级罗杰斯",
        "desc": "15年+类金融行业投资者，8年+币圈交易员拥有成熟的投资和量化交易团队",
        "twitter": "https://x.com/superogers1",
        "followers": "28K+",
        "icon_name": "superogers1.png"
    },
    {
        "name": "雪球",
        "desc": "链游领域专家，深耕链游赛道，专注链游早期项目投研及增长运营。",
        "twitter": "https://x.com/xueqiu88",
        "followers": "90K+",
        "icon_name": "xueqiu88.jpg"
    },
    {
        "name": "磊哥",
        "desc": "3am Club技术总监  日本某大型交易平台技术专家,专注空投，NFT方向",
        "twitter": "https://x.com/zlexdl",
        "followers": "86K+",
        "icon_name": "zlexdl.png"
    },
    {
        "name": "lilili.eth",
        "desc": "资深社交媒体影响者，NFT早期发倔与扶持，擅长增加项目品牌影响力",
        "twitter": "https://x.com/dashutiaozi",
        "followers": "119K+",
        "icon_name": "dashutiaozi.jpg"
    },
    {
        "name": "charles",
        "desc": "专注defi类项目，隐私，应用等赛道，撸毛交互狂热者",
        "twitter": "https://x.com/charles48011843",
        "followers": "117K+",
        "icon_name": "charles48011843.png"
    },
    {
        "name": "捡个大西瓜",
        "desc": "千万英语学习app联合创始人，基金定投研究者，目前专注社区建设与新项目挖掘，以及定投在区块链投资的应用。",
        "twitter": "https://x.com/Uncle_Simon25",
        "followers": "17K+",
        "icon_name": "Uncle_Simon25.png"
    },
    {
        "name": "大树",
        "desc": "3am Club艺术总监、官推负责人，互联网公司品牌设计负责人。NFT创作 / 收藏 / 投研",
        "twitter": "https://x.com/ultree_",
        "followers": "17K+",
        "icon_name": "ultree_.png"
    },
    {
        "name": "Rick",
        "desc": "3am Club商务负责人 律师lawyer Web3法律服务提供者",
        "twitter": "https://x.com/xiaoxiaozhangsm",
        "followers": "17K+",
        "icon_name": "xiaoxiaozhangsm.png"
    },
    {
        "name": "Oeuia",
        "desc": "3am club商务经理，专注于Web3空&NFT&Gamefi，发掘早期优质项目",
        "twitter": "https://x.com/oeuia_eth",
        "followers": "7K+",
        "icon_name": "oeuia_eth.png"
    }
]

def process_images():
    print(f"Source Directory: {SOURCE_IMG_DIR}")
    
    if not SOURCE_IMG_DIR.exists():
        print(f"Error: Source directory {SOURCE_IMG_DIR} does not exist!")
        return

    for member in team_list:
        icon_name = member['icon_name']
        src_path = SOURCE_IMG_DIR / icon_name
        
        if not src_path.exists():
             print(f"Warning: Source image not found: {src_path}")
             continue
             
        dest_path = DEST_IMG_DIR / icon_name
        
        try:
            with Image.open(src_path) as img:
                if icon_name.lower().endswith(('.jpg', '.jpeg')):
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    img.save(dest_path, 'JPEG', quality=90)
                else:
                    img.save(dest_path, 'PNG')
            
            member['image'] = f"assets/images/kol/{icon_name}"
            print(f"Synced: {icon_name}")
            
        except Exception as e:
            print(f"Error processing {icon_name}: {e}")

def update_json():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        new_team_data = []
        for m in team_list:
            new_team_data.append({
                "name": m['name'],
                "role": "Core Team",
                "desc": {
                    "cn": m['desc'],
                    "en": m['desc']
                },
                "image": m.get('image', ''),
                "twitter": m['twitter'],
                "followers": m['followers']
            })
            
        data['team'] = new_team_data
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print("Successfully updated site_content.json")
        
    except Exception as e:
        print(f"Error updating JSON: {e}")

if __name__ == "__main__":
    process_images()
    update_json()
