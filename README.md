# acm-inspector

## Motivation

Red Hat Advanced Cluster Management (RHACM) is a product that uses several operators, containers, stateful sets etc to managed a fleet of clusters. There is a [must-gather](https://github.com/stolostron/must-gather) script that can gather data from an installation that is having issues and that data can be uploaded for Engineers to debug. However it is not easy to determine the current health of RHACM. If we could to it, perhaps problems could be resolved much faster. This project attempts to solve that problem. If you run `python entry.py prom` you will get a read out of the current state of RHACM.
There is an equally strong secondary motivation that has come up lately. We need an elegant way to collect existing data from a Hub Server that gives an idea of how stressed the system is. From this data, we should be able to infer how much more managed clusters will this Hub cluster be able to handle. 

## Work-in-Progress

This is very much work in progress. 
- As of now, the argument it supports is just `prom`. This stands for `in-cluster Prometheus on the Hub`. We will extend it to ACM Observability Thanos in the very near future. 
- We have begun by looking at a few key operators of RHACM and grabbing the health of those. 
- We have also gathered current snapshot of a few prometheus metrics to check the health of the containers, API Server, etcd. 
- We also gather current snapshot of Prometheus alerts firing on the Hub Server.
- We will continue to expand by looking at the entire set of RHACM operators (MCO, ManifestWork, Placement etc).
- The next few bold steps could be

      - recommending an action to solve the problem by drawing inference from the output. 
      - inferring if the current size of the Hub cluster can handle more managed clusters.
      - inferring a pattern of usage of the Hub from which we could infer a new Hub size if the number of managed clusters increased from say x to 10x (10 to 300)

## Note

Connection to in-cluster Prometheus works from OCP 4.10 upwards. That is because of route changes in open-shift-monitoring namespace.

## To run this

- clone this git repo
- cd src/supervisor
- connect to your OpenShift cluster that runs RHACM by `oc login`. You will need a kubeadmin access.
- install dependencies `pip install -r requirements.txt`
- run `python entry.py prom`
- `if you` run `python entry.py prom 2>&1 | tee ../../output/report.txt` then all the output on the screen will also be redirected to `output/report.txt` file.

### Result

1. `Historical` metric results are created as png & csv files under `output` directory
      - There is `output/breakdown` directory which contains detailed png & csv files containing breakdown metrics for example by namespace or resource etc
      - Under the `output` directory all png & csv files contain metrics are grouped by time `only`
      - This allows us to merge all metrics under a csv called `master.csv` and to create a set of graphs (png) that start with the name `master-*.png`. These visually correlate how the system is performing with time as the number of managed clusters gets added. 
2. `Current` data is printed out in the screen as below:

Note: `True` in the ouput means good status (*though this is not fully working yet*).
```
Starting to Run ACM Health Check -  2022-05-29 09:10:17.130964

============================
MCH Operator Health Check
{'name': 'multiclusterhub', 'CurrentVersion': '2.5.0', 'DesiredVersion': '2.5.0', 'Phase': 'Running', 'Health': True}
 ============ MCH Operator Health Check ============  True
ACM Pod/Container Health Check
      container                              namespace  RestartCount
0       console                open-cluster-management             2
1        restic         open-cluster-management-backup             3
2  thanos-store  open-cluster-management-observability             3
==============================================
                           persistentvolumeclaim   AvailPct
0   alertmanager-db-observability-alertmanager-0  98.102710
1    data-observability-thanos-receive-default-1  99.447934
2               data-observability-thanos-rule-2  97.888564
3      data-observability-thanos-store-shard-2-0  97.913342
4   alertmanager-db-observability-alertmanager-1  98.102710
5            data-observability-thanos-compact-0  99.924190
6    data-observability-thanos-receive-default-0  99.447965
7               data-observability-thanos-rule-0  97.888964
8      data-observability-thanos-store-shard-1-0  98.589732
9                                    grafana-dev  97.843333
10  alertmanager-db-observability-alertmanager-2  98.102710
11   data-observability-thanos-receive-default-2  99.448000
12              data-observability-thanos-rule-1  97.888964
13     data-observability-thanos-store-shard-0-0  98.467535
==============================================
                                     namespace  PodCount
0               open-cluster-management-backup         8
1          open-cluster-management-agent-addon         9
2                  open-cluster-management-hub        12
3                      open-cluster-management        33
4  open-cluster-management-addon-observability         2
5        open-cluster-management-observability        33
6                open-cluster-management-agent         7
=============================================
            instance  etcdDBSizeMB
0  10.0.151.183:9979    325.195312
1   10.0.191.35:9979    325.320312
2   10.0.202.61:9979    326.210938
=============================================
            instance  LeaderChanges
0  10.0.151.183:9979              1
1   10.0.191.35:9979              1
2   10.0.202.61:9979              1
=============================================
                         alertname  value
0  APIRemovedInNextEUSReleaseInUse      3
1                  ArgoCDSyncAlert      3
=============================================
                       resource  APIServer99PctLatency
0        clusterserviceversions               4.290000
1                       backups               0.991571
2                 manifestworks               0.095667
3              multiclusterhubs               0.092000
4                  clusterroles               0.084417
5               managedclusters               0.083000
6                  authrequests               0.081500
7  projecthelmchartrepositories               0.072000
8              apirequestcounts               0.070978
9                     ingresses               0.070000
=============================================
 ============ ACM Pod/Container Health Check  -  PLEASE CHECK to see if the results are concerning!! ============
Managed Cluster Health Check
[{'managedName': 'alpha', 'creationTimestamp': '2022-05-27T19:35:51Z', 'health': True}, {'managedName': 'aws-arm', 'creationTimestamp': '2022-05-16T19:38:43Z', 'health': True}, {'managedName': 'local-cluster', 'creationTimestamp': '2022-05-06T02:25:59Z', 'health': True}, {'managedName': 'machine-learning-team-03', 'creationTimestamp': '2022-05-13T21:41:39Z', 'health': True}, {'managedName': 'pipeline-team-04', 'creationTimestamp': '2022-05-13T21:45:44Z', 'health': True}]
 ============ Managed Cluster Health Check passed ============  False
Checking Addon Health of  alpha
{'managedName': 'alpha', 'cluster-proxy': False, 'observability-controller': False, 'work-manager': False}
 ============ Managed Cluster Addon Health Check passed ============  False
Checking Addon Health of  aws-arm
{'managedName': 'aws-arm', 'application-manager': False, 'cert-policy-controller': False, 'cluster-proxy': False, 'config-policy-controller': False, 'governance-policy-framework': False, 'iam-policy-controller': False, 'managed-serviceaccount': False, 'observability-controller': False, 'search-collector': False, 'work-manager': False}
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