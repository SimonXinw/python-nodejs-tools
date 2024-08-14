import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

import os
import time
from datetime import datetime
import random
from urllib.parse import quote


class MajorsScraper:
    def __init__(
        self,
        chrome_driver_path,
        school_name_excel_path,
        js_script_path,
        save_majors_excel_path,
    ):
        self.school_name_excel_path = school_name_excel_path
        self.chrome_driver_path = chrome_driver_path
        self.js_script_path = js_script_path
        self.save_majors_excel_path = save_majors_excel_path
        self.df = None
        self.majors_df = None
        self.school_name = None
        self.row_index = None
        self.url = None
        self.driver = None

    def _init_read_school_name_excel(self):
        # 读取Excel文件
        self.df = pd.read_excel(self.school_name_excel_path)

    def find_row(self, index):
        # 查找指定行的院校名称
        row = self.df.loc[index]

        self.school_name = row["院校名称"]

    def prepare_url(self):
        # 准备要访问的URL，将院校名称插入URL中
        if self.school_name is not None:
            self.url = f"https://www.gaokao.cn/headSearch?search={self.school_name}"

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
            self.majors_df.to_excel(
                self.save_majors_excel_path, index=False, header=False
            )

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

    def close_others_tag_pages(self):
        # 获取当前窗口的句柄
        current_window_handle = self.driver.current_window_handle

        # 获取所有窗口的句柄
        all_window_handles = self.driver.window_handles

        # 遍历所有窗口句柄，关闭除当前窗口外的其他窗口
        for handle in all_window_handles:
            if handle != current_window_handle:
                self.driver.switch_to.window(handle)
                self.driver.close()

        # 切换回当前窗口
        self.driver.switch_to.window(current_window_handle)

    def scrape_web(self):
        try:
            time.sleep(random.uniform(0.3, 0.8))

            self.driver.get(self.url)

            current_url = self.driver.current_url

            encoded_url = quote(self.url, safe=":/?=")

            # 访问的页面被重定向到别的地方，直接中断
            if not encoded_url in current_url:
                print(f"页面跳转失败，页面被重定向了：{self.url} -> {current_url}")
                
                self.df.at[self.row_index, "状态"] = "失败"
                
                return

            # 等待 - 有没有表格详细的行内的单元格
            school_name_selector = (
                ".head-search_schoolSearchItem__vOFho .head-search_schoolName__2ozme em"
            )

            if not self._wait_for_element_update(school_name_selector, 8):
                self.df.at[self.row_index, "状态"] = "失败"

                print("加载失败，找不到院校名称元素，等待超时或其他错误")

                return
            
            # 不要点击那么快
            time.sleep(random.uniform(0.1, 0.3))

            # 找到所有目标类的元素
            school_item = self.driver.find_element(
                By.CSS_SELECTOR, ".head-search_schoolSearchItem__vOFho"
            )

            school_name_element = school_item.find_element(
                By.CSS_SELECTOR, ".head-search_schoolName__2ozme em span"
            )

            # 选出目标学校名称的元素并点击
            if school_name_element.text == self.school_name:
                school_name_element.click()
                
            else:
                print(
                    f"无法点击到 {school_name_element}，请检查 {self.school_name} 是否正确"
                )
                
                self.df.at[self.row_index, "状态"] = "失败"
                
                return

            # 切换页面，新打开的标签页
            self.driver.switch_to.window(self.driver.window_handles[-1])

            shcool_tabbar_selector = ".school-tab_tabNavs__1wdWg img"

            # 等待页面加载出来
            if not self._wait_for_element_update(shcool_tabbar_selector, 6):
                self.df.at[self.row_index, "状态"] = "失败"

                print("页面加载失败，等待超时或其他错误")

                return

            # 执行 JavaScript 函数
            self.driver.execute_script(self.js_code)

            self._wait_for_element_update("#schoolMajorsExcelDataStatus", 64)

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
            self.save_school_name_excel()

            self.close_others_tag_pages()

            print(
                f"爬取完成，当前时间 => {datetime.now().strftime('%Y年%m月%d日 %H时%M分%S秒')}"
            )

    def save_school_name_excel(self):
        # 保存更新后的Excel文件
        self.df.to_excel(self.school_name_excel_path, index=False)

    def _save_majors_result(self):
        # 转换为 Python 的二维列表
        python_2d_list = [list(row) for row in self.school_majors_data]

        new_df = pd.DataFrame(python_2d_list)

        self.majors_df = pd.concat([self.majors_df, new_df], ignore_index=True)

        self.majors_df.to_excel(self.save_majors_excel_path, index=False, header=False)

    def run(self):
        # 计时开始
        self.start_time = time.time()

        # 运行整个爬虫流程
        self._init_driver()

        self._init_js_script()

        self._init_read_majors_excel()

        self._init_read_school_name_excel()

        rows = self.df.iterrows()

        for index, row in rows:
            if row["状态"] != "成功":
                self.row_index = index

                self.find_row(index)

                self.prepare_url()

                self.scrape_web()

                print(f"处理行号: {self.row_index}, 学校名称: {self.school_name}")

        self.save_school_name_excel()

        # 计时结束
        end_time = time.time()

        print(
            f"脚本全部执行完成 >>>>>>>>> 处理总用时: {end_time - self.start_time:.2f} 秒"
        )

        self.driver.quit()


# 示例用法：
if __name__ == "__main__":

    # 获取当前脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))

    school_name_excel_path = os.path.join(current_dir, "还需要爬取的院校.xlsx")

    chrome_driver_path = r"D:\Program Files (x86)\chromedriver-win64\chromedriver.exe"

    # chrome_driver_path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"

    js_script_path = os.path.join(current_dir, "控制台-中国教育-学校专业组.js")

    save_majors_excel_path = os.path.join(current_dir, "院校招生专业组专业明细.xlsx")

    scraper = MajorsScraper(
        chrome_driver_path,
        school_name_excel_path,
        js_script_path,
        save_majors_excel_path,
    )

    scraper.run()
