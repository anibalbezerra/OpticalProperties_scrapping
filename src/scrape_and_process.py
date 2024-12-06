#!pip install selenium
#!pip install webdriver_manager

import requests
from bs4 import BeautifulSoup
import bs4
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def getResponse(url):
    """
    Fetches data containing the string "data_n_wl" from a webpage using an HTTP GET request.

    This function retrieves the HTML content of a webpage at the specified URL and searches for occurrences of the string "data_n_wl" 
    within the text content of the page elements.

    Args:
        url (str): The URL of the webpage to retrieve data from.

    Returns:
        list: A list containing all BeautifulSoup objects found that have text content containing the string "data_n_wl". 
        If the request fails or no matches are found, an empty list is returned.

    Raises:
        None: This function does not raise any exceptions. However, it prints a warning message if the HTTP GET request fails.
    """
    # Send an HTTP GET request to the webpage
    response = requests.get(url)
    if response.status_code == 200:
    # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.text, 'html.parser')
    else:
        print('Something went wrong, watch to the URL')
        return 1

    # Find all occurrences of the string anywhere within the text content
    data_matches = soup.find_all(string=lambda text: text and 'data_n_wl' in text)

    return data_matches

def processing(data, verbose = True):
    """
    Extracts specific information from the first element of a data list.

    This function assumes the first element of the input data list is a string containing information separated by whitespace. 
    It extracts four specific values based on their positions within the string.

    Args:
        data (list): A list containing data, where the first element is a string to be processed.
        verbose (bool, optional): Flag to control printing the extracted values during processing. Defaults to True.

    Returns:
        tuple: A tuple containing four strings:
            - n_wl_str (str): The value at the 4th position in the input string.
            - k_wl_str (str): The value at the 5th position in the input string.
            - n_str (str): The value at the 6th position in the input string.
            - k_str (str): The value at the 7th position in the input string.

    Notes:
        - The function assumes the input data list has at least one element and the first element is a string.
        - Verbose mode prints the extracted values for debugging or clarity. 
        - No error handling is implemented for cases where the input string format is unexpected.
    """
    #poping the text to generate a string
    string = data.pop(0)

    n_wl_str = string.split()[4]
    k_wl_str = string.split()[5]
    n_str = string.split()[6]
    k_str = string.split()[7]

    if verbose:
        print(n_wl_str)
        print(k_wl_str)
        print(n_str)
        print(k_str)
    
    return n_wl_str, k_wl_str, n_str, k_str

def splitting(string, verbose = True):
    """
    Parses a string containing a variable assignment with a list of comma-separated values.

    This function takes a string representing a variable assignment where the value is a list of comma-separated numbers. 
    It extracts the list of values and converts them to floating-point numbers.

    Args:
        string (str): The input string containing the variable assignment.
        verbose (bool, optional): Flag to control printing intermediate steps during processing. Defaults to True.

    Returns:
        numpy.ndarray: A NumPy array containing the extracted and converted floating-point values. 
                       If the parsing fails or the list is empty, an empty NumPy array is returned.

    Raises:
        ValueError: If any of the values in the list cannot be converted to float.

    Notes:
        - The function assumes the input string follows the format "variable=[list_of_numbers]".
        - Verbose mode prints intermediate steps during processing for debugging or clarity.
    """
    sp1 = string.split('=')    
    print('Accessing Variable ', sp1[0])
    sp2 = sp1[1].split('[')[1].split(']')[0]    
    sp3 = sp2.split(',')

    if verbose:        
        print('step1 ', sp2)
        print('step2 ', sp3)        

    # Convert each value in sp3 to float if not empty
    try:
        float_list = [float(num) for num in sp3]
        if verbose:
            print('step3 ', float_list) 

        return np.array(float_list)
    except ValueError:
        if verbose:
            print('step3 ', [])
        return []

def um2nm(w):
    return [wl * 1000 for wl in w]

def nm2um(w):
    return [wl / 1000 for wl in w]

