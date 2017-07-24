import unittest
import sql_scripts as sql

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SimpleDomainTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 30)
        self.driver.get("https://domainpunch.com/tlds/daily.php")
        self.domain_list = []
        self.last_page = 0
        self.matches = None

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

    def test_find_white_domains(self):
        self.matches = sql.get_domains_by_name('20')
        pass

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()