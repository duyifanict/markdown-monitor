import sys
import json
import os
import frontmatter
from datetime import datetime
from PyRSS2Gen import RSS2, RSSItem

# 配置参数
TARGET_REPO_URL = "https://github.com/dw-dengwei/daily-arXiv-ai-enhanced.git" 
SITE_URL = "https://duyifanict.github.io/markdown-monitor"  # 替换为你的Pages地址
REPO_RAW_URL = f"{TARGET_REPO_URL}/raw/main/"  # 用于直接访问Markdown

def generate_feed(changed_files):
    print(changed_files)
    items = []
    
    for rel_path in changed_files:
        file_path = os.path.join("data", rel_path)
        
        if not os.path.exists(file_path):
            continue
            
        # 获取文件修改时间
        mtime = os.path.getmtime(file_path)
        pub_date = datetime.fromtimestamp(mtime)
        
        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            # 尝试解析Front Matter
            try:
                post = frontmatter.loads(content)
                title = post.metadata.get("title", os.path.splitext(rel_path)[0])
                description = post.content[:300] + "..." if len(post.content) > 300 else post.content
            except:
                title = os.path.splitext(rel_path)[0]
                description = content[:300] + "..." if len(content) > 300 else content
        
        # 创建RSS条目
        items.append(RSSItem(
            title=title,
            link=f"{TARGET_REPO_URL}/blob/main/{rel_path}",
            description=f"<pre>{description}</pre>",
            pubDate=pub_date,
            guid=f"{REPO_RAW_URL}{rel_path}"
        ))
    
    # 生成RSS
    rss = RSS2(
        title="Markdown文件更新追踪",
        link=SITE_URL,
        description="自动监控的Markdown变更订阅",
        lastBuildDate=datetime.now(),
        items=items
    )
    
    # 保存RSS文件
    with open("feed.xml", "w", encoding="utf-8") as f:
        rss.write_xml(f)

def path_preprocess(path):
    path = path[1:-1]
    result = []
    for item in  path.split(","):
        item = item.strip().strip('"')
        if item.startswith("data"):
            result.append(item)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(sys.argv[1])
        generate_feed(path_preprocess(sys.argv[1]))
    else:
        print("Error: No changed files data provided")
        sys.exit(1)