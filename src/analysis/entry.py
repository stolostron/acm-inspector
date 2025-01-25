from colorama import Fore, Back, Style
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime
import matplotlib.pyplot as plt
import os
from analysis.bottlenecks.grc import *

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# To run this, go to:
# acm-inspector/src
# python -m analysis.entry

def main():
    print(Back.LIGHTYELLOW_EX+"")
    print("************************************************************************************************")
    print("Starting to Analyze the output of acm-inspector")
    print("************************************************************************************************")
    print(Style.RESET_ALL)

    startGRCAnalysis()

if __name__ == "__main__":
    main()