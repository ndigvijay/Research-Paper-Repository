import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.switch_page_button import switch_page

# st.sidebar.write(st.session_state)

conn = mysql.connector.connect(
    host="localhost", user="nishanthdmello", passwd="nishanth", database="rpr"
)
sql = conn.cursor()

st.title("List of all Conferences")
add_vertical_space(2)


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "add_click" not in st.session_state:
    st.session_state.add_click = False
if "c_id" not in st.session_state:
    st.session_state.c_id = "NULL"
if "edit_click" not in st.session_state:
    st.session_state.edit_click = False


def edit_click():
    st.session_state.add_click = False
    st.session_state.edit_click = True


def add_click():
    st.session_state.edit_click = False
    st.session_state.add_click = True


def butn_click(id):
    st.session_state.edit_click = False
    st.session_state.add_click = False
    st.session_state.c_id = id


def done_click(title, date, loc, org, papers):
    if st.session_state.add_click:
        query = f"INSERT INTO Conference (Title, Date, Location, Organiser) VALUES ('{title}', '{date}', '{loc}', '{org}');"
        sql.execute(query)
        conn.commit()

    if st.session_state.edit_click:
        query = f"UPDATE Conference SET Title = '{title}', Date = '{date}', Location = '{loc}', Organiser = '{org}' WHERE ID = {st.session_state.c_id};"
        sql.execute(query)
        conn.commit()

    query = f"SELECT ID FROM Conference WHERE Title = '{title}' AND Date = '{date}' AND Location = '{loc}' AND Organiser = '{org}';"
    sql.execute(query)
    data = sql.fetchall()

    for i in papers:
        query = f"UPDATE ResearchPaper SET Conference = {data[0][0]} WHERE ID = '{i}';"
        sql.execute(query)
        conn.commit()

    st.session_state.add_click = False
    st.session_state.edit_click = False


if st.session_state.logged_in:
    st.button("Add", on_click=add_click)


query = "select ID, Title from Conference;"
sql.execute(query)
data = sql.fetchall()

col1, col2, col3 = st.columns(3)

for i, title in enumerate(data):
    if i % 3 == 0:
        with col1:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],))
    elif i % 3 == 1:
        with col2:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],))
    else:
        with col3:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],))

add_vertical_space(3)

if (
    st.session_state.c_id != "NULL"
    and not st.session_state.add_click
    and not st.session_state.edit_click
):
    query = f"SELECT C.ID, C.Title, C.Date, C.Location, C.Organiser, RP.ID, RP.Title FROM ResearchPaper RP JOIN Conference C ON RP.Conference = C.ID WHERE RP.Conference = {st.session_state.c_id};"
    sql.execute(query)
    data = sql.fetchall()
    papers_dict = {}
    for i in data:
        c_id = i[0]
        c_title = i[1]
        c_date = i[2]
        c_loc = i[3]
        c_org = i[4]
        f"Paper Title : {i[6]}------->Paper ID : {i[5]}"
        papers_dict[i[5]] = i[6]

    papers = []
    for key, value in papers_dict.items():
        papers.append(value)

    f"Conference ID : {i[0]}"
    f"Conference Title : {i[1]}"
    f"Date : {i[2]}"
    f"Location : {i[3]}"
    f"Organiser : {i[4]}"

    if st.session_state.logged_in:
        st.button("Edit", on_click=edit_click)

query = "select ID, Title from ResearchPaper;"
sql.execute(query)
data = sql.fetchall()
all_papers_dict = {}
all_papers = []
for i in data:
    all_papers_dict[i[0]] = i[1]
for key, value in all_papers_dict.items():
    all_papers.append(key)

if st.session_state.add_click:
    title = st.text_input("Title")
    date = st.text_input("Date")
    loc = st.text_input("Location")
    org = st.text_input("Organiser")
    papers = st.multiselect("Papers : ", all_papers)

if st.session_state.edit_click:
    query = f"SELECT C.ID, C.Title, C.Date, C.Location, C.Organiser, RP.ID, RP.Title FROM ResearchPaper RP JOIN Conference C ON RP.Conference = C.ID WHERE RP.Conference = {st.session_state.c_id};"
    sql.execute(query)
    data = sql.fetchall()
    papers_dict = {}
    for i in data:
        c_id = i[0]
        c_title = i[1]
        c_date = i[2]
        c_loc = i[3]
        c_org = i[4]
        papers_dict[i[5]] = i[6]
    papers = []
    for key, value in papers_dict.items():
        papers.append(key)
    title = st.text_input("Title", c_title)
    date = st.text_input("Date", c_date)
    loc = st.text_input("Location", c_loc)
    org = st.text_input("Organiser", c_org)
    papers = st.multiselect("Papers : ", all_papers, papers)

if st.session_state.edit_click or st.session_state.add_click:
    st.button(
        "Done",
        on_click=done_click,
        args=(
            title,
            date,
            loc,
            org,
            papers,
        ),
    )