def plotting(nwl, n, k):
    """
    Generates a plot of refractive index (n) and extinction coefficient (k) vs wavelength.

    This function creates a plot with two lines:
        - One line shows the refractive index (n) vs wavelength (converted to nanometers).
        - The second line (optional) shows the extinction coefficient (k) vs wavelength, but only if the k data is not empty.

    Args:
        nwl (array): Array of wavelengths in micrometers (μm).
        n (array): Array of corresponding refractive indices.
        k (array): Array of corresponding extinction coefficients.

    Notes:
        - The function first converts the input wavelengths from micrometers to nanometers using an external function `um2nm`.
        - It checks if the `k` array is empty. If so, a warning message is printed, and the `k` data is replaced with an array of zeros before plotting.
        - The plot uses Matplotlib for visualization.
            - The figure size is set to 8 inches wide and 6 inches high.
            - Labels and title are set for the axes and the plot.
            - A legend is added to differentiate the lines (n and k, if applicable).
            - Grid lines are enabled for better readability.
    """
    # Convert micrometers to nanometers
    nwl_nm = um2nm(nwl)
    
    # Create the plot
    plt.figure(figsize=(8, 6))

    # Plot nwl vs n
    plt.plot(nwl_nm, n, label='n')

    # Plot kwl vs k

    if not list(k)==[]:
        plt.plot(nwl_nm, k, label='k')
    else:
        print('Warning: k array is empty. It will be converted to a zeros array')

    # Set labels and title
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('n, k')
    plt.title('Refractive Index (n) and Extinction Coefficient (k) vs Wavelength')

    # Add legend
    plt.legend()

    # Show the plot
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def save_data(nwl, n, k, filename):
    """
    Saves wavelength (nwl), refractive index (n), and extinction coefficient (k) data to a file.

    This function saves the provided data arrays (wavelength, refractive index, and extinction coefficient) 
    to a text file with a specified filename. It performs a check to ensure there's actual data before saving.

    Args:
        nwl (array): Array of wavelengths in micrometers (μm).
        n (array): Array of corresponding refractive indices.
        k (array): Array of corresponding extinction coefficients.
        filename (str): The filename to save the data to.

    Returns:
        int:
            - 0: Success, data saved to the file.
            - -1: No data to save (all elements in nwl_nm are zero). 

    Notes:
        - The function first converts the input wavelengths from micrometers to nanometers using an external function `um2nm`.
        - It checks if all elements in the converted wavelength array (nwl_nm) are zero. 
            If so, it prints a warning message and returns -1 to indicate no data was saved.
        - The function opens the file in write mode ('w') and writes a header line with column labels.
        - It iterates through the data arrays and writes each data point (wavelength, refractive index, extinction coefficient) to a separate line in the file.
    """
    nwl_nm = um2nm(nwl)
    if all(element == 0 for element in nwl_nm):
        print('Warning: There is no data within the specified range of wavelength. No file will be saved!')
        return -1
    # Open the file for writing
    with open(filename, 'w') as f:
        # Write the header line
        f.write('Wavelength (nm), n, k\n')

        # Write each data point to the file
        for i in range(len(nwl_nm)):
            f.write(f'{nwl_nm[i]}, {n[i]}, {k[i]}\n')

