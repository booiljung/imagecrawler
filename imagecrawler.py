"""This module retrieves images from search engines and stores them in { key: [], ...} data types and returns them.

If the internet is slow, it may not change for 1 second.
I do not know how to check because I indirectly crawl using selenium.
"""

import random
from selenium import webdriver
import urllib.parse


def wait_page_downloading(driver):
    """Wait for the web page to finish downloading.
    """
    old_page = driver.page_source
    while True:
        driver.implicitly_wait(0.5 + random.random() * 1.0)
        new_page = driver.page_source
        if new_page != old_page:
            old_page = new_page
        else:
            break


def scroll_down_all(driver):
    """Scroll down to the bottom of the web page until it is finished downloading.
    """
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
    """
    Show all Google image search pages.
    """
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
    """Search for keywords in the Google search engine.
    If there is no browser instance, open a new instance and use the instance if it exists.
    """
    driver.get('https://www.google.com/search?q=' + search_keyword + '&tbm=isch')


default_search_func = google_search_func


def google_parse_func(driver):
    """Parse Google image search results to get url of image as list.
    Result is [ url, ... ]
    """
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
    """Query the search engine for a keyword to get the image URLs.
    The result is a list data type.
    """
    if search_func is None:
        search_func = default_search_func
    search_func(driver, search_keyword)
        
    show_all_page(driver)

    if parse_func is None:
        parse_func = default_parse_func

    return default_parse_func(driver)


def search_images_urls(driver, search_keywords, search_func=None, parse_func=None):
    """Search engines sequentially query multiple keywords to obtain image URLs.
    The result is the { key: [], ... } datatype.
    search_keywords is either a keyword or a list of keywords.
    """
    keyed_image_urls = { }

    if isinstance(search_keywords, str):
        keyed_image_urls[search_keywords] = search_images_url(driver, search_keywords)
        return keyed_image_urls

    for kw in search_keywords:
        image_urls = search_images_url(driver, kw, search_func, parse_func)
        keyed_image_urls[kw] = image_urls
    return keyed_image_urls

