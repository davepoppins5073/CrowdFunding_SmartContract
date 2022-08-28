#####################
# Import / Libraries
#####################
import pandas as pd
import numpy as np
from pathlib import Path
import glob
import os

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html

import hashlib
from dataclasses import dataclass
from typing import Any, List
import yfinance as yf

from web3 import Web3
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))

from bs4 import BeautifulSoup 
import requests 
import time
from crypto_wallet import generate_account, get_balance

from bip44 import Wallet
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

###########################################
# Functions 1: Page Structure in Streamlit
###########################################

def main_page():
    st.markdown("# HOA Community Voting!")
    st.sidebar.markdown("# Owner, HOA Dues, & Eth Cost")

def page2():
    st.markdown("# HOA Voting ❄️")
    st.sidebar.markdown("# Page 2 ❄️")


page_names_to_funcs = {
    "Main Page": main_page,
    "Voting": page2,
}

selected_page = st.sidebar.selectbox("# Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

###############################################
# Functions 2: Non-page Strcuture Calculations
###############################################

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


def housing_data():
    
    # This is going to formulate the Basic Housing Data in no order
    #     1. Calculate dues in ETH and USD
    #     2. Convert USD to ETH conversion rate 
    #     3. Create  the df of address
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
    
 

    gan_addrss = pd.read_csv("addr_img - Sheet1.csv")
    from_account = gan_addrss.head(add_num)
    addresses['Ganache_add'] = from_account['Address'].values
    addresses['house_img'] = from_account['Image'].values
    
    return(addresses)


def send_transaction(w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w3.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas({"to": to_account.address, "from": account.address, "value": value})



    # Construct a raw transaction
    raw_tx = {
        "to": to_account.address,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

######################
#    Code
######################

housing_df = housing_data()
names = list(housing_df['Owner'])

ganache_addys =list()
for number in range(len(names)):
    ganache_addys.append(w3.eth.get_accounts()[number])

housing_df['ganache_addr'] = ganache_addys


address_db = housing_df.to_dict('index')
address_list = housing_df.index.values.tolist()

BTC_Ticker = yf.Ticker("BTC-USD")
BTC_Data = BTC_Ticker.history(period="14d")
BTC_Data = BTC_Data.drop(['Open', 'High', 'Low', 'Volume', 'Dividends', 'Stock Splits'], axis=1)
df_daily_returns = BTC_Data.pct_change()
df_daily_returns = df_daily_returns.dropna()





    



#def get_houses(w3):
#    """ Display the database of Home Owner."""
#    db_list = list(address_db.values())



##################
# STREAMLIT CODE
##################


# Streamlit application headings
#st.markdown("# Community Voting!")
st.markdown("## Pay & Vote like a rabid bear!")
st.text(" \n")

from PIL import Image
image = Image.open('hoa-dues-1-800x400-1.jpeg')

st.image(image, caption='Just dont pay dues, Set Policies for Our Community')
gbizl_addy = st.selectbox('Select an Address', ganache_addys)

st.markdown("## Ethereum Daily Percent Change")
st.write("These are what the Ethereum Prices have been behaving over the last 14 days") 
my_chart2 = st.line_chart(df_daily_returns)


log_file_df = pd.read_csv("ganache-20220825-020302.log", names=['LOG','Comment'], sep='\r\n')
st.markdown("## Transaction LOGS ")
st.dataframe(log_file_df) 


################################################################################
# Streamlit Sidebar Code - Start
################################################################################

# Generate the Account for the home Owner
st.sidebar.markdown("# Owner Acct & Ether Balance")
account = generate_account()


# Convert private key into an Ethereum account
to_account = Account.privateKeyToAccount("430a8b95844a140ee831ddfb8b5491b60a33b90fa4ad0439dc688aefa499dc0c")


# Write the client's Ethereum account address to the sidebar
st.sidebar.write("### HOA ACCT:")
st.sidebar.write(account.address)


# Write the Account Balance for the Address
ether_balance = get_balance(w3, account.address)
st.sidebar.write("### Acct Balance:", ether_balance)

# Create a select box to chose an Address
hoa_address = st.sidebar.selectbox('Select an Address', address_list)
rec_list = list(housing_df.loc[hoa_address])


st.sidebar.markdown("## Owner, HOA Dues, and Eth Cost")

# Identify the HomeOwner
candidate = rec_list[0]
hoa_dues = rec_list[2]
eth_due = rec_list[3]
home_image = rec_list[5]


# Write the Fintech Finder candidate's name to the sidebar
from PIL import Image
image2 = Image.open(home_image)

st.sidebar.image(image2, caption='Home Sweet Home')

st.sidebar.write("1. Home Owner:", candidate)
st.sidebar.write("2. Home Owner Assoc Dues:", hoa_dues)
st.sidebar.write("3. Ethereum Amt Due:",eth_due)





##########################################
#   Side Bar: Transactions
##########################################

if st.sidebar.button("Send Transaction"):

    transaction_hash = send_transaction(w3, account ,to_account, eth_due)

    # Markdown for the transaction hash
    st.sidebar.markdown("#### Validated Transaction Hash")

    # Write the returned transaction hash to the screen
    st.sidebar.write(transaction_hash)
    st.write("## Transaction HASH",transaction_hash)

    # Celebrate your successful payment
    st.balloons()

#get_houses(w3)