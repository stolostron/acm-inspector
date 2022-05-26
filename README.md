# acm-inspector

## Motivation
Red Hat Advanced Cluster Management (RHACM) is a product that uses several operators, containers, stateful sets etc to managed a fleet of clusters. There is a must-gather script that can gather data from an installation that is having issues and that data can be uploaded for Red Hat Engineers to debug. However there is a not an easy way by which you can determine the health of RHACM as is now. And if we did that, perhaps problems could be resolved much faster. This project attempts to solve that problem. If you run `python entry.py` you will get a read out of the current state of RHACM.

## Work-in-Progress
This is very much work in progress. 
- We have begun by looking at a few Key operators of RHACM and grabbing the health from those. 
- Next we will look at the prometheus metrics to grab the health of the containers. 
- We will continue to expand by looking at the entire set of RHACM operators.
- The next bold step could be recommending an action to solve the problem.

## To run this
- clone this git repo
- cd src/supervisor
- connect to your OpenShift cluster that runs RHACM by `oc login`
- run `python entry.py`
You will get an output like:
```
➜  supervisor git:(main) python entry.py
Starting to Run ACM Health Check -  2022-05-26 07:40:47.426542

============================
MCH Operator Health Check
{'name': 'multiclusterhub', 'CurrentVersion': '2.5.0', 'DesiredVersion': '2.5.0', 'Phase': 'Running', 'Health': True}
 ============ MCH Operator Health Check ============  True
ACM Pod/Container Health Check
 ============ ACM Pod/Container Health Check passed -  UNDER DEVELOPMENT - IGNORE FOR NOW!! ============
Managed Cluster Health Check
[{'managedName': 'aws-arm', 'creationTimestamp': '2022-05-16T19:38:43Z', 'health': True}, {'managedName': 'build-team-02', 'creationTimestamp': '2022-05-13T21:56:26Z', 'health': True}, {'managedName': 'elpaso', 'creationTimestamp': '2022-05-15T04:03:14Z', 'health': True}, {'managedName': 'local-cluster', 'creationTimestamp': '2022-05-06T02:25:59Z', 'health': True}, {'managedName': 'machine-learning-team-03', 'creationTimestamp': '2022-05-13T21:41:39Z', 'health': True}, {'managedName': 'pipeline-team-04', 'creationTimestamp': '2022-05-13T21:45:44Z', 'health': True}]
 ============ Managed Cluster Health Check passed ============  True
Checking Addon Health of  aws-arm
{'managedName': 'aws-arm', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'managed-serviceaccount': False, 'observability-controller': False, 'search-collector': True, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  build-team-02
{'managedName': 'build-team-02', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'managed-serviceaccount': True, 'observability-controller': False, 'search-collector': True, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  elpaso
{'managedName': 'elpaso', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'observability-controller': False, 'search-collector': True, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  local-cluster
{'managedName': 'local-cluster', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'observability-controller': False, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  machine-learning-team-03
{'managedName': 'machine-learning-team-03', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'managed-serviceaccount': True, 'observability-controller': False, 'search-collector': True, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  pipeline-team-04
{'managedName': 'pipeline-team-04', 'application-manager': True, 'cert-policy-controller': True, 'cluster-proxy': True, 'config-policy-controller': True, 'governance-policy-framework': True, 'iam-policy-controller': True, 'managed-serviceaccount': True, 'observability-controller': False, 'search-collector': True, 'work-manager': True}
 ============ Managed Cluster Addon Health Check passed ============  False
Node Health Check
{'name': 'ip-10-0-133-168.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
{'name': 'ip-10-0-151-183.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
{'name': 'ip-10-0-176-78.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
{'name': 'ip-10-0-191-35.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
{'name': 'ip-10-0-196-178.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
{'name': 'ip-10-0-202-61.us-east-2.compute.internal', 'MemoryPressure': 'False', 'DiskPressure': 'False', 'PIDPressure': 'False', 'Ready': 'True'}
 ============ Node Health Check passed ============  True
============================

 End ACM Health Check
 ```
## Please contribute!
This is an open invitation to all RHACM users and developers to start to contribute so that we can acheive the end goal faster and improve this!