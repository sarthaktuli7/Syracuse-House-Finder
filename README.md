<img width="1873" height="817" alt="image" src="https://github.com/user-attachments/assets/1215bb68-703c-424b-bd75-1449363461da" />

1. Problem Statement: "The Housing Hunt Hurdle"
"In Syracuse, finding suitable student-friendly rental housing near Syracuse University is a significant challenge. Existing online platforms often provide overwhelming lists of properties without robust filtering for specific academic needs, like proximity to campus. This forces individuals to manually sift through hundreds of listings, cross-referencing locations, and estimating commute times, leading to frustration, wasted time, and potentially sub-optimal housing choices."

2. How I Tackled It (Methodology): "From Raw Data to Insight"
"To address this, I developed the Syracuse Rent Analyzer. My approach involved:

Data Acquisition & Preprocessing: I started with a dataset of rental listings (which could be sourced from web scraping or property aggregators). The raw data often contained inconsistencies, missing values, and varying formats. I used Pandas to clean this data, handling missing lat/lon values, converting price and beds to appropriate numerical types, and standardizing the is_furnished column into a boolean.

Geospatial Analysis: A key requirement was filtering by distance to Syracuse University. I used the geopy library to calculate the precise geodesic distance (in miles) for each listing from a central Syracuse University coordinate. This transformed raw address data into a highly relevant metric for users.

Interactive Dashboard Development: I leveraged Streamlit to build an intuitive, interactive web application. I designed a user-friendly sidebar with multiple filters (price range, bedroom count, maximum distance to SU, neighborhood, furnished status).

Visualization & Presentation: The processed data is presented in two key ways:

An interactive map displaying all filtered listings, providing a quick visual overview of property distribution relative to the university.

A sortable table for detailed viewing of filtered listings.

Individual listing cards with clickable links, offering direct access to the source.

This multi-faceted approach ensures that users can quickly narrow down their search and make informed decisions."

3. Impact & Results: "Empowering Informed Decisions"
"The Syracuse Rent Analyzer directly addresses the problem by:

Saving Time: Users no longer need to manually verify distances or cross-reference multiple platforms.

Enhancing Decision-Making: By visualizing properties on a map and providing precise distance metrics, users gain a clearer understanding of their options and can prioritize based on their commute preferences.

Improving User Experience: The interactive filters and clear presentation make the housing search process significantly more efficient and less frustrating.
The application successfully transforms raw, disparate rental data into an easily navigable and highly valuable resource for anyone seeking housing near Syracuse University."

4. Tools & Technologies Used:
Python: The core programming language.

Streamlit: For building the interactive web application/dashboard.

Pandas: For data loading, cleaning, transformation, and manipulation.

Geopy: For geospatial calculations, specifically geodesic distance.

5. Key Skills Demonstrated:
Data Cleaning & Preprocessing: Handling missing values, type conversion, data standardization.

Data Transformation: Creating new features (distance to SU) from existing data.

Geospatial Analysis: Applying geographical calculations to enhance data utility.

Interactive Dashboard Development: Designing and implementing a user-friendly interface.

Data Visualization: Presenting complex data clearly on maps and tables.

Python Programming: Writing modular, efficient, and readable Python code.

Problem-Solving: Identifying a real-world problem and building a data-driven solution.

Version Control: (Implicit, as you'd host this on GitHub)

📁 Project Structure
To run this project, your folder structure should look like this:

syracuse_rent_analyzer/  (Your main project folder)
├── housing.py           (Your Streamlit application code)
└── data/                (Folder to store your data files)
    └── corrected_csv.csv  (Your rental data CSV file)

**Follow these steps to set up and run the Syracuse Rent Analyzer on your local machine:**

Prerequisites
Python 3.7+ (Anaconda is recommended for environment management)

pip (Python package installer)

1. Set Up Your Environment
Open your Anaconda Prompt (or your terminal/command prompt) and navigate to your desired project directory.

Navigate to where you want to create your project folder
C:\Users\YourUser\Documents\Projects 

Create the project folder
mkdir syracuse_rent_analyzer
cd syracuse_rent_analyzer

Create the 'data' subfolder
mkdir data

Activate your base environment (or create a new one)
conda activate base 

2. Install Dependencies
In the Anaconda Prompt (with your environment activated), install the necessary Python libraries:

conda install pandas streamlit geopy

 If conda has issues, you can try:
 pip install pandas streamlit geopy

3. Place Your Data File
Make sure your rental data file is named corrected_csv.csv and placed inside the data folder within your syracuse_rent_analyzer project directory.

4. Your Streamlit Application Code (housing.py)

5. Run the Application
Once you have placed housing.py and the data/corrected_csv.csv file in their respective locations within the syracuse_rent_analyzer directory, open your Anaconda Prompt, navigate to the syracuse_rent_analyzer folder, and run:

streamlit run housing.py
