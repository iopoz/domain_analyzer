import unittest
import sql_scripts as sql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StrangeDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.driver_web = webdriver.Chrome()
        self.wait_web = WebDriverWait(self.driver_web, 30)

        mobile_emulation = {"deviceName": "Nexus 5"}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        self.driver_mbl = webdriver.Chrome(chrome_options=chrome_options)
        self.wait_mbl = WebDriverWait(self.driver_mbl, 30)

    def test_get_page(self):
        pass

    def tearDown(self):
        self.driver_web.close()
        self.driver_mbl.close()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(StrangeDomainTestCase, 'test'))
    return suite


if __name__ == "__main__":
    unittest.main()
