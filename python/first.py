# 导入所有需要的库，注意新增了 selenium
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# ===================================================================
# 【第一步: 初始化 Selenium】
# 在所有循环开始之前，启动一个浏览器实例。
# 就像你开始上网前，会先打开一个浏览器窗口一样。
# ===================================================================
print("正在启动浏览器...")
driver = webdriver.Chrome()
print("浏览器启动成功！")


# --- 下面的变量定义和你原来的一样 ---
start_url = 'https://www.17k.com/chapter/3583700/48584344.html'
base_domain = 'https://www.17k.com'
next_page_url = start_url

# 在这里，我们把整个爬虫逻辑放到一个 try...finally 结构中
# 这样做的好处是：无论程序是正常结束还是中途报错，
# finally 块中的 driver.quit() 都一定会被执行，确保浏览器能被正确关闭。
try:
    with open('星辰之门.txt', 'a', encoding='utf-8') as f:
        while next_page_url:
            
            # ===================================================================
            # 【第二步: 使用 Selenium 替换 requests 来获取网页】
            # 这是最核心的修改！
            # ===================================================================
            print(f"浏览器正在加载页面：{next_page_url}")
            
            # 命令浏览器打开页面
            driver.get(next_page_url)
            
            # 【重要】强制等待3秒。因为网速和电脑性能不同，需要给JS足够的时间去加载内容。
            # 如果内容还是出不来，可以适当增加这个时间，比如 time.sleep(5)
            time.sleep(3)
            
            # 从浏览器获取加载完成后的HTML源代码
            html_content = driver.page_source

            # --- 从这里开始，后面的所有代码几乎和你原来的一模一样！---
            # 因为我们已经拿到了完整的HTML，接下来的解析工作没有变化。
            
            soup = BeautifulSoup(html_content, 'html.parser')

            # ===================================================================
            # 【代码修正部分】
            # 我们将获取标题和正文的逻辑合并在一起，使其更加稳健。
            # ===================================================================

            # 1. 首先，定位到包含标题和所有正文段落的那个最大的<div>容器
            #    根据网页源码，这个容器的 class 是 'readAreaBox content'
            content_div = soup.find('div', class_='readAreaBox content')
            
            # 如果这个最主要的容器都找不到，那说明页面结构发生重大变化，直接结束程序
            if not content_div:
                print("本页没有找到小说内容容器，爬虫结束")
                break
            
            # 2. 获取章节标题
            #    标题<h1>标签就在我们刚刚找到的 content_div 容器里面，并且它本身没有class
            chapter_title_tag = content_div.find('h1')
            if chapter_title_tag:
                chapter_title = chapter_title_tag.get_text().strip()
                print(f"成功获取章节：{chapter_title}")
                f.write(chapter_title + '\n\n')
            else:
                # 即使没有标题，我们也可以选择继续爬取正文，所以这里只打印提示，不退出
                print("未在内容区域内找到章节标题")

            # 3. 获取小说正文
            #    直接在已经找到的 content_div 容器里查找所有的<p>标签
            paragraphs = content_div.find_all('p')
            print(f"找到 {len(paragraphs)} 个段落")

            for p in paragraphs:
                paragraph_text = p.get_text().strip()
                # 增加一个判断，避免将网站的推广信息也写入文件
                if "本书首发来自17K小说网" not in paragraph_text:
                    f.write(paragraph_text + '\n')
            
            f.write('\n\n')

            # 4. 寻找下一页
            #    这部分逻辑保持不变
            next_page_li = soup.find('li', class_='next')
            if next_page_li and next_page_li.find('a'):
                relative_link = next_page_li.find('a').get('href')
                next_page_url = urljoin(base_domain, relative_link)
                print(f"找到下一章链接：{next_page_url}")
            else:
                print("没有'下一章'按钮了，结束爬取")
                next_page_url = None # 设为None以结束while循环

finally:
    # ===================================================================
    # 【第三步: 关闭浏览器】
    # 当所有循环结束后，或者程序出现异常时，关闭浏览器，释放资源。
    # ===================================================================
    print("所有任务完成，正在关闭浏览器...")
    driver.quit()
    print("*" * 20 + "\n" + "爬取结束，内容已保存到 '星辰之门.txt'")