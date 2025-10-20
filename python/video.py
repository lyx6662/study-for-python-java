
#本程序不以任何盈利目的为前提,仅分享程序,以交流学习心得
#本程序不传递任何传播淫秽信息,如有发现,纯属巧合,请立即删除



import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def get_video_url_optimized(target_url: str):
    """
    使用优化后的 Selenium 配置抓取单个视频的链接。
    """
    print("正在配置详情页浏览器选项...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=3")
    chrome_options.page_load_strategy = 'eager'
    
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"浏览器正在加载页面: {target_url}")
        driver.get(target_url)

        wait = WebDriverWait(driver, 15)
        
        print("正在等待并切换到 iframe...")
        iframe_element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "td#playleft iframe"))
        )
        driver.switch_to.frame(iframe_element)
        print("已成功切换到 iframe。")

        print("正在 iframe 内寻找 video 标签...")
        video_element = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        
        video_src = video_element.get_attribute('src')
        return video_src

    except TimeoutException:
        print(f"抓取超时：在规定时间内未能找到所需元素。")
        return None
    except Exception as e:
        print(f"抓取过程中发生错误: {e}")
        return None
    finally:
        driver.quit()

def main_scraper():
    """
    主爬虫函数，包含所有修复和优化。
    """
    base_url = ""
    current_url = base_url + "/index.php/vod/type/id/14.html"
    
    all_videos_info = []
    page_count = 1

    print("--- [Selenium] 正在启动浏览器以爬取视频列表 ---")
    
    list_options = Options()
    list_options.add_argument('--headless')
    list_options.add_argument('--disable-gpu')
    list_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    list_options.add_argument('--no-sandbox')
    list_options.add_argument('--disable-dev-shm-usage')
    list_options.add_argument("--log-level=3")
    list_options.page_load_strategy = 'eager'
    
    prefs = {"profile.managed_default_content_settings.images": 2}
    list_options.add_experimental_option("prefs", prefs)

    list_driver = webdriver.Chrome(options=list_options)
    
    previous_url = ""
    
    try:
        while current_url and current_url != previous_url:
            print(f"正在爬取列表页 第 {page_count} 页: {current_url}")
            previous_url = current_url
            list_driver.get(current_url)
            
            try:
                WebDriverWait(list_driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.box-item a.item-link"))
                )
                items = list_driver.find_elements(By.CSS_SELECTOR, 'div.box-item a.item-link')
                if not items:
                    print("未在此页面上找到视频项目，结束列表爬取。")
                    break
                
                for item in items:
                    title = item.get_attribute('title')
                    page_href = item.get_attribute('href')
                    all_videos_info.append({'title': title, 'page_url': page_href})

                try:
                    next_page_link_element = list_driver.find_element(By.CSS_SELECTOR, 'a.pagelink_a[title="下一页"]')
                    current_url = next_page_link_element.get_attribute('href')
                    page_count += 1
                    

                    time.sleep(0.5)


                except NoSuchElementException:
                    current_url = None
                    print("已到达最后一页（未找到“下一页”按钮）。")

            except Exception as e:
                print(f"处理页面 {current_url} 时出错: {e}")
                current_url = None
    
    except Exception as e:
        print(f"启动或爬取列表页时发生严重错误: {e}")
    
    finally:
        print("--- 列表页爬取完毕，关闭浏览器 ---")
        list_driver.quit()

    if not all_videos_info:
        print("\n未能从列表页获取到任何视频信息，程序终止。")
        return

    print(f"\n--- 列表爬取完成，共找到 {len(all_videos_info)} 个视频 ---")
    
    print("--- 开始获取每个视频的 m3u8 地址 ---")
    final_data = []
    total_videos = len(all_videos_info)
    
    try:
        for index, video_info in enumerate(all_videos_info):
            print(f"\n正在处理第 {index + 1}/{total_videos} 个视频: 《{video_info['title']}》")
            
            m3u8_url = get_video_url_optimized(video_info['page_url'])
            
            if m3u8_url:
                final_data.append({
                    'title': video_info['title'],
                    'm3u8_url': m3u8_url
                })
                print(f"  ✓ 成功获取到 m3u8 地址!")
            else:
                print(f"  ✗ 未能获取《{video_info['title']}》的 m3u8 地址。")
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n\n检测到用户中断 (Ctrl+C)，程序即将退出...")
    
    finally:
        print("\n--- 进入收尾阶段，正在保存已获取的数据 ---")
        if final_data:
            try:
                with open('video_data.json', 'w', encoding='utf-8') as f:
                    json.dump(final_data, f, ensure_ascii=False, indent=4)
                print(f"\n🎉 成功！数据已保存到 video_data.json 文件中，共 {len(final_data)} 条记录。")
            except IOError as e:
                print(f"保存文件时出错: {e}")
        else:
            print("\n未能获取到任何视频数据，未生成JSON文件。")


if __name__ == "__main__":
    main_scraper()