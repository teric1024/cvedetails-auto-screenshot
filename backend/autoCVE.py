#!/usr/bin/python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import shutil
from pathlib import Path

DATA_DIR = './data'

def del_pic(screenshot_dir):
    pic_list = os.listdir(screenshot_dir)
    for pic in pic_list:
        os.remove(screenshot_dir + pic)

def run_web_driver():
    #瀏覽器參數設定
    option = webdriver.ChromeOptions()
    # disable-infobars (解bug)
    option.add_argument("disable-infobars")
    option.add_argument("--disable-gpu") 
    option.add_argument("--disable-extensions")
    option.add_argument("--disable-notifications")
    option.add_argument('--no-sandbox')
    option.add_argument("--disable-setuid-sandbox")
    option.add_argument('--disable-dev-shm-usage')
    option.add_experimental_option("excludeSwitches", ['enable-automation'])

    #背景執行
    option.add_argument("--headless")

    #舊版寫法
    #driver = webdriver.Chrome("./chromedriver.exe", options=option)

    #設定chromedriver 路徑
    s = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s, options=option)
    
    
    print("Chrome version:", driver.capabilities['browserVersion'])
    print("ChromeDriver version:", driver.capabilities['chrome']['chromedriverVersion'])
    
    #chrome size 設定
    driver.set_window_size(1024, 803)

    #cvedetails 網址
    driver.get("https://www.cvedetails.com/") 
    time.sleep(1)
    #關閉cookie提示
    driver.execute_script("cookieconsentReject()")
    
    return driver

def process_packages(site_list):
    site_list = [site.strip().replace("官方原生提供", "") for site in site_list]
    return site_list

def prepare_screenshot_dir(screenshot_dir:Path):
    if os.path.exists(screenshot_dir):
        shutil.rmtree(screenshot_dir)
    os.makedirs(screenshot_dir)

def screenshot(packages, screenshot_dir='pic', zip_file='cve'):
    driver = run_web_driver()
    site_list = process_packages(packages)
    screenshot_dir = Path(DATA_DIR) / screenshot_dir 
    zip_file = Path(DATA_DIR) / zip_file
    prepare_screenshot_dir(screenshot_dir)

    #讀取url依序執行security header 檢測
    for i in range(0, len(site_list)):
        driver.find_element('id', 'unifiedsearchinput').send_keys(str(site_list[i]))
        time.sleep(2)

        # #設定winodws大小
        # driver.execute_script('window.scrollBy(0,200)')
        #圖片儲存
        driver.save_screenshot(os.path.join(screenshot_dir, str(i+1) + ".png"))
        
        #清空搜尋欄
        try:
            driver.find_element('id', 'unifiedsearchinput').clear()
        except Exception as e:
            print ("Exception found", format(e))
        
    driver.close()
    zip_file = shutil.make_archive(zip_file, 'zip', screenshot_dir)
    print("""
    __ _       _     _              _ 
    / _(_)     (_)   | |            | |
    | |_ _ _ __  _ ___| |__   ___  __| |
    |  _| | '_ \| / __| '_ \ / _ \/ _` |
    | | | | | | | \__ \ | | |  __/ (_| |
    |_| |_|_| |_|_|___/_| |_|\___|\__,_|
    """)
    return Path(zip_file)

def main():
    package_file = "./packages.txt"
    #開啟packages.txt
    with open(package_file, "r", encoding="utf-8") as f:
        site_list = f.readlines()
        screenshot(site_list)

if __name__ == "__main__":
    main()