# utils.py
import git

def read_file_content(file_path):
    """读取文件内容并返回字符串"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None
    
def clone_repository(repo_url, local_dir):
    """克隆 Git 仓库到本地"""
    try:
        git.Repo.clone_from(repo_url, local_dir)
    except git.exc.GitCommandError as e:
        print(f"Error cloning repository: {e}")
        return False
    return True

    #更新了一下
    #更新了两下
    #更新了三下
