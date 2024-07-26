import streamlit as st 
from streamlit_lottie import st_lottie_spinner
import pandas as pd
import json
from kafka import KafkaProducer
from main import load_lottiefile,generate_random_alphanumeric_string,setup_tg_connection
import json

lottie_file = "Animation-1716966760564.json"
lottie_animation = load_lottiefile(lottie_file)

with st.sidebar:
    st.image("NVlogo.png",width=150)
    st.header("Novigo Solutions")
    

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

if st.session_state.logged_in:
    if st.sidebar.button("Log out"):
        logout()
else:
    if st.sidebar.button("Log in"):
        login()

if not st.session_state.logged_in:
    st.title("Please log in to access the application.")
    st.stop()

@st.cache_resource
def connect_to_producer(ip="172.16.20.71:9092"):
    Producer = KafkaProducer(bootstrap_servers=[ip],
                         value_serializer=lambda x:json.dumps(x).encode('utf-8')
                         ) 
    return Producer

lottie_file = "Animation-1716966760564.json"
lottie_animation = load_lottiefile(lottie_file)

st.title("Online Shopping Site")
connection=-1
try:
    Producer=connect_to_producer()
    conn=setup_tg_connection()
    connection=1
except:
    st.write("Unable to connect kafka broker!")
    
df=pd.DataFrame()
if connection==1:
    try:
        merchant=st.text_input(label="Merchant Name towards payment initiated!")
        category=st.text_input(label="Category of product bought!")
        transaction_datetime=st.text_input(label="Transaction date and time!")
        location=st.text_input(label="Location from where transaction initiated!")
        cardnumber=int(st.number_input(label="Enter card number!"))
        amount=st.number_input(label="Transaction Amount!")
        if len(location)>0:
            merchant_lat=float(location.split(",")[0])
            merchant_long=float(location.split(",")[1])
            transID=generate_random_alphanumeric_string(15)
    
            data={"cc_num":cardnumber,"trans_num":transID,"category":category,"amt":amount,"merchant":merchant,"merch_lat":merchant_lat,"merch_long":merchant_long,"transaction_datetime":transaction_datetime,
            "merch_loc_id":location}
            df=pd.DataFrame(data,index=[0])
    except:
        st.write("Please provide valid details!")
        
    details=st.button("Submit Details")
    if details==True:
        if len(df)>0:
            with st_lottie_spinner(lottie_animation, height=200, key=f"loading_animation_x1"):
                placeholder_loading = st.empty()
                Producer.send("creditcardfraud", value=df.to_dict())
                response=conn.runInstalledQuery("get_ml_prediction",params={"transactionID":transID})[0]["prediction"]
            
            
                placeholder_loading.text("Transaction in progress, please wait...")
                while response != 0 and response != 1:
                    response=conn.runInstalledQuery("get_ml_prediction",params={"transactionID":"050f65bec17b3a90ee6e75dec69fe438"})[0]["prediction"]
                    #response=-1
            if response ==1:
                placeholder_loading.text("Transaction Declined")
        
            elif response==0:
                placeholder_loading.text("Transaction Accepted")
                st.write("Thank you for shopping with us!")
            
        else:
            st.write("Please enter valid card details!")
    
    
        
        
