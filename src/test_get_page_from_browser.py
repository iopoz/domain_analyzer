import os
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def search_folder(end_folder):
    path = os.path.abspath(os.curdir)
    while path:
        for root, dirs, files in os.walk(path, topdown=True):
            if end_folder in root:
                return os.path.join(root[0:root.find(end_folder)], end_folder)
        path = os.path.dirname(path)


class StrangeDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.driver_web = webdriver.Chrome()
        self.wait_web = WebDriverWait(self.driver_web, 30)

        mobile_emulation = {
            "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
        chrome_options = Options()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver_mbl = webdriver.Chrome(chrome_options=chrome_options)
        self.wait_mbl = WebDriverWait(self.driver_mbl, 30)

        self.strange_domain_list = []

    def test_general(self):
        folder_img = search_folder('domain_images')
        folder_tmp = search_folder('tmp')
        with open(os.path.abspath(os.path.join(folder_tmp, "temp.txt")), 'r') as f:
            for line in f:
                self.get_page(folder_img, line[:line.find('\n')])
        f.close()

    def get_page(self, folder, domain):
        self.driver_web.get('http://%s' % domain)
        title = self.driver_web.title
        self.driver_web.get_screenshot_as_file(os.path.join(folder, '-'.join(['web', domain, title])+'.png'))

        self.driver_mbl.get('http://%s' % domain)
        title = self.driver_mbl.title
        self.driver_mbl.get_screenshot_as_file(os.path.join(folder, '-'.join(['mbl', domain, title])+ '.png'))

    def tearDown(self):
        self.driver_web.close()
        self.driver_mbl.close()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StrangeDomainTestCase, 'test'))
    return suite


if __name__ == "__main__":
    unittest.main()
