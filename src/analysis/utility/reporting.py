import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from pathlib import Path
from reportlab.lib.units import inch
import datetime
from analysis.utility.causalExtractor import *

def get_output_directory():
    # Get the current script's directory
    base_dir = Path(__file__).parent.parent

    output_dir = base_dir / 'output'
    # Create the directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)  

    return output_dir

# Function to add text to PDF
def add_text_to_pdf(pdf_filename, flowables):
    if isinstance(pdf_filename, Path):
        pdf_filename = str(pdf_filename)

    document = SimpleDocTemplate(pdf_filename, pagesize=letter)
    document.build(flowables)

# Function to create a table from a dataframe
def create_table_from_dataframe(df):
    data = [df.columns.tolist()] + df.values.tolist()  # Prepare table data
    table = Table(data)
    
    # Table style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(style)
    return table

# Function to generate a Matplotlib chart (example: simple line chart)
def create_matplotlib_chart_sample():
    fig, ax = plt.subplots()
    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]
    ax.plot(x, y)
    ax.set_title("Sample Line Chart")
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close(fig)
    
    return img_buffer

# Function to generate a Matplotlib chart (example: simple line chart)
def create_matplotlib_chart(df,metric1):

    plt.figure(figsize=(30,10))
    #ax = df.plot(y=metric1, title=f"{metric1} Line Chart")
    ax = df.plot(y=metric1)

    # Set the labels and title
    ax.set_xlabel("Time")
    #ax.set_ylabel(f"{metric1} Value")


    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

# Function to generate a NetworkX graph (example: simple graph)
def create_networkx_graph_sample():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)])
    
    # Create plot of the graph
    fig, ax = plt.subplots()
    nx.draw(G, with_labels=True, ax=ax, node_size=500, node_color="lightblue", font_size=12, font_weight="bold")
    ax.set_title("NetworkX Graph")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close(fig)
    
    return img_buffer

# Function to render a NetworkX graph
def create_networkx_graph(G):
    
    # Create plot of the graph
    fig, ax = plt.subplots()
    #nx.draw(G, with_labels=True, ax=ax, node_size=500, node_color="lightblue", font_size=8, font_weight="bold")
    nx.draw(G, with_labels=True, ax=ax, node_color="lightblue",font_size=8)
    ax.set_title("relation visualization")

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close(fig)
    
    return img_buffer

# Function to render a NetworkX graph
def create_graphviz_graph(G):
    
    # Create plot of the graph
    fig, ax = plt.subplots()
    #nx.draw(G, with_labels=True, ax=ax, node_size=500, node_color="lightblue", font_size=8, font_weight="bold")
    
    #nx.draw(G, with_labels=True, ax=ax, node_color="lightblue",font_size=8)
    #ax.set_title("relation visualization")

    # Render the Graphviz graph to a PNG file in memory using BytesIO
    img_buffer = BytesIO()
    G.format = 'png'
    G.render(img_buffer, format='png', cleanup=False)  # Don't delete the temporary file
    #img_buffer.seek(0)  # Reset the buffer to the start

    #img_buffer = BytesIO()
    #plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    #plt.close(fig)
    
    return img_buffer

# Main function to create the PDF
def create_pdf(pdf_filename, results, conclusion_df, data_df):

    indent=5
    # Create an indentation string based on the current depth
    indent_str = "  " * indent
    
    # Create a DataFrame for the table
    #data = {'Metric': ['A', 'B', 'C'], 'Value': [10, 20, 30]}
    #df = pd.DataFrame(data)

    now = datetime.datetime.now()
    output_dir = get_output_directory()

    # Use datetime to create a unique filename
    filename = output_dir / f"{pdf_filename}_{now.strftime('%Y%m%d_%H%M%S')}.pdf"

    # Convert POSIX to string
    filename=str(filename)

    # Create the PDF document
    document = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Add a title
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    story.append(Paragraph("Analysis Report", title_style))
    story.append(Spacer(1, 12))

    # Add some text
    story.append(Paragraph("This document contains a table, chart, and network graph.", styles['Normal']))
    story.append(Spacer(1, 12))

    for key, value in results.items():
        if key=="relationship" :
            causal_graph_nx,causal_metricgv = getCausalGraph(value)
            # Add a networkx graph
            graph_img = create_networkx_graph(causal_graph_nx)
            ##graph_img = create_graphviz_graph(causal_metricgv)
            # Use the Image class to add the graph image
            graph_image = Image(graph_img)  
            # very primitive way
            graph_image.drawHeight = 4*inch 
            graph_image.drawWidth = 10*inch 
            story.append(Paragraph("Relationship Graph", styles['Heading2']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("This causal graph explains which the causal metrics affect the health metrics."
                                   "The causal metrics influence or drive the system's health, either improving or degrading it.", styles['Normal']))
            story.append(Spacer(1, 12))
            # Adding the NetworkX graph image to the story
            story.append(graph_image)  
            story.append(Spacer(1, 12))
        elif key=="allMetrics" :
            continue
            # story.append(Paragraph("List of Metrics", styles['Heading2']))
            # story.append(Spacer(1, 12)) 
            # # Add bulleted list from python List 
            # for item in value:
            #     story.append(Paragraph(f"{indent_str}- {item}", styles['Normal'])) 
            #     story.append(Spacer(1, 12))
        elif key=="impactedMetricList" :
            story.append(Paragraph("Health Metrics: Indicate how well the system is performing.", styles['Heading2']))
            story.append(Spacer(1, 12))  
            # Add bulleted list from python List
            for item in value:
                story.append(Paragraph(f"{indent_str}- {item}", styles['Normal']))   
                story.append(Spacer(1, 12)) 

                chart_img = create_matplotlib_chart(data_df,item)
                chart_image = Image(chart_img)  # Use the Image class to add the chart image
                chart_image.drawHeight = 3*inch  # Set the height of the image
                chart_image.drawWidth = 9*inch   # Set the width of the image
                #story.append(Paragraph("Sample Line Chart", styles['Heading2']))
                story.append(Spacer(1, 12))
                story.append(chart_image)  # Adding the Matplotlib chart image to the story
                story.append(Spacer(1, 12))
        elif key=="driverMetricList" :
            story.append(Paragraph("Causal Metrics: Influence or drive the system's health, either improving or degrading it.", styles['Heading2']))
            story.append(Spacer(1, 12))  
            # Add bulleted list from python List
            for item in value:
                story.append(Paragraph(f"{indent_str}- {item}", styles['Normal']))  
                story.append(Spacer(1, 12))   
        elif key=="conclusion" :
            story.append(Paragraph("To Summarize", styles['Heading2']))
            story.append(Spacer(1, 12)) 
            # Add Table from dataframe 
            story.append(create_table_from_dataframe(conclusion_df))
            story.append(Spacer(1, 12))                                         
        else :
            story.append(Paragraph(key, styles['Normal']))
            story.append(Spacer(1, 12))
            story.append(Paragraph("New Stuff...", styles['Normal']))
            story.append(Spacer(1, 12))




    #print(story)
    # Build the document
    document.build(story)
    print(f"PDF created successfully at {pdf_filename}")

# Create the PDF
#pdf_filename = "analysis_report.pdf"
#create_pdf_with_table_text_chart(pdf_filename)

#print(f"PDF created successfully at {pdf_filename}")
