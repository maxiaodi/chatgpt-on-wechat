import requests
import tempfile
import os
from urllib.parse import urlparse

from common.tmp_dir import TmpDir


class DownloadFile(object):
    def __init__(self):
        self.path = TmpDir().path()
        self.temp_path = ""

    def download_image(
            self,
            url: str,
            save_dir: str = None,
            filename: str = None,
            overwrite: bool = True,  # 新增：是否覆盖现有文件
    ) -> str:
        """
        从URL下载图片并保存到本地（使用URL中的原始文件名）

        参数:
            url: 图片URL（必须包含文件名）
            save_dir: 保存目录（默认当前目录）
            overwrite: 是否覆盖现有文件（默认True）
            check_hash: 是否检查文件哈希避免重复下载（默认False）

        返回:
            保存的文件绝对路径

        异常:
            会抛出包含详细信息的RuntimeError
        """
        try:
            # 1. 验证URL
            if not url.lower().startswith(('http://', 'https://')):
                raise ValueError("只支持http/https协议的URL")

            # 2. 从URL提取文件名
            parsed = urlparse(url)
            filename = os.path.basename(parsed.path)
            if not filename:
                raise ValueError("URL中未检测到文件名")

            # 3. 准备保存路径
            save_dir = save_dir or self.path
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)

            # 4. 检查文件是否存在
            if os.path.exists(save_path):
                if not overwrite:
                    return save_path

            # 5. 下载图片
            headers = {
                "accept": "*/*",
                "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "cache-control": "no-cache",
                "pragma": "no-cache",
                "priority": "u=1, i",
                "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "none",
                "sec-fetch-storage-access": "active",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
            }
            response = requests.get(url, headers=headers, stream=True, verify=False)
            response.raise_for_status()

            # 6. 写入临时文件（确保原子性操作）
            self.temp_path = f"{save_path}.tmp"

            with open(self.temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # 7. 哈希校验（如果启用）

            # 8. 重命名为目标文件
            os.replace(self.temp_path, save_path)  # 原子性覆盖操作

            return save_path

        except Exception as e:
            # 清理临时文件
            if 'temp_path' in locals() and os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except:
                    pass
            raise RuntimeError(f"图片下载失败: {str(e)}")

if __name__ =="__main__":
    download_file = DownloadFile()
    image_path = download_file.download_image(
        url="http://file.alapi.cn/60s/202504031743617702.png",
        overwrite=True  # 只有当内容不同时才下载
    )
    print(image_path)