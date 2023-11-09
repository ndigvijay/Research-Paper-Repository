import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from MySQL_Connection import *

# st.sidebar.write(st.session_state)

add_state("logged_in")

if st.session_state.logged_in:
    st.success("Logged In")
else:
    st.error("Logged Out")

def logged_in():
    st.session_state.logged_in = True
    
def logged_out():
    st.session_state.logged_in = False


def check_pass():
    if password == "yo":
        logged_in()

if not st.session_state.logged_in:
    password = st.text_input("Password", type="password")
    st.button("Login", on_click=check_pass)


if st.session_state.logged_in:
    st.button("Logout", on_click=logged_out)
