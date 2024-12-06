Web Scraping for Optical Data
=============================

Description:

This Python script scrapes data for refractive index (n) and extinction
coefficient (k) from a webpage and saves it to a file. It performs
processing, filtering, interpolation, and plotting to obtain the desired
data range.

Installation:
-------------

Clone the repository:

.. code:: bash

   git clone https://github.com/anibalbezerra/OpticalProperties_scrapping.git

Install dependencies:

.. code:: bash

   cd OpticalProperties_scrapping
   pip install requests beautifulsoup4 numpy matplotlib selenium webdriver_manager

Usage:
------

Modify the URL: Replace the placeholder URL
‘https://refractiveindex.info/?shelf=main&book=Ta2O5&page=Bright-amorphous’
in the url variable with the actual URL of the webpage containing the
desired optical data.

Run the script:

.. code:: bash

   python scrape_and_process

Functionality:
~~~~~~~~~~~~~~

Data Scraping:

1. Fetches data from the specified URL using getMaterial and getResponse
   functions.
2. Processes the response using processing to extract relevant values.
3. Splits the extracted strings into numerical data using splitting (it
   handles potential parsing errors).

Data Processing:

4. Plots the full acquired data using plotting for initial inspection
   (sanity check).
5. Cuts and interpolates the data within a specific wavelength range
   (range_i to range_f) with a desired resolution (delta) using the
   cut_and_interpolate function.

Data Visualization:

6. Plots the interpolated curves using plotting for final visualization.

Data Saving:

7. Saves the interpolated data to a file named nk\_.dat using save_data.

Notes:
~~~~~~

1. The script requires external libraries requests, beautifulsoup4,
   numpy, and matplotlib. Install them using pip.
