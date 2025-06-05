import sys
import json
import os
from datetime import datetime
from PyRSS2Gen import RSS2, RSSItem

# 配置参数
TARGET_REPO_URL = "https://github.com/dw-dengwei/daily-arXiv-ai-enhanced.git" 
SITE_URL = "https://duyifanict.github.io/markdown-monitor"  # 替换为你的Pages地址

def generate_feed(changed_files):
    items = []
    files = json.loads(sys.argv[1])
    
    for file in files:
        file_path = f"data/{file}"
        pub_date = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        with open(file_path, "r") as f:
            content = f.read()
            # 可选：截取摘要
            description = content[:300] + "..." if len(content) > 300 else content
        
        items.append(RSSItem(
            title=f"更新: {file}",
            link=f"{TARGET_REPO_URL}/blob/main/{file.replace(' ', '%20')}",
            description=f"<pre>{description}</pre>",
            pubDate=pub_date
        ))
    
    rss = RSS2(
        title="Markdown文件更新追踪",
        link=SITE_URL,
        description="自动监控的Markdown变更订阅",
        lastBuildDate=datetime.now(),
        items=items
    )
    rss.write_xml(open("feed.xml", "w", encoding="utf-8"))

if __name__ == "__main__":
    generate_feed(sys.argv[1])