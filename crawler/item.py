import os
from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/88.0.4324.104 Safari/537.36 '
}

# 获取物品列表的JSON数据并解析为
target = 'https://pvp.qq.com/web201605/js/item.json'
item_df = pd.DataFrame(requests.get(target, headers=headers).json())

# 数据预处理
item_df.sort_values(["item_type", "price", "item_id"], inplace=True)
item_df.fillna("", inplace=True)
item_df['des1'] = item_df['des1'].str.replace("</?p>", "", regex=True)
item_df['des2'] = item_df['des2'].str.replace("</?p>", "", regex=True)

# 定义下载图片的函数
def download_img(item_id):
    img_path = f"imgs/{item_id}.jpg"
    if not os.path.exists(img_path):
        img_url = f"http://game.gtimg.cn/images/yxzj/img201606/itemimg/{item_id}.jpg"
        res = requests.get(img_url)
        with open(img_path, "wb") as f:
            f.write(res.content)

# 创建保存图片的目录
os.makedirs("itemimg", exist_ok=True)

# 使用线程池并发下载图片
with ThreadPoolExecutor(max_workers=8) as executor:
    executor.map(download_img, item_df['item_id'])
