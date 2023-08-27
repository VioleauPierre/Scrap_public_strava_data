# Strava Activity Data Retrieval
This project is aimed at retrieving public activity data of a user on Strava without using the official API. It utilizes web scraping techniques with the help of the Selenium and BeautifulSoup libraries in Python.

## Skills : 
- Web Scraping: Utilizing requests and BeautifulSoup for data extraction.
- Data Manipulation: Converting, filtering, cleaning, loading, and saving data.
- Browser Automation: Utilizing Selenium for browser interactions.
- Writing and Importing Custom Modules: Creating functions_strava.py for custom module imports.
  
## Librairies used : 
- requests
- Selenium
- Beautifulsoup

## 1. Open and save file
To save the data and load it later, the project provides functions for saving and loading lists and datasets.

## 2. Retrieve activity ID 
This section focuses on retrieving activity IDs from Strava for a given user. Modify the function in functions_strava.py to retrieve activities for a specific user by specifying their ID. Additionally, provide your Strava account email and password.

### 2.1 Login to Strava
To access and retrieve all the public data from Strava, the first step is to login. The strava_login_selen() function is used for this purpose 

### 2.2 Loop on all weeks of the interval
This section describes how to loop through all the weeks within a specified interval in order to retrieve activities in this interval

## 3. Retrieve activity data

### 3.1 Dealing with Home Trainer (HT) activity and manually input activity
This section addresses the handling of Home Trainer (HT) activities and manually input activities. Manually add the activity ID and run the cell to retrieve associated data.

### 3.2 Loop to retrieve activity data
This section covers the retrieval of activity data from Strava.

### 3.3 Loop to retrieve activity date and type
This section focuses on retrieving activity dates and types from Strava. Provide your Strava account email and password.

## Optional: 4. Deleting the data when not moving and useless field
This section covers the initial cleaning of data and removal of irrelevant fields.
