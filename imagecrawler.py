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
        driver.implicitly_wait(1.0 + random.random() * 1.0)
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


def google_search_func(driver, search_keyword):
    driver.get('https://www.google.com/search?q=' + search_keyword + '&tbm=isch')


default_search_func = google_search_func


def google_parse_func(driver):
    image_urls = []
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
    return image_urls


default_parse_func = google_parse_func


def search_images_url(driver, search_keyword, search_func=None, parse_func=None):
    if search_func is None:
        search_func = default_search_func
    search_func(driver, search_keyword)
        
    show_all_page(driver)

    if parse_func is None:
        parse_func = default_parse_func

    return default_parse_func(driver)


def search_images_urls(driver, search_keywords, search_func=None, parse_func=None):
    keyed_image_urls = { }

    if isinstance(search_keywords, str):
        keyed_image_urls[search_keywords] = search_images_url(driver, search_keywords)
        return keyed_image_urls

    for kw in search_keywords:
        image_urls = search_images_url(driver, kw, search_func, parse_func)
        keyed_image_urls[kw] = image_urls
    return keyed_image_urls


