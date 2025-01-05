# Analysis
## Determine if the ACM hub is getting bottlenecked; if so why?

- Through the analysis, we want to the return a Yes/No answer or as close to it as possible. 
- And then we need to back it up by relevant charts / tables etc if needed. That is the exact goal of this analysis. 
- We want to move away from the practice of showing lots of charts and tables to the user and let the user infer the result from it. 

### Internal Steps of Analysis

1. We do the data collection, feature extraction, feature engineering etc to gather the right data. 
1. We use the ACM Engineers domain knowledge to create the causal input at acm-inspector/src/analysis/causalrelations/*.json. [Here](./causalrelations/grc_bottleneck.json) is an example.
1. We do the analysis based on the above 2 and create the results under acm-inspector/src/analysis/output

### Running the Analysis
1. First run the acm-inspector/supervisor and make sure the master.csv is created under acm-inspector/output as mentioned [here](/README.md#to-run-this-using-your-own-python-env).
1. Second `cd` to `acm-inspector/src` and run `python -m analysis.entry`
1. High level results are printed out in the terminal. More detailed results are under acm-inspector/src/analysis/output

### Delivery
Above, we lay down how the analysis can be run today. This does not mean that this cannot be changed at a later point of time. Some of the possibilities could be:
1. Can we run this from a container env, so that we do not need a local python environment ?
1. Can we trigger this from ACM User Interface ?
1. Can we trigger this through a Chat/LLM interaction with some additional context?
1. Can we run this analysis on some other data gathered elsewhere ?

The answer to all of the above is - yes, they are very much possible. But as first step, we are focussing on the basic building block now. Once these building blocks are done, they can be wrapped around in numerous ways and reusable across a number of scenarios.



