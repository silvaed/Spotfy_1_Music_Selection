# World Football Data Dashboard ⚽

This is a Streamlit web application that allows you to explore football match statistics from various countries and leagues. You can filter the data based on countries, leagues, and teams, view metrics related to goals scored, and visualize the data on a map.

## Features

- **Data Download**: The application can download football match data from a Google Drive shareable link and display it in a tabular format.

- **Data Filtering**: You can filter the data by selecting specific countries, leagues, and teams using the sidebar widgets.

- **Metric Calculation**: The application calculates and displays various metrics related to goals scored in football matches, providing insights into different game events.

- **Total Goals by Team**: It calculates and displays the total goals scored and conceded by each team, giving you an overview of their performance.

- **Map Visualization**: The application creates an interactive map plot using Plotly Express to visualize the total goals scored by each country.

## How to Use

1. **Run the Application**: To run the application, execute the code provided in your Streamlit environment or Python IDE.

2. **Filter Data**: Use the sidebar widgets to filter the data by selecting countries, leagues, and teams of interest.

3. **View Metrics**: Explore the calculated metrics related to goals scored and other game events in the DataFrame.

4. **Total Goals by Team**: Check out the total goals scored and conceded by each team in the DataFrame.

5. **Map Visualization**: Interact with the map plot to see the distribution of total goals scored by country.

## Requirements

- Python 3.x
- Streamlit
- Pandas
- Plotly Express
- Gdown

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone <repository-url>

pip install streamlit pandas plotly gdown

streamlit run <filename.py>
