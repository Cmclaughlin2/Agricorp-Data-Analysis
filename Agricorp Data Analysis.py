import requests
from copy import copy


PALMER_DATA_URL = 'https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/palmer_drought/'
CENTRAL_FILE = 'wpdcentr.txt'
WESTERN_FILE = 'wpdwest.txt'
SOUTHERN_FILE = 'wpdsouth.txt'
EASTERN_FILE = 'wpdeast.txt'


def get_weather_data(region):
    """Gets the parsed weather data as a list of lists where each item in the outer list
    is a list of the data elements for a row from the data based on the results of the
    parse_row function.
    
    Parameters
    ----------
    region : str
        The file name to be used at the end of the URL to get the data for that region.
    
    Returns
    -------
    list
        Contains the parsed weather data for the user specified region.
    
    Raises
    ------
    requests.exceptions.RequestException
        Raised when there is a problem downloading the data from the Palmer Website.
    """
    try:
        url = PALMER_DATA_URL + region
        response = requests.get(url)
        response.raise_for_status()
        decode_data = response.text
        data_list = [row for row in decode_data.split('\n') if len(row) > 0]
    except requests.exceptions.RequestException as error:
        print(f"{error} downloading data from the Palmer Website.")
    else:
        return [parse_row(row) for i, row in enumerate(data_list) if 7 < i < (len(data_list) - 1)]


def parse_row(row):
    """Slices the neccessary variables for the data analysis project from the .txt file.
       Allows the parsing of the unstructured data for the get_weather_data function.
    
    Parameters
    ----------
    row : str
    Contains the rows of parsed data from the Palmer website .txt file.
        
    Returns
    -------
    Provides the parsed data from the user input region of the Palmer Drought Severity & Crop Moisture Website.
    """
    state = (row[:3].strip())
    tempurature = float(row[27:33].strip())
    precipitation = float(row[33:39].strip())
    drought_index = float(row[89:96].strip())
    precipitation_needed = float(row[99:].strip()) if row[99:].strip() != '' else 0.0
    return [drought_index, state, tempurature, precipitation, precipitation_needed]


def row_aggregations(data):
    """
    Parameters
    ----------
    data : list
    Contains the regional parsed data file from the user provided input.
    
    Returns
    -------
    Provides the average of each neccessary data point. This is stored in the row_calculations list variable.
    """
    row_calculations = []
    row_count = 0
    avg_tempurature = 0
    avg_precipitation = 0
    avg_drought_index = 0
    avg_precipitation_needed = 0
    for i, row in enumerate(data):
        row_count += 1
        current_state = row[1]
        avg_tempurature += row[2]
        avg_precipitation += row[3]
        avg_drought_index += row[0]
        avg_precipitation_needed += row[4]
        if i == len(data) - 1:
            next_state = ''
        else:
            next_state = data[i+1][1]
        if current_state != next_state:
            row_calculations.append([(avg_drought_index / row_count),current_state,(avg_tempurature / row_count), (avg_precipitation / row_count), (avg_precipitation_needed / row_count)])
            row_count = 0
            avg_tempurature = 0 
            avg_precipitation = 0
            avg_drought_index = 0
            avg_precipitation_needed = 0
    return row_calculations


def worst_drought_state(data):
    """Copies the data list and then sorts to find the state with the worst average drought.
       This will later be printed to the terminal for analysis purposes.
    
    Parameters
    ----------
    data : list
    Contains the regional parsed data file from the user provided input.
    
    Returns
    -------
    Provides the state code with the worst average drought statistic.
    """
    copy_drought_data = copy(data)
    copy_drought_data.sort()
    return copy_drought_data[0][1]


print("Agricorp Q3 Investment Data Analysis\n")

print("This program begins by prompting the user for the region they would like to select.\nIt then parses the input file and outputs several data columns for each state contained within.\nThese include it's average drought index, state code, average tempurature, average precipitation, and average precipitation needed.\n")


def user_input(prompt):
    """
    Parameters
    ----------
    prompt : str
    Parameter that encapsulates the upper case user input in the input(prompt).
    
    Returns
    -------
    Returns the upper case raw input along with the corresponding file name and region.
    """
    valid_inputs = ["W","E","S","C"]
    while True:
        raw_input = input(prompt).upper()
        if raw_input in valid_inputs:
           region = get_region(raw_input)
           file_name = get_file_name(raw_input)
           print(f"You selected the {region} from the {file_name}.\n")
           return file_name, region, raw_input
        else:
            print(f"{raw_input} is not accepted, please try again.")


def get_states(aggregated_data):
    """Returns a list containing the state codes in the user input region.
    
    Parameters
    ----------
    aggregated_data : 
    Parameter that encapsulates the aggregated_data function.

    Returns
    -------
    Provides a list of the state codes from the region that the user supplies.
    """
    regional_state_list = ''
    for row_list in aggregated_data:
        current_state = row_list[1]
        regional_state_list += current_state + (', ')
    return regional_state_list.strip(', ')


def get_region(region):
   """Returns a specific region string based on the user input prompt.
    
    Parameters
    ----------
    region : 
    parameter that encapsulates the user input for their selected region.
    
    Returns
    -------
    Provides a string of whichever region the user selects in the terminal.
    """
   if region == 'W':
       return "Western Region"
   elif region == 'C':
       return "Central Region"
   elif region == 'S':
        return "Southern Region"
   elif region == 'E':
        return "Eastern Region"


def get_file_name(file_name):
   """Returns a specific file name string based on the user input prompt.
    
    Parameters
    ----------
    file_name : 
    parameter that encapsulates the user input for their selected file name.
    
    Returns
    -------
    Provides a string of whichever file name the user selects in the terminal.
    """
   if file_name == 'W':
        return WESTERN_FILE
   elif file_name == 'E':
        return EASTERN_FILE
   elif file_name == 'C':
        return CENTRAL_FILE
   elif file_name == 'S':
        return SOUTHERN_FILE



user_file, user_region, raw_input = user_input("Please select a region of the United States (W for Western, E for Eastern, C for Central, or S for Southern).\n")
user_weather_data = get_weather_data(user_file)

rows = row_aggregations(user_weather_data)
print(f"The {get_region(raw_input)} contains the following states: {get_states(rows)}.\n")
print(f"{worst_drought_state(user_weather_data)} is the state with the worst drought index.\n")

row_format = '{:<15.3f}{:>15}{:>15.3f}{:>20.3f}{:>20.3f}'
header_format = '{:<15}{:>15}{:>15}{:>20}{:>20}'
print(header_format.format('AVG Drought Index', 'State', 'AVG Temp', 'AVG Precip', 'AVG Precip Needed'))


for row_list in rows:
    drought_index, current_state, tempurature, precipitation, precipitation_needed = row_list
    print(row_format.format(drought_index, current_state, tempurature, precipitation, precipitation_needed))
    print(f"-------------------------------------------------------------------------------------\n")

input("Press enter to quit....")