#####################
# Import / Libraries
#####################
import pandas as pd
import numpy as np
from pathlib import Path

import streamlit as st
import hashlib
from dataclasses import dataclass
from typing import Any, List
import yfinance as yf

from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

from bs4 import BeautifulSoup 
import requests 
import time
from crypto_wallet import generate_account, get_balance, send_transaction

#######################
# Functions
#######################

def housing_data():
    
    # This is going to formulate the Basic Housing Data 
    # We need to know the USD to ETH conversion rate 
    eth_price = crypto_price_cnvrtr()
    eth_price = eth_price[:8]
    eth = eth_price.replace(",","")
    eth = float(eth)
    
    # Reading in csv of Addresses & adding columns
    addresses = pd.read_csv("address.csv")
    addresses = addresses.rename(columns={"Real-Estate Owner":"Owner","House Valuation":"Valuation"})
    addresses = addresses.set_index("Address")


    addresses[addresses.columns[1:]] = addresses[addresses.columns[1:]].replace('[\$,]', '', regex=True).astype(float)
    addresses['HOA_Dues'] = addresses['Valuation']* 0.015
    addresses['Eth_Dues'] =  addresses['HOA_Dues'] / eth
    add_num = len(addresses)
    
 

    #addresses['Ganache_add'] = gan_addrss['Address'].values
    gan_addrss = pd.read_csv("addr_img - Sheet1.csv")
    from_account = gan_addrss.head(add_num)
    addresses['Ganache_add'] = from_account['Address'].values
    addresses['house_img'] = from_account['Image'].values
    
    return(addresses)



def crypto_price_cnvrtr():
    
    coin = "Ethereum"
    
    # Get the URL df=pd.DataFrame()
    url = "https://www.google.com/search?q="+coin+"+price"
    
    # Make a request to the website
    HTML = requests.get(url) 
  
    # Parse the HTML
    soup = BeautifulSoup(HTML.text, 'html.parser') 
  
    # Find the current ETH price 
    text = soup.find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).find("div", attrs={'class':'BNeawe iBp4i AP7Wnd'}).text
    
    # Return the text 
    return text

# source:https://betterprogramming.pub/get-the-price-of-cryptocurrencies-in-real-time-using-python-cdaf07516479

######################
# Code
######################

housing_df = housing_data()
address_db = housing_df.to_dict('index')
address_list = housing_df.index.values.tolist()
address_db = housing_df.to_dict('index')
address_list = housing_df.index.values.tolist()

BTC_Ticker = yf.Ticker("BTC-USD")
BTC_Data = BTC_Ticker.history(period="14d")
BTC_Data = BTC_Data.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
df_daily_returns = BTC_Data.pct_change()
df_daily_returns = df_daily_returns.dropna()



def get_people(w3):
    """Display the database of Fintech Finders candidate information."""
    db_list = list(address_db.values())

  

    #for number in range(len(address_list)):
    #    #st.image("House_Image:",address_db[number][5], width=200)
    #    st.write("Owner: ", address_db[number][0])
    #    st.write("House Valuation: ", address_db[number][1])
    #    st.write("HOA_Dues: ", address_db[number][2])
    #    st.write("Eth_Dues: ", address_db[number][3], "eth")
    #    st.write("From_Acct: ", address_db[number][4], "eth")
    #    st.text(" \n")

##################
# STREAMLIT CODE
##################


# Streamlit application headings
st.markdown("# Community Voting!")
st.markdown("## Pay and Vote like a rabid bear!")
st.text(" \n")

from PIL import Image
image = Image.open('hoa-dues-1-800x400-1.jpeg')

st.image(image, caption='Just dont pay dues, Set Policies for Our Community')

################################################################################
# Streamlit Sidebar Code - Start
################################################################################

# Generate the Account for the home Owner
st.sidebar.markdown("## Client Account Address and Ethernet Balance in Ether")
account = generate_account()


# Write the client's Ethereum account address to the sidebar
st.sidebar.write(account.address)

# Write the Account Balance for the Address
ether_balance = get_balance(w3, account.address)
st.sidebar.write(ether_balance)

# Create a select box to chose a FinTech Hire candidate
hoa_address = st.sidebar.selectbox('Select an Address', address_list)
rec_list = list(housing_df.loc[hoa_address])

# Create a input field to record the number of hours the candidate worked
#hours = st.sidebar.number_input("Number of Hours")

st.sidebar.markdown("## Owner, HOA Dues, and Eth Cost")

# Identify the FinTech Hire candidate
candidate = rec_list[0]
hoa_dues = rec_list[2]
eth_due = rec_list[3]
from_acct = rec_list[4]
home_image = rec_list[5]

#owner_acct = from_acct.address
#

# Write the Fintech Finder candidate's name to the sidebar
from PIL import Image
image2 = Image.open(home_image)

st.sidebar.image(image2, caption='Home Sweet Home')

st.sidebar.write("1. Home Owner:", candidate)
st.sidebar.write("2. Home Owner Assoc Dues:", hoa_dues)
st.sidebar.write("3. Ethereum Amt Due:",eth_due)
#st.sidebar.write("4. From_Account:",from_acct.address)
#st.sidebar.write(from_acct.address)

st.sidebar.markdown("## Ethereum Daily Percent Change")
st.sidebar.write("These are what the Ethereum Prices have been behaving over the last 14 days") 
my_chart2 = st.sidebar.line_chart(df_daily_returns)



# Identify the FinTech Finder candidate's hourly rate
#hourly_rate = address_db[person][3]

# Write the inTech Finder candidate's hourly rate to the sidebar
#st.sidebar.write(hourly_rate)

# Identify the FinTech Finder candidate's Ethereum Address
#candidate_address = address_db[person][1]

# Write the inTech Finder candidate's Ethereum Address to the sidebar
#st.sidebar.write(candidate_address)

# Write the Fintech Finder candidate's name to the sidebar
#st.sidebar.markdown("## Total Wage in Ether")



##########################################

#wage = hourly_rate * hours 

# @TODO
# Write the `wage` calculation to the Streamlit sidebar
#st.sidebar.write(wage)


if st.sidebar.button("Send Transaction"):

    # @TODO
    # Call the `send_transaction` function and pass it 3 parameters:
    # Your `account`, the `candidate_address`, and the `wage` as parameters
    # Save the returned transaction hash as a variable named `transaction_hash`
    transaction_hash = send_transaction(w3, from_acct, account, eth_due)

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)

    # Celebrate your successful payment
    st.balloons()

# The function that starts the Streamlit application
# Writes FinTech Finder candidates to the Streamlit page
get_people(w3)