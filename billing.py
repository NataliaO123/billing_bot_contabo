# billing.py

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Loading data from .env
load_dotenv()

# Getting data from .env
username = os.getenv('CONTABO_USERNAME')
password = os.getenv('CONTABO_PASSWORD')

# URL of login page and secure page
login_url = 'https://my.contabo.com/account/login'
payment_url = 'https://my.contabo.com/account/payment'

def get_payment_info():
    # Creating a session
    session = requests.Session()

    # Performing a GET request to the login page to get tokens
    response = session.get(login_url)
    
    if response.status_code == 200:
        # Creating a BeautifulSoup Object for Parsing HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extracting token values ​​from HTML code
        token_key = soup.find('input', {'name': 'data[_Token][key]'}).get('value')
        token_fields = soup.find('input', {'name': 'data[_Token][fields]'}).get('value')
        token_unlocked = soup.find('input', {'name': 'data[_Token][unlocked]'}).get('value')
        
        # Generating payload for POST request
        login_payload = {
            '_method': 'POST',
            'data[_Token][key]': token_key,
            'data[Account][username]': username,
            'data[Account][password]': password,
            'x': '58',
            'y': '8',
            'data[_Token][fields]': token_fields,
            'data[_Token][unlocked]': token_unlocked
        }
        
        # Performing a POST request to login
        response = session.post(login_url, data=login_payload)
        
        # Checking for successful login
        if response.url == login_url:
            return f"Failed to sign in. Please check your login and password for {username}."
        
        # GET request to a secure page
        response = session.get(payment_url)
        
        # Verifying that the page was successfully received
        if response.status_code == 200:
            # Creating a BeautifulSoup Object for Parsing HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the desired element and extract the text
            div_content = soup.find('div', style="margin:auto; width:500px; font-size:16px; font-weight:bold")
            
            if div_content:
                # Received text
                result_text = div_content.get_text(strip=True)
                return f"Logged in: {username}\n{result_text}"
            else:
                return f"Logged in: {username}\nElement not found."
        else:
            return f"Logged in: {username}\nFailed to get page, status code: {response.status_code}"
    else:
        return f"{username}\nFailed to get login page, status code: {response.status_code}"
