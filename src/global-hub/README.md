# Global Hub Inspector

The inspector is inspired by [acm-inspector](https://github.com/bjoydeep/acm-inspector). It aims to easily obtain the operating status of the global hub and determine the health of the system, so as to support exploring the scalability.

## Prerequisites

1. Set the `KUBECONFIG` so that you can connect the OCP.
2. Expose the postgres endpoint to allow get the database connection. 

    ```yaml
    cat <<EOF | oc apply -f -
    apiVersion: v1
    kind: Service
    metadata:
      name: multicluster-global-hub-postgres-lb
      namespace: multicluster-global-hub
    spec:
      ports:
      - name: postgres
        port: 5432
        protocol: TCP
        targetPort: 5432
      selector:
        name: multicluster-global-hub-postgres
      type: LoadBalancer
    EOF
    ```

3. The `python` and the tool `pip` have been installed on your environment.
4. Enable the `Prometheus` on your global hub.
5. Running the `pip install -r ./src/global-hub/requirements.txt` to install dependencies.

## Running the inspector

### Count the records of database
   
  - Start a backend process to count the records
    
    The statistical data includes:

    1. The count of the managed clusters from all the hubs
    2. The count of the events from Replicas policies
    3. The count of the compliances from all the replicas polices
    3. The count of the compliant and non-compliant polices when rotating the policies status
  
    ```bash
    # override the previous csv file
    ./src/global-hub/cmd/counter.sh start
    # append the count result to the previous files
    ./src/global-hub/cmd/counter.sh continue
    ```
  
  - Draw the count results [ Optional: The picture also generate in the next step ]

    ```bash
    ./src/global-hub/cmd/counter.sh draw
    ```
  
  - Stop the backend process
  
    ```bash
    ./src/global-hub/cmd/counter.sh stop
    ```

### Get CPU and Memory information

  ```bash
  # The time range is from seven days ago to the current time
  ./src/global-hub/cmd/check.sh 

  # The time range from the "2023-09-18 00:00:00" to the current time
  ./src/global-hub/cmd/check.sh "2023-09-18 00:00:00"

   # The time range from the "2023-09-18 00:00:00" to the "2023-09-20 00:00:00"
  ./src/global-hub/cmd/check.sh "2023-09-18 00:00:00" "2023-09-20 00:00:00"

  # For the global hub agent
  ./src/global-hub/cmd/check_agent.sh
  ```

All the csv file and picture will be save on the folder `./src/global-hub/output`


## Note

This has been tested using Python 3.11.4 on OCP 4.12.18.