# Analysis

## Determine if the ACM hub is getting bottlenecked; if so, why?

- The goal of this analysis is to return a **Yes/No** answer (or as close to it as possible) to the question: **"Is my ACM hub currently bottlenecked?"**
- The conclusion will be backed up with relevant charts, tables, and supporting data as needed.

We aim to move away from overwhelming users with a large number of charts and tables, which often requires them to have a deep understanding of how ACM works in order to draw accurate inferences. This current approach reduces the cognitive load on the user by providing high-level answers and supporting information.

## Internal Steps of Analysis

The analysis consists of the following steps:

1. **Data Collection & Preparation**: First, we perform data collection, feature extraction, and feature engineering to gather the relevant data.
1. **Causal Analysis**: Using ACM Engineers' domain knowledge, we create causal input files under `acm-inspector/src/analysis/causalrelations/*.json`. For example, you can see [here](./causalrelations/grc_bottleneck.json) an example of this.
1. **Analysis Execution**: Using the above data and causal relations, we run the analysis. High-level results will be printed out in the terminal during the run. More detailed findings, including charts and tables, will be saved in the `acm-inspector/src/analysis/output` directory.

## Running the Analysis

1. **Step 1**: First, run the `acm-inspector/supervisor` and ensure that the `master.csv` file is created under `acm-inspector/output` as outlined [here](/README.md#to-run-this-using-your-own-python-env).
1. **Step 2**: Navigate to the `acm-inspector/src` directory and run the following command:
   ```bash
   python -m analysis.entry
   ```
1. High level results are printed out in the terminal. More detailed results will be saved in `acm-inspector/src/analysis/output`

## Delivery

This document has explained the current steps for running the analysis. However, there are several potential enhancements or modifications to the process that could be explored in the future:

1. **Can we run this from a containerized environment** so that users do not need a local Python environment (as demonstrated [here](/README.md#using-docker))?
1. **Can we trigger this analysis from the ACM User Interface** to make it more accessible for end-users?
1. **Can we trigger the analysis through a Chat/LLM interface** with added context, allowing users to interact with the system conversationally?
1. **Can we run this analysis on data gathered from external sources?** This would open the analysis to more diverse datasets.

The answer to all of the above is: **Yes, these enhancements are possible.** However, as a first step, we are focusing on establishing the basic building blocks. Once these are in place, the analysis can be easily extended and adapted to a variety of use cases.


