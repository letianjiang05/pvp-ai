import os
import requests
from urllib.parse import urlparse

def download_file(url, save_dir):
    # 检查并创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 从URL中提取文件名
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    
    # 构建完整的文件路径
    file_path = os.path.join(save_dir, file_name)
    
    # 发送HTTP请求下载文件
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 将文件内容写入本地文件
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File downloaded and saved to {file_path}")
    else:
        print(f"Failed to download file from {url}, status code: {response.status_code}")

save_dir = "json"  # 保存目录
url_herolist = "http://pvp.qq.com/web201605/js/herolist.json"  # 文件URL
url_

download_file(url_herolist, save_dir)