def select_wavelength_range(nwl, n, range_i = 0.25, range_f=0.45):
    """
    Selects a specific range of wavelength (nwl) and refractive index (n) data.

    This function filters the input data (nwl and n) to a user-specified wavelength range.

    Args:
        nwl (array): Array of wavelengths in micrometers (μm).
        n (array): Array of corresponding refractive indices.
        range_i (float, optional): Lower wavelength limit (inclusive) in micrometers (μm). Defaults to 0.25.
        range_f (float, optional): Upper wavelength limit (exclusive) in micrometers (μm). Defaults to 0.45.

    Returns:
        tuple: A tuple containing two arrays:
            - selected_nwl (array): Array of filtered wavelengths within the specified range (in nanometers).
            - selected_n (array): Array of corresponding refractive indices for the filtered wavelengths.

    Raises:
        Exception: If no data points fall within the specified wavelength range.

    Notes:
        - The function first converts the input wavelengths from micrometers to nanometers using an external function `um2nm`.
        - It then finds the indices of the data points closest to the desired range boundaries (inclusive for lower limit, exclusive for upper limit) 
            using `min` and a lambda function.
        - The function slices the original nwl and n arrays based on the identified indices to extract the data within the desired range.
        - If no data points fall within the range, it raises an exception with an informative message and returns empty lists.
    """

    nwl_nm = um2nm(nwl)

    try:
        # Find the indices of the wavelengths in the desired range
        start_index = min(range(len(nwl_nm)), key=lambda i: abs(nwl_nm[i] - range_i))
        end_index = min(range(len(nwl_nm)), key=lambda i: abs(nwl_nm[i] - range_f))
        print(start_index, end_index)        
        # Select the desired range of wavelengths and refractive indices
        selected_nwl = nwl_nm[start_index:end_index]
        selected_n = n[start_index:end_index]

        return selected_nwl, selected_n
    except Exception as e:
        print(f"Data doesen't fit the range: {e}")
        return [], []


def cut_and_interpolate(wavelength, n, range_i=250, range_f=450, delta=1):
    """
    Cuts and interpolates refractive index data within a wavelength range.

    Args:
        wavelength (array): Array of original wavelengths (nm).
        n (array): Array of corresponding refractive indices.
        range_i (int): Initial wavelength value of the range.
        range_f (int): Final wavelength value of the range.
        delta (float): wavelength step

    Returns:
        tuple: Tuple containing the interpolated wavelength and refractive index arrays.
    """

    # Generate a new wavelength array
    new_wavelength = np.arange(range_i, range_f+1, delta)
    
    wavelength = np.array(um2nm(wavelength))
    size = len(new_wavelength)
    if list(wavelength)==[]:
        print("Warning: No data points found in any range.")
        return np.zeros(size, dtype=int), np.zeros(size, dtype=int)

    mask = (wavelength >= 250) & (wavelength <= 450)
    wavelength_cut = wavelength[mask]

    # Check if any data points are available in the desired range
    if not len(wavelength_cut):
        print("Warning: No data points found in the range (250nm - 450nm).")
        return np.zeros(size, dtype=int), np.zeros(size, dtype=int)

    n_cut = n[mask]

    # Interpolate the n curve
    interp_func = interp1d(wavelength_cut, n_cut, kind='linear', bounds_error=False, fill_value='extrapolate')

    # Interpolate n values for the new wavelength array
    new_n = interp_func(new_wavelength)
    return nm2um(new_wavelength), new_n

def getMaterial(url):
    material = url.split('&')[1].split('=')[1]
    print('Material being analysed ', material)
    return material


######### Running scrapping ################
# Replace with the actual URL of the webpage
url = 'https://refractiveindex.info/?shelf=main&book=Ta2O5&page=Bright-amorphous'

# Get the material from the url
material = getMaterial(url)

# Get the optical response from the html
data_matches = getResponse(url)

# Process the resulting response
n_wl_str, k_wl_str, n_str, k_str = processing(data_matches, verbose = True)

nwl = splitting(n_wl_str)
kwl = splitting(k_wl_str)
n = splitting(n_str)
k = splitting(k_str)

 # plotting full acquired data - sanity check
plotting(nwl, n, k)

# Cut to desired range and performs the interpolation
new_nwl, new_n = cut_and_interpolate(nwl, n, range_i=250, range_f=450, delta=1)
new_kwl, new_k = cut_and_interpolate(kwl, k, range_i=250, range_f=450, delta=1)

# Plots the resulting curves after interpolation
plotting(new_nwl, new_n, new_k)

#saving data to file
save_data(new_nwl, new_n, new_k, f'nk_{material}.dat')
