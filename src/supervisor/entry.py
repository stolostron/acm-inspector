    
from mch import *       
from container import *
from managedCluster import *
from node import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from datetime import datetime

 

# pass debug(boolean) as env
def main():
    now = datetime.now()
    print("Starting to Run ACM Health Check - ",now," \n")
    print("============================")
    mch = checkMCHStatus()
    cont = checkACMContainerStatus()
    mc = checkManagedClusterStatus()
    node = checkNodeStatus()
    print("============================")
    print("\n End ACM Health Check")

if __name__ == "__main__":
    main()