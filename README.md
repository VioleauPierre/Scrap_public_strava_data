# Strava Activity Data Retrieval
This project is aimed at retrieving public activity data of a user on Strava without using the official API. It utilizes web scraping techniques with the help of the Selenium and BeautifulSoup libraries in Python.

Table of Contents
Open and save file
Retrieve activity ID
2.1 Login to Strava
2.2 Loop on all weeks of the interval
2.3 Dealing with Home Trainer (HT) activity and manually input activity
Retrieve activity data
3.1 Loop to retrieve activity data
3.2 Loop to retrieve activity date and type
Deleting the data when not moving and useless field



## 1. Open and save file
To save the data and load it later, the project provides functions for saving and loading lists and datasets.

## 2. Retrieve activity ID 
This section covers the retrieving  of the activity IDs from Strava for a given user  --> Modify the function in functions_strava.py to retrieve the activity for a specific user by specifying their ID, also enter your Strava account email and password.

### 2.1 Login to Strava
To access and retrieve all the public data from Strava, the first step is to login. The strava_login_selen() function is used for this purpose 

### 2.2 Loop on all weeks of the interval
This section describes how to loop through all the weeks within a specified interval in order to retrieve activities in this interval

## Retrieve activity data

### 3.1 Dealing with Home Trainer (HT) activity and manually input activity
This section covers the handling of Home Trainer (HT) activities and manually input activities. Add manually the activity ID and then run the cell to retrieve the data associated

### 3.2 Loop to retrieve activity data
This section covers the retrieving  of the activity data from Strava. 

### 3.3 Loop to retrieve activity date and type
This section covers the retrieving  of the activity date and type from Strava. --> Enter your Strava account email and password.

## 4. Deleting the data when not moving and useless field (Optionnal)
This section covers a first cleaning of data and removing of useless field
