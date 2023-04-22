import re
import json

from util.util import read_file

# on macOS, the following encoding is needed to read the files: "utf-8"
audi_html = read_file("../input-extraction/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html", "utf-8")
volvo_html = read_file("../input-extraction/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html", "utf-8")

def regular_expressions(html) -> None:
    print(html)
    # TODO: Implement regular expressions for extracting the following data:
    # Author

    # Published time
    
    # Title

    # Subtitle

    # Lead

    # Content

    # output JSON

def run_regular_expressions() -> None:
    print("Running regular expressions for first page...")
    regular_expressions(audi_html)
    print("Running regular expressions for second page...")
    regular_expressions(volvo_html)
    print("Done.")