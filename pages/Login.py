import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# st.sidebar.write(st.session_state)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

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

    else:
        st.error("Incorrect Password")

if not st.session_state.logged_in:
    password = st.text_input("Password", type="password")
    st.button("Login", on_click=check_pass)


if st.session_state.logged_in:
    st.button("Logout", on_click=logged_out)
