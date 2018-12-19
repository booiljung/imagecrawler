import random
from selenium import webdriver
import urllib.parse

# 인터넷이 느린 경우 1초동안 변화가 없을 수 있는데 다운로드 완료 한것으로 오판할 위험이 있음.

def wait_page_downloading(driver):
    old_page = driver.page_source
    while True:
        driver.implicitly_wait(0.5 + random.random() * 1.0)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break


def scroll_down_all(driver):
    old_pos = driver.execute_script("return window.pageYOffset;")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(0.5 + random.random() * 1.0)
        wait_page_downloading(driver)
        new_pos = driver.execute_script("return window.pageYOffset;")
        if old_pos != new_pos:
            old_pos = new_pos
        else:
            break


def show_all_page(driver):
    wait_page_downloading(driver)
    while True:
        scroll_down_all(driver)
        driver.implicitly_wait(2.5 + random.random() * 2.0)
        input = driver.find_element_by_id("smb")
        if input is None:
            break
        if not input.is_displayed():
            break
        input.click()
        driver.implicitly_wait(2.5 + random.random() * 2.0)


def search_images_urls(driver, search_keywords):
    keyed_image_urls = { }
    for kw in search_keywords:
        image_urls = []
        driver.get('https://www.google.com/search?q=' + kw + '&tbm=isch')
        show_all_page(driver)
        a_elements = driver.find_elements_by_tag_name('a')
        for a_ele in a_elements:
            jsname_attr = a_ele.get_attribute('jsname')
            if jsname_attr != "hSRGPd":
                continue
            href_attr = a_ele.get_attribute('href')
            if href_attr is None:
                continue
            href_urls = href_attr.split('?')
            if len(href_urls) <= 1:
                continue
            split_urls = href_urls[1].split('&')
            if 1 <= len(split_urls):
                if split_urls[0].startswith('imgurl='):
                    imgurl = split_urls[0][7:]
                    imgurl = urllib.parse.unquote(imgurl)
                    image_urls.append(imgurl)
        keyed_image_urls[kw] = image_urls
    return keyed_image_urls


chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('headless')
chrome_options.add_argument('--window-size=1024,1024')
#chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
chrome_options.add_argument("--lang=en_US")
#chrome_options.add_argument("--lang=ko_KR")

driver = webdriver.Chrome('/home/booil/Downloads/chromedriver', chrome_options=chrome_options)
driver.implicitly_wait(3)

founds = search_images_urls(driver, ['얼룩말', '연필'])
print(founds)


"""
결과 더보기
<input class="ksb" value="결과 더보기" id="smb" data-lt="로드 중..." type="button" data-ved="0ahUKEwi8qae8vanfAhUH5LwKHdWIBT4QxdoBCIoC">
<a href="https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.freeimages.com%2Fimages%2Fpremium%2Fpreviews%2F4642%2F46422546-zebra-tail.jpg&imgrefurl=https%3A%2F%2Fkr.freeimages.com%2Fpremium%2Fzebra-tail-1645948&docid=cLwRlTsZYWc6VM&tbnid=hFbKGYP_dua6VM%3A&vet=10ahUKEwic3eXZv6vfAhVFyLwKHYZaBPEQMwisAiheMF4..i&w=681&h=1024&bih=893&biw=1016&q=%EC%96%BC%EB%A3%A9%EB%A7%90&ved=0ahUKEwic3eXZv6vfAhVFyLwKHYZaBPEQMwisAiheMF4&iact=mrc&uact=8">
"""