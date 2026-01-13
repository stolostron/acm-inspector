import pymannkendall as mk
import networkx as nx
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from analysis.utility.charting import *
import statsmodels.api as sm
from statsmodels.stats.diagnostic import linear_rainbow
import ruptures as rpt



def checkIfTrendIsRising(df, metric):
    # A little bit of regression and then check slope
    # We may have to change boolean to a value
    
    #Run Mann-Kendall Test. It is a non parametric test
    
    trend = False
    # Perform the Mann-Kendall test
    result = mk.original_test(df[metric])

    #print(f"Mann-Kendall Test Statistic: {result.z}")
    #print(f"P-value: {result.p}")
    if result.p < 0.05 and result.trend == 'increasing':
        trend = True
        print("There is a statistically significant rising trend in: ",metric)
    else:
        print("No significant trend detected in: ",metric)
    
    return trend

#0.5 sec threshold default
def pctTimeValueIsHigh(df, metric,thresholdValue = 0.5):
    # How many times have this exceeded over a given value
    # How many observations in total
    # Therefore conclude ....
    
    countThresholhExceed = (df[metric] > thresholdValue).sum() 
    totalCount = len(df[metric])
    #print(thresholdValue)
    percentageExceeds = (countThresholhExceed / totalCount) * 100

    print("Threshold Violation analysis for: ",metric, " completed")
    print("The percentage of times it has exceed threshold of ",thresholdValue," sec is: ",percentageExceeds )
    
    return percentageExceeds

def dependsOn(causal_graph_nx, metric):
    metricList= list(causal_graph_nx.predecessors(metric))
    print("Dependency - Metric: ", metric, " depends on ", metricList)
    return metricList

def getMetricList(causal_graph_nx) :
    metricList= list(causal_graph_nx.nodes)
    return metricList

def getImpactedMetricList(causal_graph_nx) :
    # Nodes with no outgoing edges
    leafNodeMetricList = [node for node in causal_graph_nx.nodes if causal_graph_nx.out_degree(node) == 0]

    return leafNodeMetricList

def getDriverMetricList(causal_graph_nx):

    # Find leaf nodes (nodes with no outgoing edges)
    leafNodeMetricList = getImpactedMetricList(causal_graph_nx)

    # Find the metrics that cause the leaf node metrics
    driverMetricSet = set()
    for metric in leafNodeMetricList:
        # Get the nodes that have outgoing edges to the leaf node
        causalList = list(causal_graph_nx.predecessors(metric))
        driverMetricSet.update(causalList)

    # convert set to list
    driverMetricList = list(driverMetricSet)
    
    return driverMetricList

def checkLinearity(df, metric, dependsOn) :
    X = df[dependsOn]  
    y = df[metric]  

    # Add constant to the independent variables (for the intercept term)
    X_with_intercept = sm.add_constant(X)

    # Fit the statsmodel linear regression model (not sklearn regression model)
    model = sm.OLS(y, X_with_intercept).fit()  # Fitting the linear regression model

    # Perform the Rainbow Test for non-linearity
    _, p_value = linear_rainbow(model)

    # Output the p-value of the test
    print(f'Rainbow test p-value: {p_value}')

    # p-value < 0.05: This indicates evidence of non-linearity
    # p-value ≥ 0.05: This suggests that the linear model is appropriate
    if p_value >= 0.5 :
        print("Rainbow test show relationship is Linear")
        return True
    else:
        print("Rainbow test show relationship is Non-Linear !")
        return False

def changeLevelDetection(df,metric) :

    metric_data=df[metric].values
    #print(df.shape[0])
    # Apply the PELT change point detection algorithm
    # Use least squares for detecting changes in mean
    model = "l2"  
    # Fit Model
    algo = rpt.Pelt(model=model).fit(metric_data) 
    # Predict change points with penalty
    # Larger values of pen will penalize the detection of additional change points and 
    # result in fewer change points being detected.
    # Smaller values of pen will allow more change points to be detected, 
    # leading to a more complex model that might overfit the data.
    change_points = algo.predict(pen=10)

    # Display the change points
    print(f"Detected change points: {change_points} for {metric}")
    
    dir = get_output_directory()
    #plt.figure(figsize=(20, 6))
    #plt.plot(metric_data, label='Metric')
    rpt.display(metric_data, change_points)
    plt.title(f"Detected Change Points for {metric}")
    #plt.show()
    plt.savefig(f"{dir}/health-{metric}-changepointdetection.png")
    plt.close('all') 


def runRegression(df, metric, dependsOn) :

    # TODO Scale the variables?
    # TODO Test Linearity of the relationship

    # Calculate the Pearson correlation between all pairs of variables
    correlationMatrix = df.corr()
    #print(correlationMatrix)

    # To get the correlation between each feature and the target variable 
    targetCorrelation = correlationMatrix[metric]
    print(f"Correlation between {metric} and {dependsOn}")
    print(targetCorrelation.loc[dependsOn])   


    #print(type(dependsOn))
    dir = get_output_directory()
    # Independent variable/s. 
    # This is a list with one or more metrics
    X = df[dependsOn]  
    # Dependent variable
    y = df[metric]  

    # Fit the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Get the regression line predictions
    y_pred = model.predict(X)

   
    # Get Predicted/fitted values
    y_pred = model.predict(X)  
    # Get Residuals : Actual - Predicted
    residuals = y - y_pred      

    # Plot the residuals vs. fitted values (predicted values)
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, color='blue', alpha=0.5)
    # Line at y = 0 (ideal)
    plt.axhline(y=0, color='r', linestyle='--')  
    plt.xlabel('Fitted Values (Predicted)')
    plt.ylabel('Residuals')
    plt.title(f"Residual Plot for {metric}")
    plt.savefig(f"{dir}/health-{metric}-residuals.png")
    plt.close('all') 

    # For each feature in dependsOn, create a separate regression plot
    for feature in dependsOn:
        sns.regplot(x=feature, y=metric, data=df)
        plt.title(f'Regression Line for {feature} vs {metric} (Slope: {model.coef_[0]:.2f}, Intercept: {model.intercept_:.2f})')
        #plt.show()
        plt.savefig(f"{dir}/health-{metric}-regression-{feature}.png")
        plt.close('all') 
    
    print(f"Regression coeff between {metric} and {dependsOn}")
    print(f"Slope (quantifies the change in the dependent variable (Y) for a one-unit change in an independent variable (X)): {model.coef_[0]}")
    print(f"Intercept (baseline value of the health metric when causal metrics are 0): {model.intercept_}")

def summarizeBottleneck(df):

    for row in df[df['Bottleneck'] == True].iterrows():
        print(f"System is Bottlenecked is on {row['MetricName']}")
    
    if not df['Bottleneck'].any() == True:
        print("There are no bottlenecks in the system.")
   


def metricBottleneck(trend, threshold):

    if trend or threshold > 50:
        return True
    else :
        return False  

    
