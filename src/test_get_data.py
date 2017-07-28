import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src import sql_scripts as sql


class SimpleDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://domainpunch.com/tlds/daily.php")
        self.domain_list = []
        self.last_page = 0

    def test_collect(self, page=2):
        self.wait.until_not(EC.visibility_of_element_located((By.ID, 'domtable_processing')))
        domains = self.driver.find_elements_by_css_selector('#tablewrap td:nth-child(2)')
        for domain in domains:
            self.domain_list.append(domain.text)
        sql.add_new_domain(self.domain_list)

        next_pages = self.driver.find_elements_by_css_selector('#domtable_paginate > span > a')
        for next_page in next_pages:
            if int(next_page.text) == page:
                self.last_page = next_page.text
                next_page.click()
                self.domain_list = []
                break
        if int(self.last_page) < page:
            return
        self.test_collect(page + 1)

    def tearDown(self):
        self.driver.close()


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleDomainTestCase, 'test'))
    return suite


if __name__ == "__main__":
    unittest.main()
