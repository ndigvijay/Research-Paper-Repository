import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space

# st.sidebar.write(st.session_state)

conn = mysql.connector.connect(
    host="localhost", user="nishanthdmello", passwd="nishanth", database="rpr"
)
sql = conn.cursor()

st.title("List of all Researchers")
add_vertical_space(2)

sql.execute("select distinct Expertise from ResearcherExpertise;")
data = sql.fetchall()
all_expertise = []
for i in data:
    all_expertise.append(i[0])

if "add_click" not in st.session_state:
    st.session_state.add_click = False
if "r_id" not in st.session_state:
    st.session_state.r_id = "NULL"
if "edit_click" not in st.session_state:
    st.session_state.edit_click = False
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def add_click():
    st.session_state.edit_click = False
    st.session_state.add_click = True


if st.session_state.logged_in:
    st.button("Add", on_click=add_click)

col1, col2, col3 = st.columns(3)


def butn_click(id):
    st.session_state.add_click = False
    st.session_state.edit_click = False
    st.session_state.r_id = id


def edit_click():
    st.session_state.add_click = False
    st.session_state.edit_click = True


def r_done(rname, remail, rage, rexper):
    if st.session_state.add_click:
        query = f"INSERT INTO Researcher (Name, Email, Age) VALUES ('{rname}', '{remail}', '{rage}');"
        sql.execute(query)
        conn.commit()

        query = (
            f"select ID from Researcher where Name = '{rname}' and Email='{remail}';"
        )
        sql.execute(query)
        data = sql.fetchall()
        for i in rexper:
            query = f"INSERT INTO ResearcherExpertise (ID, Expertise) VALUES ({data[0][0]}, '{i}');"
            sql.execute(query)
            conn.commit()

    if st.session_state.edit_click:
        query = f"update Researcher set Name = '{rname}',Email =  '{remail}', Age = '{rage}' where ID = '{st.session_state.r_id}';"
        sql.execute(query)
        conn.commit()

    st.session_state.add_click = False
    st.session_state.edit_click = False


sql.execute("select ID, Name from Researcher")
data = sql.fetchall()

for i, name in enumerate(data):
    butn_key = f"r_{name[0]}"
    if i % 3 == 0:
        with col1:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],))
    elif i % 3 == 1:
        with col2:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],))
    else:
        with col3:
            st.button(name[1], key=butn_key, on_click=butn_click, args=(name[0],))

add_vertical_space(2)

if (
    st.session_state.r_id != "NULL"
    and not st.session_state.add_click
    and not st.session_state.edit_click
):
    expertise = []
    sql.execute(
        f"select RE.Expertise from Researcher R LEFT JOIN ResearcherExpertise RE ON R.ID = RE.ID where R.ID = {st.session_state.r_id};"
    )
    data = sql.fetchall()
    for i in data:
        expertise.append(i[0])

    papers_dict = {}
    sql.execute(
        f"SELECT R.ID, R.Name, R.Age, R.Email, RP.ID, RP.Title FROM Researcher R  LEFT JOIN Authorship A ON R.ID = A.Author LEFT JOIN ResearchPaper RP ON A.Paper = RP.ID WHERE R.ID = {st.session_state.r_id};"
    )
    data = sql.fetchall()
    for i in data:
        papers_dict[i[4]] = i[5]
        r_id = i[0]
        r_name = i[1]
        r_email = i[2]
        r_age = i[3]

    "Researcher ID : ", r_id
    "Researcher Name : ", r_name
    "Age : ", r_age
    "Email : ", r_email
    "Expertise : "
    for i in expertise:
        i
    "Papers :"
    for key, value in papers_dict.items():
        "Paper ID : ", key, "Paper Title : ", value

    if st.session_state.logged_in:
        st.button("Edit", on_click=edit_click)

if st.session_state.add_click and not st.session_state.edit_click:
    rname = st.text_input("Name")
    rage = st.number_input("Age", min_value=10, max_value=100)
    remail = st.text_input("Email")
    rexper = st.multiselect("Expertise", all_expertise)

if st.session_state.edit_click and not st.session_state.add_click:
    expertise = []
    sql.execute(
        f"select RE.Expertise from Researcher R LEFT JOIN ResearcherExpertise RE ON R.ID = RE.ID where R.ID = {st.session_state.r_id};"
    )
    data = sql.fetchall()
    for i in data:
        expertise.append(i[0])
    sql.execute(
        f"SELECT R.ID, R.Name, R.Age, R.Email, RP.ID, RP.Title FROM Researcher R  LEFT JOIN Authorship A ON R.ID = A.Author LEFT JOIN ResearchPaper RP ON A.Paper = RP.ID WHERE R.ID = {st.session_state.r_id};"
    )
    data = sql.fetchall()
    for i in data:
        r_id = i[0]
        r_name = i[1]
        r_age = i[2]
        r_email = i[3]
    rname = st.text_input("Name", r_name)
    rage = st.text_input("Age", r_age)
    remail = st.text_input("Email", r_email)
    rexper = st.multiselect("Papers : ", all_expertise, expertise)

if st.session_state.edit_click or st.session_state.add_click:
    st.button(
        "Done",
        on_click=r_done,
        args=(
            rname,
            remail,
            rage,
            rexper,
        ),
    )
