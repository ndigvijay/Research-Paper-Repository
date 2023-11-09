import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *

# st.sidebar.write(st.session_state)
conn=connect_to_mysql()
sql = conn.cursor()

st.title("List of all Researchers")

all_expertise = []
sql.execute("select * from Expertise;")
data = sql.fetchall()
for i in data:
    all_expertise.append(i[0])

add_state("r_add_click")
add_state("r_edit_click")
add_state("logged_in")
if "r_id" not in st.session_state:
    st.session_state.r_id = "NULL"


def r_add_click():
    st.session_state.r_edit_click = False
    st.session_state.r_id = "NULL"
    st.session_state.r_add_click = True




def butn_click(id):
    st.session_state.r_add_click = False
    st.session_state.r_edit_click = False
    st.session_state.r_id = id


def r_edit_click():
    st.session_state.r_add_click = False
    st.session_state.r_edit_click = True


def r_done(rname, remail, rexper):
    if rname=="" or remail=="" or len(rexper)==0:
        return
    if st.session_state.r_add_click:
        query = f"INSERT INTO Researcher (Name, Email) VALUES ('{rname}', '{remail}');"
        sql.execute(query)
        conn.commit()

    if st.session_state.r_edit_click:
        query = f"update Researcher set Name = '{rname}',Email =  '{remail}' where ID = '{st.session_state.r_id}';"
        sql.execute(query)
        conn.commit()
        
        
    query = (
        f"select ID from Researcher where Name = '{rname}' and Email='{remail}';"
    )
    sql.execute(query)
    data = sql.fetchall()
    st.session_state.r_id=data[0][0]
    
    query=f"delete from ResearcherExpertise where ID = '{st.session_state.r_id}'"
    sql.execute(query)
    conn.commit()

    for i in rexper:
        query = f"INSERT INTO ResearcherExpertise (ID, Expertise) VALUES ('{st.session_state.r_id}', '{i}');"
        sql.execute(query)
        conn.commit()

    st.session_state.r_add_click = False
    st.session_state.r_edit_click = False


if st.session_state.logged_in:
    st.button("Add", on_click=r_add_click,use_container_width=True)

col1, col2, col3 = st.columns(3)

sql.execute("select ID, Name from Researcher")
data = sql.fetchall()

for i, name in enumerate(data):
    butn_key = f"r_{name[0]}"
    if i % 3 == 0:
        with col1:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],),use_container_width=True)
    elif i % 3 == 1:
        with col2:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],),use_container_width=True)
    else:
        with col3:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],),use_container_width=True)


if (
    st.session_state.r_id != "NULL"
    and not st.session_state.r_add_click
    and not st.session_state.r_edit_click
):
    expertise = []
    sql.execute(
        f"SELECT RE.Expertise FROM ResearcherExpertise RE JOIN Researcher R ON R.ID = RE.ID WHERE R.ID = '{st.session_state.r_id}';"
    )
    data = sql.fetchall()
    for i in data:
        expertise.append(i[0])

    papers_dict = {}
    sql.execute(
        f"SELECT RP.ID, RP.Title FROM Researcher R LEFT JOIN Authorship A ON R.ID = A.Author LEFT JOIN ResearchPaper RP ON A.Paper = RP.ID WHERE R.ID = '{st.session_state.r_id}';"
    )
    data = sql.fetchall()
    for i in data:
        papers_dict[i[0]] = i[1]

    sql.execute(f"SELECT R.ID, R.Name, R.Email FROM Researcher R WHERE R.ID = '{st.session_state.r_id}';")
    data = sql.fetchall()
    for i in data:
        r_id = i[0]
        r_name = i[1]
        r_email = i[2]

    "Researcher Name : ", r_name
    "Email : ", r_email
    "Expertise : "
    for i in expertise:
        i
    "Papers :"
    for key, value in papers_dict.items():
        "Paper ID : ", key, "Paper Title : ", value

    if st.session_state.logged_in:
        st.button("Edit", on_click=r_edit_click)

if st.session_state.r_add_click and not st.session_state.r_edit_click:
    rname = st.text_input("Name")
    remail = st.text_input("Email")
    rexper = st.multiselect("Expertise", all_expertise)

if st.session_state.r_edit_click and not st.session_state.r_add_click:
    expertise = []
    sql.execute(
        f"SELECT RE.Expertise FROM Researcher R JOIN ResearcherExpertise RE ON R.ID = RE.ID WHERE R.ID = '{st.session_state.r_id}';"
    )
    data = sql.fetchall()
    for i in data:
        expertise.append(i[0])
    sql.execute(
        f"SELECT R.ID, R.Name, R.Email FROM Researcher R WHERE R.ID = '{st.session_state.r_id}';"
    )
    data = sql.fetchall()
    for i in data:
        r_id = i[0]
        r_name = i[1]
        r_email = i[2]
    rname = st.text_input("Name", r_name)
    remail = st.text_input("Email", r_email)
    rexper = st.multiselect("Expertise : ", all_expertise, expertise)

if st.session_state.r_edit_click or st.session_state.r_add_click:
    st.button(
        "Done",
        on_click=r_done,
        args=(
            rname,
            remail,
            rexper,
        ),
    )
