# Agricorp Q3 Investment Data Analysis

This Python project performs analysis on weather data obtained from the Palmer Drought Severity & Crop Moisture Website. Users first select a region of the United States (Western, Eastern, Central, or Southern). The program then parses the corresponding data file, and outputs various data columns for each state within the chosen region.

## Getting Started

### Prerequisites

- Python version 3.0 or greater
- Requests library (install with `pip install requests`)

### Running the Script

1. Clone the repository to your local machine.
2. Open a terminal and navigate to the project directory.
3. Run the script by executing the command:
   ```bash
   python Agricorp Data Analysis.py

## Features

### `get_weather_data(region)`

This function retrieves and parses weather data for the specified region from the Palmer Drought Severity & Crop Moisture Website. It employs the Requests library to make an HTTP request and handles potential errors during the data retrieval process.

### `parse_row(row)`

This function begins by slicing the necessary variables from a row of parsed data obtained from the Palmer website. It then extracts information such as state code, temperature, precipitation, drought index, and precipitation needed for further analysis.

### `row_aggregations(data)`

This function calculates the average values of key weather parameters for each state in the specified region. It returns a list containing the aggregated data.

### `worst_drought_state(data)`

This function first identifies the state with the worst average drought index based on the parsed data. Then it creates a copy of the data, sorts it, and returns the state code with the lowest drought index.

### `user_input(prompt)`

The function prompts the user to select a region by entering a specific code (W for Western, E for Eastern, C for Central, or S for Southern). It has error checking to ensure that the user input is valid and then returns the corresponding file name and region.

### `get_states(aggregated_data)`

Returns a formatted string containing the state codes present in the user-specified region. Then this information is used to display the list of states in the project results.

### `get_region(region)`

This function returns a string that represents the selected region based on the user input.

### `get_file_name(file_name)`

Begins by returning the corresponding file name based on the user input. This function is used within the project to identify the data file for the selected region.

## Usage

1. Run the project and follow the prompts to select a region.
2. The user can then view the analysis results. These include the worst drought state and average data for each state in the chosen region.

## File Structure

- `Agricorp Data Analysis.py`: Main Python script for data analysis.
- `wpdcentr.txt`, `wpdwest.txt`, `wpdsouth.txt`, `wpdeast.txt`: Data files for the United States regions from the Palmer website.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The data for this project is sourcded from the [Palmer Drought Severity & Crop Moisture Website](https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/palmer_drought/).
