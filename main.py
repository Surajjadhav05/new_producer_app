
import random
import string
import json
import streamlit as st 
import pyTigerGraph as tg
  
  
def generate_random_alphanumeric_string(length):

    characters = string.ascii_letters + string.digits
    
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string  

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
@st.cache_resource
def setup_tg_connection():
    hostName = "https://172.16.20.71/"
    graphName = "CreditCardFraud"
    secret ="crupk3h01dhv9i8quodlb1r521bbuaa0"
    conn = tg.TigerGraphConnection(host=hostName,graphname=graphName, gsqlSecret=secret,tgCloud=False)
    conn = tg.TigerGraphConnection(host=hostName,graphname=graphName, gsqlSecret=secret,tgCloud=False,apiToken=conn.getToken(secret)[0])
    return conn
