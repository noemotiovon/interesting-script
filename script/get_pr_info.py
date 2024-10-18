import requests
import pandas as pd

# 定义用户名称和仓库
# 请在这里输入 GitHub 用户名列表
USER_NAMES = [#'WoosukKwon','youkaichao','simon-mo','DarkLight1337','mgoin',
#              'njhill', 'robertgshaw2-neuralmagic', 'ywang96','rkooo567','Yard1',
              'zhuohan123','tlrmchlsmth'
              #'comaniac','esmeetu','khluu'
              #'pcmoritz','Isotr0py','cadedaniel','dsikka','tdoublep'
              ]  
REPO = 'vllm-project/vllm'        # 仓库名称（可修改）
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXX'  # 设置用户TOKEN（可修改）
OUTPUT_FILE = 'vllm_prs.xlsx'   # 导出结果的文件名（可修改）
NAME_TO_REAL_NAME = {}

# 设置请求头
headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_user_info(username):
    # 获取用户的真实姓名
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('name', username)  # 返回真实姓名，若没有则返回用户名
    else:
        print(f"Error fetching user info for {username}: {response.status_code} - {response.text}")
        return username  # 出错时返回用户名作为默认值

def get_user_prs(usernames, repo):
    # GitHub API URL
    url = f'https://api.github.com/repos/{repo}/pulls'
    
    # 存储用户的 PR 信息
    user_prs = []

    # 获取用户的真实姓名
    for username in usernames:
        real_name = get_user_info(username)
        NAME_TO_REAL_NAME[username] = real_name
    
    page = 1
    while True:
        # 请求指定页的 PR
        response = requests.get(url, headers=headers, params={'state': 'closed','page': page, 'per_page': 100})
        print(page)
        if response.status_code == 200:
            prs = response.json()
            if not prs:
                print(f"last page: {page}")
                break  # 如果没有更多 PR，退出循环
            
            for pr in prs:
                # 检查 PR 的创建者用户名
                if pr['user']['login'] in usernames:
                    username = pr['user']['login']
                    user_prs.append({
                        'username': username,
                        'real_name': NAME_TO_REAL_NAME[username],  
                        'title': pr['title'],
                        'packages': extract_package_names(pr['number'], repo, headers)
                    })
            page += 1  # 增加页码以请求下一页
        else:
            print(f"Error fetching PRs: {response.status_code} - {response.text}")
            break
    
    return user_prs

def extract_package_names(pr_number, repo, headers):
    # 获取指定 PR 的文件信息
    url = f'https://api.github.com/repos/{repo}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        files = response.json()
        # 提取 vllm 目录下的一级子包名
        package_names = set()
        for file in files:
            file_path = file['filename']
            # 只提取 vllm/ 下的一级子包
            if file_path.startswith('vllm/'):
                subdirs = file_path.split('/')
                if len(subdirs) > 1:
                    package_names.add(subdirs[1])  # 提取 vllm 下的一层包名
        return ', '.join(package_names)  # 返回以逗号分隔的包名
    else:
        print(f"Error fetching files for PR {pr_number}: {response.status_code} - {response.text}")
        return ''

def main():
    all_prs = []
    prs = get_user_prs(USER_NAMES, REPO)
    all_prs.extend(prs)
        
    # 将结果导出到 Excel
    if all_prs:
        df = pd.DataFrame(all_prs)
        df.to_excel(OUTPUT_FILE, index=False, columns=['username', 'real_name', 'title', 'packages'])
        print(f"Data exported to {OUTPUT_FILE}.")
    else:
        print(f"No PRs found for users: {', '.join(USER_NAMES)}.")

if __name__ == "__main__":
    main()