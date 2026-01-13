import matplotlib.pyplot as plt
import pandas as pd
import datetime
from pathlib import Path
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.linear_model import LinearRegression

def get_output_directory():
    # Get the current script's directory
    base_dir = Path(__file__).parent.parent

    output_dir = base_dir / 'output'
    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)  

    return output_dir

def plot(df,metric,metricThreshold) :
        
    dir = get_output_directory()
    if isinstance(dir, Path):
        dir = str(dir)
           
    ax = df.plot(y=metric,figsize=(30, 15) )
    plt.axhline(y=metricThreshold, color='red', linestyle='--', label=f'Threshold: {metricThreshold}')
    plt.savefig(f"{dir}/health-{metric}-trend.png")
    plt.close('all') 

def correlationMatrix(df,  allMetrics) :

    dir = get_output_directory()
    if isinstance(dir, Path):
        dir = str(dir)

    df_delta=df[allMetrics]
    # Generate the correlation matrix
    correlation = df_delta.corr()
    #print(correlation)

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Causal and Health Metrics')
    plt.savefig(f"{dir}/correlationMatrix.png")
    plt.close()

def scatterPlot(df, metric,dependsOn) :
    
    dir = get_output_directory()
    if isinstance(dir, Path):
        dir = str(dir)
    
    #print(type(dependsOn))
    #print(len(dependsOn))

    num_plots = len(dependsOn)
    if num_plots == 0:
        return  
    
    # Create the figure with an appropriate number of subplots
    fig, ax = plt.subplots(1, num_plots, figsize=(6 * num_plots, 6), sharey=True)
    
    # Handle the case when there is only one plot, i.e., not an array of axes
    if num_plots == 1:
        # Make it iterable so the loop can be unified
        ax = [ax] 
    
    # Loop through `dependsOn` and create scatter plots
    for i, dep in enumerate(dependsOn):
        ax[i].scatter(df[dep], df[metric])
        ax[i].set_xlabel(dep)
        ax[i].set_ylabel(metric)
        ax[i].set_title(f"Effect of {dep} on {metric}")
    
    # Adjust layout for better spacing
    plt.tight_layout()
    plt.savefig(f"{dir}/health-{metric}-scatterplot.png")
    plt.close()

    # if len(dependsOn) == 1 :
        
    #     plt.figure(figsize=(12, 6))
    #     plt.scatter(df[dependsOn], df[metric])
    #     plt.xlabel(dependsOn)
    #     plt.ylabel(metric)
    #     plt.title(f"Effect of {dependsOn} on {metric}")
    #     plt.savefig(f"{dir}/health-{metric}-scatterplot.png")
    #     plt.close()
    # elif len(dependsOn) == 2  :
    #     # Create a figure and axes with 1 row and 2 columns (side by side plots)
    #     fig, ax = plt.subplots(1, 2, figsize=(20, 6), sharey=True)

    #     # Scatter plot 1: Effect of RateOfRootPolicySpecChange on RootPolicySpecCtrlResponse95Pctle
    #     ax[0].scatter(df[dependsOn[0]], df[metric])
    #     ax[0].set_xlabel(dependsOn[0])
    #     ax[0].set_ylabel('metric')
    #     ax[0].set_title(f"Effect of {dependsOn[0]} on {metric}")

    #     ax[1].scatter(df[dependsOn[1]], df[metric])
    #     ax[1].set_xlabel(metric)
    #     ax[1].set_title(f"Effect of {dependsOn[1]} on {metric}")

    #     # Adjust the layout for better spacing
    #     plt.tight_layout()
    #     plt.savefig(f"{dir}/health-{metric}-scatterplot.png")
    #     plt.close()

    #     #surfacePlot(df, metric, dependsOn)
    # else  :
    #     # Create a figure and axes with 1 row and 3 columns (side by side plots)
    #     # not attempting to draw more than 3.
    #     # it is very unlikely we will have even 3
    #     fig, ax = plt.subplots(1, 3, figsize=(20, 6), sharey=True)

    #     # Scatter plot 1: Effect of RateOfRootPolicySpecChange on RootPolicySpecCtrlResponse95Pctle
    #     ax[0].scatter(df[dependsOn[0]], df[metric])
    #     ax[0].set_xlabel(dependsOn[0])
    #     ax[0].set_ylabel(metric)
    #     ax[0].set_title(f"Effect of {dependsOn[0]} on {metric}")

    #     ax[1].scatter(df[dependsOn[1]], df[metric])
    #     ax[1].set_xlabel(metric)
    #     ax[1].set_title(f"Effect of {dependsOn[1]} on {metric}")

    #     ax[2].scatter(df[dependsOn[2]], df[metric])
    #     ax[2].set_xlabel(metric)
    #     ax[2].set_title(f"Effect of {dependsOn[2]} on {metric}")

    #     # Adjust the layout for better spacing
    #     plt.tight_layout()
    #     plt.savefig(f"{dir}/health-{metric}-scatterplot.png")
    #     plt.close()    

def surfacePlot(df, metric, dependsOn) :

   
    X = df[dependsOn]
    y = df[metric]

    # Define and train the regression model
    model = LinearRegression()
    model.fit(X, y)

    # Create a meshgrid for the 3D surface plot
    x = np.linspace(df[dependsOn[0]].min(), df[dependsOn[0]].max(), 100)
    y = np.linspace(df[dependsOn[1]].min(), df[dependsOn[1]].max(), 100)
    x, y = np.meshgrid(x, y)

    # Predict health metric values using the regression model
    # Ensure that np.c_ is used correctly to match the feature dimensions
    grid_points = np.c_[x.ravel(), y.ravel()]
    z = model.predict(grid_points)

    # Reshape the predictions back into the grid shape
    z = z.reshape(x.shape)

    # Plot the 3D surface
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surface = ax.plot_surface(x, y, z, cmap='viridis')

    # Label the axes
    ax.set_xlabel(dependsOn[0])
    ax.set_ylabel(dependsOn[1])
    ax.set_zlabel(metric)
    plt.title('3D Effect of Causal Metrics on Health Metric')

    # Show the plot
    plt.show()
