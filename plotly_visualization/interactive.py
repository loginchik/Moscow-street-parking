import plotly.graph_objects as go
import pandas as pd
import json

# Read prepared data from the external files 
parks_graphData_tiny = pd.read_csv('plotly_visualization/data/parkings_tiny.csv')
parks_graphData_small = pd.read_csv('plotly_visualization/data/parkings_small.csv')
parks_graphData_meduim = pd.read_csv('plotly_visualization/data/parkings_medium.csv')
parks_graphData_big = pd.read_csv('plotly_visualization/data/parkings_big.csv')
regs_graphData = pd.read_csv('plotly_visualization/data/regs.csv')

with open('plotly_visualization/data/quantiles.json') as q_file:
    quantiles = json.load(q_file)

q_25 = quantiles['q1']
q_50 = quantiles['q2']
q_75 = quantiles['q3']

# Set up colors for the graph
colors = {
    'darkblue': 'black',
    'lightred': '#F2545B', 
    'background': '#AED4E6'
}

gradient = {
    'tiny': '#FF6D3F',
    'small': '#B14B4B',
    'medium': '#594057',
    'big': '#36162E'
}

# Create plotly Figure object to place graph there 
fig = go.Figure()

# Trace for Scattergeo for Moscow regions  
fig.add_trace(go.Scattergeo(
    # Data to display 
    lat = regs_graphData['lat'],
    lon = regs_graphData['lon'],
    
    # Display data as lines 
    mode = 'lines',  
    # Set the color of the lines   
    marker = {
        'color': colors['darkblue'],
    },
    
    # Remove any info on hover not to overload the graph with information
    hoverinfo='none',
    
    # Specify legend label
    name = 'Районы г. Москва'
))
        

# Trace for Scattergeo for Moscow street parkings  
fig.add_trace(go.Scattergeo(
    # Data to display 
    lon = parks_graphData_tiny['lon'],
    lat = parks_graphData_tiny['lat'], 
    
    # Display data as lines 
    mode = 'lines', 
    # Set the color of the lines   
    marker = {
        'color': gradient['tiny'],
    },
    
    # Set the information that appeares on hover 
    hoverinfo = 'text',
    text = parks_graphData_tiny['address'],
    
    # Specify legend label
    name = f'Платные парковки г. Москва (до {int(q_25)} мест)'
))

fig.add_trace(go.Scattergeo(
    # Data to display 
    lon = parks_graphData_small['lon'],
    lat = parks_graphData_small['lat'], 
    
    # Display data as lines 
    mode = 'lines', 
    # Set the color of the lines   
    marker = {
        'color': gradient['small'],
    },
    
    # Set the information that appeares on hover 
    hoverinfo = 'text',
    text = parks_graphData_small['address'],
    
    # Specify legend label
    name = f'Платные парковки г. Москва (до {int(q_50)} мест)'
))

fig.add_trace(go.Scattergeo(
    # Data to display 
    lon = parks_graphData_meduim['lon'],
    lat = parks_graphData_meduim['lat'], 
    
    # Display data as lines 
    mode = 'lines', 
    # Set the color of the lines   
    marker = {
        'color': gradient['medium'],
    },
    
    # Set the information that appeares on hover 
    hoverinfo = 'text',
    text = parks_graphData_meduim['address'],
    
    # Specify legend label
    name = f'Платные парковки г. Москва (до {int(q_75)} мест)'
))

fig.add_trace(go.Scattergeo(
    # Data to display 
    lon = parks_graphData_big['lon'],
    lat = parks_graphData_big['lat'], 
    
    # Display data as lines 
    mode = 'lines', 
    # Set the color of the lines   
    marker = {
        'color': gradient['big'],
    },
    
    # Set the information that appeares on hover 
    hoverinfo = 'text',
    text = parks_graphData_big['address'],
    
    # Specify legend label
    name = f'Платные парковки г. Москва (более {int(q_75)} мест)'
))



fig.update_geos(
    # Auto zoom up to graph borders 
    fitbounds="locations",
    # Turn off scope display 
    visible=False,
    # Turn on map frame 
    showframe = True,
    )

fig.update_layout(   
    # Graph title 
    title = 'Карта платных парковок г. Москва',
    
    legend = {
        # Clicks on legend items 
        'itemclick': 'toggle',
        'itemdoubleclick': 'toggleothers', 
        
        # Legend title
        'title_text': 'Условные обозначения'
    }, 
    
    # Specify font options
    font = {
        'family': 'PT Sans Narrow',
        'size': 14,
    },
    
    # Set up the view of the hover block 
    hoverlabel = {
        'align': 'left', 
        'bgcolor': colors['background'],
        
        'font': {
            'family': 'PT Sans Narrow',
            'size': 14,
            'color': colors['darkblue'],
        }  
    },  
    
    # Dimensions
    height = 800,
)

fig.update_scenes(
    # Set up camera 
    camera = {
        'projection': {'type': 'orthographic'}
    }
)


if __name__ == '__main__':
    fig.write_html('results/interactive_graph.html')