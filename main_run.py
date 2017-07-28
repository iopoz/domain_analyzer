import sys
import unittest

import src.sql_scripts as sql

from src import test_get_data, test_get_page_from_browser

matches = 0


def find_white_domains(param, path):
    global matches
    white_list = []
    strange_domains_list = []
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
        with open('temp.txt', 'x') as black_list:
            for domain in strange_domains_list:
                black_list.write(domain + '\n')
        black_list.close()
    except:
        print('Mistake in path')


def get_pages():
    suite = unittest.TestLoader().loadTestsFromModule(test_get_page_from_browser)
    unittest.TextTestRunner(verbosity=2).run(suite)


def main(arg1=False, arg2=20, arg3='white_list.txt'):
    if arg1:
        suite = unittest.TestLoader().loadTestsFromModule(test_get_data)
        unittest.TextTestRunner(verbosity=2).run(suite)
    find_white_domains(str(arg2), arg3)
    get_pages()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main()
