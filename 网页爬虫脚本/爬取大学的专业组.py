import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import execjs

import os
import time
import random


class MajorsScraper:
    def __init__(
        self, gaokao_id_excel_path, chrome_driver_path, js_script_path, save_majors_excel_path
    ):
        self.gaokao_id_excel_path = gaokao_id_excel_path
        self.chrome_driver_path = chrome_driver_path
        self.js_script_path = js_script_path
        self.save_majors_excel_path = save_majors_excel_path
        self.df = None
        self.majors_df = None
        self.gaokao_code = None
        self.school_name = None
        self.row_index = None
        self.url = None
        self.driver = None

    def _init_read_gaokao_id_map_excel(self):
        # 读取Excel文件
        self.df = pd.read_excel(self.gaokao_id_excel_path)

    def find_row(self, index):
        # 查找指定行的高考教育映射代码和院校名称
        row = self.df.loc[index]
        self.gaokao_code = row["高考教育映射代码"]
        self.school_name = row["院校名称"]

    def prepare_url(self):
        # 准备要访问的URL，将高考教育映射代码插入URL中
        if self.gaokao_code is not None:
            self.url = f"https://www.gaokao.cn/school/{self.gaokao_code}/provinceline"

    def _init_driver(self):
        # 使用Selenium打开网站，并进行页面的爬取操作
        options = webdriver.ChromeOptions()

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--ignore-ssl-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        options.add_argument("--log-level=3")

        service = Service(self.chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def _init_js_script(self):
        # 读取 JavaScript 文件内容
        with open(self.js_script_path, "r", encoding="utf-8") as f:
            self.js_code = f.read()
            
    def _init_read_majors_excel(self):
        # 读取专业数据 Excel 文件（如果存在）
        if os.path.exists(self.save_majors_excel_path):
            self.majors_df = pd.read_excel(self.save_majors_excel_path)
        else:
            # 如果文件不存在，创建一个空的 DataFrame 并保存为 Excel 文件
            self.majors_df = pd.DataFrame()
            self.majors_df.to_excel(self.save_majors_excel_path, index=False, header=False)

    def _wait_for_element_update(self, selector, timeout=4):
        try:
            element_present = EC.presence_of_element_located(
                (By.CSS_SELECTOR, selector)
            )

            WebDriverWait(self.driver, timeout).until(element_present)

            return True
        except TimeoutException:
            print(f"等待元素 {selector} 超时")
            return False

    def scrape_web(self):
        try:
            time.sleep(random.uniform(0.3, 0.8))

            self.driver.get(self.url)

            current_url = self.driver.current_url.split("?")[0]

            # 访问的页面被重定向到别的地方，直接中断
            if current_url != self.url:
                print(f"页面跳转失败，页面被重定向了：{self.url} -> {current_url}")

                return

            major_table_selector = (
                "#zs_plan .province_score_line_table table tbody tr td"
            )

            # 等待 - 有没有表格详细的行内的单元格
            if not self._wait_for_element_update(major_table_selector, 4):
                self.df.at[self.row_index, "状态"] = "失败"

                print("未找到专业组单元格，等待超时或其他错误")

                return

            # 执行 JavaScript 函数
            self.driver.execute_script(self.js_code)

            WebDriverWait(self.driver, 36).until(
                EC.presence_of_element_located((By.ID, "schoolMajorsExcelDataStatus"))
            )

            # 获取返回值（这里假设函数会将结果存储在一个全局变量中）
            window_school_majors_data = self.driver.execute_script(
                "return window.schoolMajorsExcelData;"
            )

            self.school_majors_data = window_school_majors_data

            self._save_majors_result()

            self.df.at[self.row_index, "状态"] = "成功"

        except TimeoutException as e:
            self.df.at[self.row_index, "状态"] = "失败"
            print(f"处理URL时超时：{self.url}，错误信息：{e}")
        except WebDriverException as e:
            self.df.at[self.row_index, "状态"] = "失败"
            print(f"处理URL时WebDriver错误：{self.url}，错误信息：{e}")
        except Exception as e:
            self.df.at[self.row_index, "状态"] = "失败"
            print(f"处理URL时出错：{self.url}，错误信息：{e}")
        finally:
            self.save_gaokao_map_id_excel()

    def save_gaokao_map_id_excel(self):
        # 保存更新后的Excel文件
        self.df.to_excel(self.gaokao_id_excel_path, index=False, header=False)

    def _save_majors_result(self):
        # 转换为 Python 的二维列表
        python_2d_list = [list(row) for row in self.school_majors_data]
        
        new_df = pd.DataFrame(python_2d_list)

        self.majors_df = pd.concat([self.majors_df, new_df], ignore_index=True)

        self.majors_df.to_excel(self.save_majors_excel_path, index=False, header=False)

    def run(self):
        # 运行整个爬虫流程
        self._init_read_gaokao_id_map_excel()

        self._init_driver()

        self._init_js_script()
        
        self._init_read_majors_excel()

        rows = self.df.iterrows()

        for index, row in rows:
            if row["状态"] != "成功":
                self.row_index = index

                self.find_row(index)

                self.prepare_url()

                self.scrape_web()

                print(
                    f"处理行号: {self.row_index}, 学校名称: {self.school_name}, 高考教育映射代码: {self.gaokao_code}"
                )

        self.save_gaokao_map_id_excel()

        print("所有未成功的行已处理完成并保存。")

        self.driver.quit()


# 示例用法：
if __name__ == "__main__":
    gaokao_id_excel_path = r"C:\Users\simon\Desktop\python-projects\python-tools\网页爬虫脚本\高考教育院校id_map_表.xlsx"

    # chrome_driver_path = r"D:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

    chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"

    js_script_path = r"C:\Users\simon\Desktop\python-projects\python-tools\网页爬虫脚本\控制台-中国教育-学校专业组.js"

    save_majors_excel_path = r"C:\Users\simon\Desktop\python-projects\python-tools\网页爬虫脚本\院校招生专业组专业明细.xlsx"

    scraper = MajorsScraper(
        gaokao_id_excel_path, chrome_driver_path, js_script_path, save_majors_excel_path
    )

    scraper.run()
