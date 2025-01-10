from datetime import datetime, timedelta
import pytz
from colorama import Back, Style
import sys

from cpuUsage import *
from memoryUsage import *
from pvcUsage import *


# pass debug(boolean) as env
def main():
    start_time = datetime.now(pytz.utc) - timedelta(days=7)
    end_time = datetime.now(pytz.utc)
    step = "1m"

    try:
        if len(sys.argv) >= 2 and sys.argv[1] != "":
            start_time = datetime.strptime(sys.argv[1], "%Y-%m-%d %H:%M:%S")
        if len(sys.argv) >= 3 and sys.argv[2] != "":
            end_time = datetime.strptime(sys.argv[2], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS'.", sys.argv)

    print(Back.BLUE + "")
    current = datetime.now().strftime("%H:%M:%S")
    print("************************************************************************")
    print(f"""[ {current} ] Start GH Inspector: {start_time} - {end_time}""")
    print("************************************************************************")
    print(Style.RESET_ALL)

    config.load_kube_config()
    checkGlobalHubCpu(start_time, end_time, step)
    checkGlobalHubMemory(start_time, end_time, step)
    checkGlobalHubPVC(start_time, end_time, step)

    print(Back.BLUE + "")
    current = datetime.now().strftime("%H:%M:%S")
    print("************************************************************************")
    print(f"""[ {current} ] End GH Inspector: {start_time} - {end_time}""")
    print("************************************************************************")
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
