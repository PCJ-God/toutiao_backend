import os

dist_dir = r'E:\vscode代码\toutiao_backend\fastAPI\day03_AI掘金头条-新闻模块\项目物料\03-前端项目代码\xwzx-news\dist\assets'

for fname in os.listdir(dist_dir):
    if fname.endswith('.js'):
        path = os.path.join(dist_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'=== {fname} ({len(content)} bytes) ===')
        # Search for API URL
        for keyword in ['101.35.89.37', '127.0.0.1', 'localhost', 'baseURL', 'VITE_API', 'picsum']:
            count = content.count(keyword)
            if count > 0:
                print(f'  {keyword}: {count}')
                # Find the surrounding context
                idx = content.find(keyword)
                start = max(0, idx - 50)
                end = min(len(content), idx + 100)
                print(f'  Context: ...{content[start:end]}...')
        print()