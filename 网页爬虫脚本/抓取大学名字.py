from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from datetime import datetime
import pandas as pd
import os
import time
import random


class UniversityScraper:
    def __init__(self, driver_path, num_urls, save_excel_path):
        self.driver_path = driver_path
        self.num_urls = num_urls
        self.driver = None
        self.results = [["院校名称", "院校代码", "状态", "错误信息"]]
        self.save_excel_path = save_excel_path
        self.start_index = 0
        self._load_existing_results()

    def _load_existing_results(self):
        if os.path.exists(self.save_excel_path):
            df = pd.read_excel(self.save_excel_path, header=None)
            self.start_index = len(df) - 1
            self.results = df.values.tolist()
            print(f"已存在的结果加载成功，继续从第 {self.start_index + 1} 条记录开始")
        else:
            print("未找到已存在的结果文件，从头开始")

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        options.add_argument("--log-level=3")
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 2)

    def _wait_for_element_update(self, selector, timeout=2):
        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            WebDriverWait(self.driver, timeout).until(element_present)
            return True
        except TimeoutException:
            print(f"等待元素 {selector} 超时")
            return False

    def _process_url(self, url):
        try:
            time.sleep(random.uniform(0.5, 1.5))
            self.driver.get(url)

            WebDriverWait(self.driver, 2).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )

            current_url = self.driver.current_url.split("?")[0]
            if current_url != url:
                self.results.append(["", url.split("/")[4], "失败", "页面跳转失败"])
                self._save_results()
                print(f"页面跳转失败：{url} -> {current_url}")
                return

            if not self._wait_for_element_update(".school-tab_name__3pOZK", 2):
                self.results.append(["", url.split("/")[4], "失败", "未找到学校元素，等待超时"])
                self._save_results()
                print("未找到学校元素，等待超时")
                return

            school_name_element = self.driver.find_element(By.CSS_SELECTOR, ".school-tab_name__3pOZK")
            school_name = school_name_element.text
            school_code = url.split("/")[4]

            if school_name:
                self.results.append([school_name, school_code, "成功", ""])
                self._save_results()
                time.sleep(random.uniform(0.5, 1.5))
            else:
                self.results.append(["", school_code, "失败", "院校名称未找到"])
                self._save_results()
            print(f"寻找结果：学校名称：{school_name}")

        except TimeoutException as e:
            self.results.append(["", url.split("/")[4], "失败", "加载超时"])
            self._save_results()
            print(f"处理URL时超时：{url}，错误信息：{e}")
        except WebDriverException as e:
            self.results.append(["", url.split("/")[4], "失败", str(e)])
            self._save_results()
            print(f"处理URL时WebDriver错误：{url}，错误信息：{e}")
        except Exception as e:
            self.results.append(["", url.split("/")[4], "失败", str(e)])
            self._save_results()
            print(f"处理URL时出错：{url}，错误信息：{e}")

    def scrape(self):
        self._init_driver()
        urls = [f"https://www.gaokao.cn/school/{i + 1}" for i in range(self.num_urls)]

        for index in range(self.start_index, self.num_urls):
            url = urls[index]
            print(f"当前访问页面： {index + 1}/{self.num_urls}: {url}")
            self._process_url(url)

        self.driver.quit()

    def _save_results(self):
        df = pd.DataFrame(self.results)
        with pd.ExcelWriter(
            self.save_excel_path,
            engine="openpyxl",
            mode="a" if os.path.exists(self.save_excel_path) else "w",
            if_sheet_exists="overlay",
        ) as writer:
            df.to_excel(writer, index=False, header=False)


if __name__ == "__main__":
    chrome_driver_path = "D:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe"
    num_urls = 5000
    save_excel_path = "D:\\projects\\xw\\python\\python-tools\\网页爬虫脚本\\高考教育院校id_map_表.xlsx"

    scraper = UniversityScraper(chrome_driver_path, num_urls, save_excel_path)
    scraper.scrape()
