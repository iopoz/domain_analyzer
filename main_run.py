import os
import unittest

import sys

import sql_scripts as sql
import test_get_data

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

matches = 0


def find_white_domains(param, path):
    global matches
    white_list = []
    strange_domains_list=[]
    temp_list = []
    matches = sql.get_domains_by_name(param)
    try:
        with open(path, 'r') as infile:
            for line in infile:
                temp_list.append(line[:line.find('\n')])
        infile.close()
        for match in matches:
            if match[0] in temp_list:
                white_list.append(match[0])
            else:
                strange_domains_list.append(match[0])
        sql.mark_as_white(white_list)
        sql.mark_as_black(strange_domains_list)
    except:
        print('Mistake in path')



def main(arg1=False, arg2=20, arg3='white_list.txt'):
    if arg1:
        suite = unittest.TestLoader().loadTestsFromModule(test_get_data)
        unittest.TextTestRunner(verbosity=2).run(suite)
    find_white_domains(str(arg2), arg3)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main()
