import unittest
from input_city import city_country


class CityTestCase(unittest.TestCase):

    def test_city_country(self):
        '''能够正确处理像 深圳 中国 这样的表达'''
        # 使用“深圳中国”实参调用要测试的函数，并将结果复制给 get_messages
        get_messages = city_country('深圳', '中国')
        # 断言：判断得到的结果是否与期望的结果一致
        self.assertEqual(get_messages, '深圳 中国')


if __name__ == '__main__':
    unittest.main()
