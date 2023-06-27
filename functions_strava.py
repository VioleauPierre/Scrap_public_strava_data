


####### Functions used in Data_recovery #######



import requests
import json
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
import numpy as np


### Saving an ID list to a txt file ###

def save_list(List_to_save, File_name) :
    file_list = open(f"{File_name}.txt","w")
    for ID in List_to_save:
        file_list.write(ID+"\n")
    file_list.close()
    

### Loading txt file to retrieve activity ID saved ###

def load_list(File_name):
    # opening the file in read mode
    my_file = open(f"{File_name}.txt", "r")
  
    # reading the file
    data = my_file.read()

    List_name = data.split("\n")
    my_file.close()
    return List_name
    
### Save the dataset in a json file ###

def save_dataset(Dataset):
    # Define the filename for the JSON file
    filename = "Dataset_training.json"

    # Save the dictionary as a JSON file
    with open(filename, "w") as f:
        json.dump(Dataset, f)
        
        
### Load the dataset ###

def load_dataset():
    # Define the filename for the JSON file
    filename = "Dataset_training.json"

    # Open the JSON file and load its contents into a dictionary
    with open(filename, "r") as f:
        Dataset = json.load(f)

    # Print the dictionary
    return Dataset

    
### login to strava with selenium ###

def strava_login_selen():
    
    #Initialisation of variables
    url_co = "https://www.strava.com/login"
    email = "XXXXXXX@XXXXX.XXX"
    password = "XXXXXX"

    # Set-up of Selenium
    driver = webdriver.Chrome()
    url = driver.command_executor._url
    session_id = driver.session_id
    driver.maximize_window()
    driver.get(url_co)

    # Find the email and password fields and fill them in
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    print(email_field)
    email_field.send_keys(email)

    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)

    # Submit the login form
    password_field.send_keys(Keys.RETURN)

    # Wait for the login process to complete and the dashboard to load
    WebDriverWait(driver, 10).until(EC.url_contains("dashboard"));
    
    # Return the driver object
    return driver
 

### create the list of week we want to loop on ###

def interval_loop(start,end):

    #Separating year and week
    year, week = divmod(start, 100)

    interval = [start]

    while start < end:
        week += 1
        if week > 52:
            year += 1
            week = 1
        start = year * 100 + week
        if start <= end:
            interval.append(start)

    return interval
    
    
### Function to retrieve activity ID of a selected interval of weeks ###

def get_activity_ID(interval,driver):
    #creation of the list that will contain all the activity IDs
    List_ID_all=[]
    actions = ActionChains(driver)
    #step for the scrolling
    step=200


    #Loop on all the weeks from 2011 week 52
    #interval=[202305]
    for w in interval:
    
        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        driver.get(f"https://www.strava.com/pros/ENTER THE USER ID#interval?interval={w}&interval_type=week&chart_type=miles&year_offset=0")
        elem = driver.find_element(By.ID,"interval-rides")

        time.sleep(1.1)


        # Coordonate of the element
        location = elem.location_once_scrolled_into_view
        time.sleep(4)
        width = elem.size['width']
        height = elem.size['height']
        x=location.get("x")
        y=location.get("y")

        Iteration_scroll = len(list(range(0, height+1, step))) + 3
   
        #Loop on all the activity of one week to retrieve the url

        for i in range(0,Iteration_scroll,1):
            actions.move_to_element_with_offset(elem,-500,0).click().perform()  #click to avoid block if a click is done on an element that open new element (groupe ride for ex)
            actions.move_to_element_with_offset(elem,140,-160).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
            time.sleep(0.11)
            driver.execute_script("window.scrollTo(0, window.scrollY + 200)")
            time.sleep(0.02)

        #loop to isolate the ID from the url 

        for j in range(1,Iteration_scroll,1):   
            driver.switch_to.window(driver.window_handles[-1])
            current_url = driver.current_url.split('/')[-1]
            if len(current_url)<=10:
                List_ID_all.append(current_url)
            driver.execute_script("window.close();")
    #Removing duplicate value
    List_ID = []
    [List_ID.append(x) for x in List_ID_all if x not in List_ID]
    List_ID.sort()
    len(List_ID)
    return List_ID


### Function to retrieve activity data and store it in the dataset ###

def get_activity_data(List_ID_Load,Dataset,driver):
    # Loop for the outdoor ride 
    for ID in List_ID_Load : 
        if ID in Dataset :
            time.sleep(0.01)
        else :
            print(ID)
            # Open new window which contain the activity data
            driver.switch_to.window(driver.window_handles[0])
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(f"https://www.strava.com/activities/{ID}/streams?stream_types[]=velocity_smooth&stream_types[]=watts&stream_types[]=watts_calc&stream_types[]=heartrate&stream_types[]=cadence&stream_types[]=temp&stream_types[]=moving&stream_types[]=distance&stream_types[]=time&stream_types[]=altitude&stream_types[]=grade_smooth")
            time.sleep(0.5)
            # Recover all the content
            activity_raw=driver.page_source
    
            # Keep only the useful infos
            activity_clean=activity_raw.split('">')[2].split('<')[0]
    
            # Convert them as dictionnary
            activity_dict = json.loads(activity_clean)
    
            # Add them to the dataset
            Dataset[ID]=activity_dict
            driver.execute_script("window.close();")
        time.sleep(0.4)
    return Dataset


### Function to retrieve activity date and type and store them ###

def get_activity_type_date(session,Dataset):
    for ID in Dataset : 
        if "date" in Dataset[ID] :
            time.sleep(0.01) 
        else :
            # Fetch the web page
            url = f"https://www.strava.com/activities/{ID}"

            # Send a GET request to the URL and retrieve the HTML content
            response = session.get(url)
            print(response)
            time.sleep(1)
            html_content = response.content

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            print(ID)
            # Recover the date of the activity
            date_raw = soup.find('div', {'data-react-class': 'ADPKudosAndComments'})['data-react-props'].split('start_date":"')[1].split('T')[0]
            time.sleep(0.3)
    
            # Recover the type of activity
            type_raw = soup.find('title')
            type_clean = type_raw.string.split('| ')[1].split(' |')[0]
    
            # Convert the date to the desired format
            date_clean = datetime.strptime(date_raw,'%Y-%m-%d').strftime('%d/%m/%Y')
            #print(datetime_final)
    
            # Add the date and type to the correspnding activity in the dataset
            Dataset[ID]["date"]=date_clean
            Dataset[ID]["type"]=type_clean
    return Dataset


### Function to calculate the normalized power ###

def cycling_norm_power(Power):

    WindowSize = 30; # second rolling average

    NumberSeries = pd.Series(Power)
    NumberSeries = NumberSeries.dropna()
    Windows      = NumberSeries.rolling(WindowSize)
    Power_30s    = Windows.mean().dropna()

    NP = round((((Power_30s**4).mean())**0.25),0)

    return(NP)


### Function to calculate the max power for a specify duration in second ###

def best_power_duration(power,duration):

    window_size = duration
    series = np.array(power)
    windows = np.lib.stride_tricks.sliding_window_view(series, window_size)
    avg_powers = np.nanmean(np.nan_to_num(windows, nan=np.nan), axis=1)
    best_power = np.nanmax(avg_powers)

    return(best_power)