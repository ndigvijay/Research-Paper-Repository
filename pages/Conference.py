import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.switch_page_button import switch_page
from MySQL_Connection import *

# st.sidebar.write(st.session_state)

conn=connect_to_mysql()
sql = conn.cursor()

st.title("List of all Conferences")

add_state("logged_in")
add_state("c_add_click")
add_state("c_edit_click")
if "c_id" not in st.session_state:
    st.session_state.c_id = "NULL"


def c_edit_click():
    st.session_state.c_add_click = False
    st.session_state.c_edit_click = True


def c_add_click():
    st.session_state.c_edit_click = False
    st.session_state.c_id = "NULL"
    st.session_state.c_add_click = True


def butn_click(id):
    st.session_state.c_edit_click = False
    st.session_state.c_add_click = False
    st.session_state.c_id = id


def done_click(title, date, loc, papers):
    if st.session_state.c_add_click:
        query = f"INSERT INTO Conference (Title, Date, Location) VALUES ('{title}', '{date}', '{loc}');"
        sql.execute(query)
        conn.commit()

    if st.session_state.c_edit_click:
        query = f"UPDATE Conference SET Title = '{title}', Date = '{date}', Location = '{loc}' WHERE ID = {st.session_state.c_id};"
        sql.execute(query)
        conn.commit()

    query = f"SELECT ID FROM Conference WHERE Title = '{title}' AND Date = '{date}' AND Location = '{loc}';"
    sql.execute(query)
    data = sql.fetchall()
    st.session_state.c_id=data[0][0]

    for i in papers:
        query = f"UPDATE ResearchPaper SET Conference = '{st.session_state.c_id}' WHERE ID = '{i}';"
        sql.execute(query)
        conn.commit()

    st.session_state.c_add_click = False
    st.session_state.c_edit_click = False


if st.session_state.logged_in:
    st.button("Add", on_click=c_add_click,use_container_width=True)


query = "select ID, Title from Conference;"
sql.execute(query)
data = sql.fetchall()

col1, col2, col3 = st.columns(3)

for i, title in enumerate(data):
    if i % 3 == 0:
        with col1:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],),use_container_width=True)
    elif i % 3 == 1:
        with col2:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],),use_container_width=True)
    else:
        with col3:
            st.button(title[1], key=title[0], on_click=butn_click, args=(title[0],),use_container_width=True)


if (
    st.session_state.c_id != "NULL"
    and not st.session_state.c_add_click
    and not st.session_state.c_edit_click
):
    
    query = f"SELECT RP.ID, RP.Title FROM ResearchPaper RP JOIN Conference C ON RP.Conference = C.ID WHERE RP.Conference = '{st.session_state.c_id}';"
    sql.execute(query)
    data = sql.fetchall()
    papers_dict = {}
    for i in data:
        papers_dict[i[0]] = i[1]
    for key,value in papers_dict.items():
        f"Paper Title : {value}------->Paper ID : {key}"
    papers = []
    for key, value in papers_dict.items():
        papers.append(key)
        
    query = f"SELECT C.ID, C.Title, C.Date, C.Location FROM Conference C WHERE C.ID = '{st.session_state.c_id}';"
    sql.execute(query)
    data = sql.fetchall()
    c_id = data[0][0]
    c_title = data[0][1]
    c_date = data[0][2]
    c_loc = data[0][3]

    f"Conference Title : {c_title}"
    f"Date : {c_date}"
    f"Location : {c_loc}"

    if st.session_state.logged_in:
        st.button("Edit", on_click=c_edit_click)

query = "select ID, Title from ResearchPaper;"
sql.execute(query)
data = sql.fetchall()
all_papers_dict = {}
all_papers = []
for i in data:
    all_papers_dict[i[0]] = i[1]
for key, value in all_papers_dict.items():
    all_papers.append(key)

if st.session_state.c_add_click and not st.session_state.c_edit_click:
    title = st.text_input("Title")
    date = st.date_input("Date")
    loc = st.text_input("Location")
    papers = st.multiselect("Papers : ", all_papers)

if st.session_state.c_edit_click and not st.session_state.c_add_click:
    query = f"SELECT RP.ID, RP.Title FROM ResearchPaper RP JOIN Conference C ON RP.Conference = C.ID WHERE RP.Conference = '{st.session_state.c_id}';"
    sql.execute(query)
    data = sql.fetchall()
    papers_dict = {}
    for i in data:
        papers_dict[i[0]] = i[1]
    papers = []
    for key, value in papers_dict.items():
        papers.append(key)
        
    query = f"SELECT C.ID, C.Title, C.Date, C.Location FROM Conference C WHERE C.ID = '{st.session_state.c_id}';"
    sql.execute(query)
    data = sql.fetchall()
    c_id = data[0][0]
    c_title = data[0][1]
    c_date = data[0][2]
    c_loc = data[0][3]
    title = st.text_input("Title", c_title)
    date = st.date_input("Date", c_date)
    loc = st.text_input("Location", c_loc)
    papers = st.multiselect("Papers : ", all_papers, papers)

if st.session_state.c_edit_click or st.session_state.c_add_click:
    st.button(
        "Done",
        on_click=done_click,
        args=(
            title,
            date,
            loc,
            papers,
        ),
    )
