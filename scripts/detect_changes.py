import os
import json
import hashlib
from filehash import FileHash

def main():
    # 配置路径
    target_dir = "target_repo"
    data_dir = "data"
    hash_file = os.path.join(data_dir, "file_hashes.json")
    
    # 创建数据目录
    os.makedirs(data_dir, exist_ok=True)
    
    # 加载历史哈希
    file_hashes = {}
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            file_hashes = json.load(f)
    
    # 计算当前哈希
    md5hasher = FileHash('md5')
    changed_files = []
    
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, target_dir)
                
                # 计算当前文件哈希
                current_hash = md5hasher.hash_file(file_path)
                
                # 检查变化
                if rel_path not in file_hashes or file_hashes[rel_path] != current_hash:
                    changed_files.append(rel_path)
                    file_hashes[rel_path] = current_hash
                    
                    # 保存文件内容到data目录
                    dest_path = os.path.join(data_dir, rel_path)
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    with open(file_path, "r") as src, open(dest_path, "w") as dest:
                        dest.write(src.read())
    
    # 保存更新后的哈希
    with open(hash_file, "w") as f:
        json.dump(file_hashes, f)
    
    # 设置GitHub Actions输出
    has_changes = "true" if changed_files else "false"
    print(f"::set-output name=has_changes::{has_changes}")
    print(f"::set-output name=changed_files::{json.dumps(changed_files)}")
    
    print(f"Changed files: {len(changed_files)}")

if __name__ == "__main__":
    main()