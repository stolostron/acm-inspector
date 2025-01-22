from prometheus_api_client import *
import sys
from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
from common import *
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from supervisor.pvcAnalysis import checkPVCUsage


def checkGlobalHubPVC(start_time, end_time, step):
    print(Back.GREEN + "")
    print(
        "============================================================================================="
    )
    print("Checking Global Hub Components PVCs Usage")
    print(
        "============================================================================================="
    )
    print(Style.RESET_ALL)

    pc = connectProm()

    # totol
    checkPVCUsage(pc, start_time, end_time, step, "multicluster-global-hub")
    # postgres
    checkPVCUsage(
        pc, start_time, end_time, step, "multicluster-global-hub", "postgresdb-.*"
    )
    # kafka broker
    checkPVCUsage(
        pc,
        start_time,
        end_time,
        step,
        "multicluster-global-hub",
        ".*-kafka-kafka-.*",
    )
    # kafka zookeeper
    checkPVCUsage(
        pc,
        start_time,
        end_time,
        step,
        "multicluster-global-hub",
        ".*-kafka-zookeeper-.*",
    )
