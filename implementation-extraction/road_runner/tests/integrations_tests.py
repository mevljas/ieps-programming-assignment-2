import contextlib
import sys
import unittest
from io import StringIO

from extractors.helpers.helper import read_file
from road_runner.road_runner_2 import road_runner


class MyTestCase(unittest.TestCase):
    def test_simple_case(self):
        html_1 = read_file("../../../input-extraction/tests/simple_case/page1.html", "utf-8")
        html_2 = read_file("../../../input-extraction/tests/simple_case/page2.html", "utf-8")
        expected_result = read_file("../../../input-extraction/tests/simple_case/result.html", "utf-8")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            road_runner(first_html=html_1, second_html=html_2)
        output = temp_stdout.getvalue().strip()
        print(output)
        self.assertEqual(output, expected_result)

    @unittest.SkipTest
    def test_complex_case(self):
        html_1 = read_file("../../../input-extraction/tests/complex_case/page1.html", "utf-8")
        html_2 = read_file("../../../input-extraction/tests/complex_case/page2.html", "utf-8")
        expected_result = read_file("../../../input-extraction/tests/complex_case/result.html", "utf-8")
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            road_runner(first_html=html_1, second_html=html_2)
        output = temp_stdout.getvalue().strip()
        print(output)
        self.assertEqual(output, expected_result)


if __name__ == '__main__':
    unittest.main()
