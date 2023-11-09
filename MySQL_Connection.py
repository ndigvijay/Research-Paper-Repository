import mysql.connector
import streamlit as st

def connect_to_mysql():

    db_config = {
        "host": "localhost",
        "user": "nishanthdmello",
        "password": "nishanth",
        "database": "rpr"
    }

    conn = mysql.connector.connect(**db_config)
    return conn


def add_state(state):
    if state not in st.session_state:
        st.session_state[state] = False
        