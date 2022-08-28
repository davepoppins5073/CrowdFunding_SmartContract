#####################
# Import / Libraries
#####################
import pandas as pd
import numpy as np
from pathlib import Path

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

#######################
# Functions
#######################

st.markdown("## Voting ❄️")
st.sidebar.markdown("## Voting ❄️")

from PIL import Image



#opening the image

image = Image.open('sauna.png')
image2 = Image.open('pool2.png')



#displaying the image on streamlit app
st.sidebar.markdown("## Voting Initiative #451")
st.sidebar.image(image, caption='Your steamy Retreat from Daily Woes')

st.sidebar.markdown("## Voting Initiative #734")
st.sidebar.image(image2, caption='Cool place to beat the heat')

readme_text = st.markdown('''
    ## Instructions
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vel lorem tincidunt, 
    congue orci id, pretium augue. Curabitur facilisis malesuada justo. Sed tincidunt 
    metus sed arcu blandit efficitur. Vestibulum ut neque sed diam dapibus imperdiet 
    id sit amet ante. In in sollicitudin est, ut bibendum lectus. Curabitur posuere 
    cursus dui. Nullam interdum eu nunc ac bibendum. Etiam id dolor laoreet nulla euismod 
    tristique. Nulla mollis condimentum auctor. Mauris ut diam ante. Maecenas at mauris 
    vulputate, hendrerit erat in, viverra libero. Nulla viverra lacus vitae urna hendrerit 
    fringilla. Aliquam pharetra justo vitae neque semper, a consequat lorem varius.
    ''')

