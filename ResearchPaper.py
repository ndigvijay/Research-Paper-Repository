import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space

# st.sidebar.write(st.session_state)

conn = mysql.connector.connect(
    host="localhost", user="nishanthdmello", passwd="nishanth", database="rpr"
)
sql = conn.cursor()

st.title("List of all Papers")
add_vertical_space(2)

if "add_click" not in st.session_state:
    st.session_state.add_click = False
if "p_add_rev" not in st.session_state:
    st.session_state.p_add_rev = False
if "p_id" not in st.session_state:
    st.session_state.p_id = "NULL"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "search_btn" not in st.session_state:
    st.session_state.search_btn = False


def butn_click(id, count):
    st.session_state.p_id = id
    count += 1
    query = f"UPDATE ResearchPaper SET CitationCount = '{count}' WHERE ID = {id};"
    sql.execute(query)
    conn.commit()
    st.session_state.add_click=False
    st.session_state.p_add_rev=False


def add_click():
    st.session_state.add_click = True
    st.session_state.p_add_rev = False


def p_del():
    query = f"DELETE FROM Review WHERE Paper = {st.session_state.p_id};"
    sql.execute(query)
    conn.commit()
    query = f"DELETE FROM Authorship WHERE Paper = {st.session_state.p_id};"
    sql.execute(query)
    conn.commit()
    query = f"DELETE FROM ResearchPaper WHERE ID = {st.session_state.p_id};"
    sql.execute(query)
    conn.commit()
    st.session_state.p_id = "NULL"
    st.success("Deleted Research Paper Successfully")


def p_add_rev():
    st.session_state.p_add_rev = True


def p_done_add(title, authors):
    date = datetime.now().date()
    query = f"INSERT INTO ResearchPaper (Title, PublicationDate, CitationCount) VALUES ('{title}', '{date}', 0);"
    sql.execute(query)
    conn.commit()
    query = f"SELECT ID FROM ResearchPaper WHERE Title = '{title}' AND PublicationDate = '{date}';"
    sql.execute(query)
    data = sql.fetchall()
    for author in authors:
        query = f"INSERT INTO Authorship (Paper, Author) VALUES ('{data[0][0]}', '{author}');"
        sql.execute(query)
        conn.commit()

    st.session_state.add_click=False


def p_done_rev(title):
    query = f"INSERT INTO Review (Paper, Title) VALUES ('{st.session_state.p_id}', '{title}');"
    sql.execute(query)
    conn.commit()

    st.session_state.p_add_rev=False


def click_search_button(text):
    if text != "":
        st.session_state.search_btn = True
        st.session_state.add_click = False
        st.session_state.p_add_rev = False
    else:
        st.session_state.search_btn = False
    
    st.session_state.p_id="NULL"


text_input = st.text_input(
    "",
    placeholder="Search for Papers ...",
)
options = st.radio(
    "",
    ["Researcher", "Research Paper", "Year of Publication", "Conference"],
    horizontal=True,
)

if text_input!="":
    click_search_button(text_input,)


if st.session_state.logged_in:
    add_vertical_space(2)
    st.button("Add", on_click=add_click)
    add_vertical_space(2)

col1, col2, col3 = st.columns(3)

if st.session_state.search_btn:
    if "Researcher" in options:
        query = f"SELECT DISTINCT RP.ID, RP.Title, RP.CitationCount FROM ResearchPaper RP JOIN Authorship A ON RP.ID = A.Paper JOIN Researcher R ON A.Author = R.ID WHERE lower(R.Name) LIKE '%{text_input}%';"
        sql.execute(query)
        data = sql.fetchall()
        for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )
            else:
                with col3:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )

    if "Research Paper" in options:
        query = f"SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp WHERE LOWER(Title) LIKE '%{text_input}%';"
        sql.execute(query)
        data = sql.fetchall()
        for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )
            else:
                with col3:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2])
                    )

    if "Year of Publication" in options:
        query = f"SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp WHERE LOWER (PublicationDate) LIKE '%{text_input}%';"
        sql.execute(query)
        data = sql.fetchall()
        for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        args=(option[0], option[2]),
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        args=(option[0], option[2]),
                    )
            else:
                with col3:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        args=(option[0], option[2]),
                    )
    if "Conference" in options:
        query = f"SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp inner join Conference c ON rp.Conference = c.ID WHERE LOWER (c.Title) LIKE '%{text_input}%';"
        sql.execute(query)
        data = sql.fetchall()
        for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        key=option[0],
                        args=(option[0], option[2]),
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        key=option[0],
                        args=(option[0], option[2]),
                    )
            else:
                with col3:
                    st.button(
                        option[1],
                        on_click=butn_click,
                        key=option[0],
                        args=(option[0], option[2]),
                    )



if st.session_state.p_id != "NULL" and not st.session_state.add_click and not st.session_state.p_add_rev:
    query = f"SELECT rp.Title AS Papep_Title, (SELECT GROUP_CONCAT(DISTINCT r.Name SEPARATOR ', ') FROM Authorship a JOIN Researcher r ON a.Author = r.ID WHERE a.Paper = rp.ID) AS Authors, rp.PublicationDate AS Publication_Date, rp.CitationCount AS Citation_Count, (SELECT c.Title FROM Conference c WHERE c.ID = rp.Conference) AS Conference_Title, (SELECT GROUP_CONCAT(DISTINCT rv.Title SEPARATOR ', ') FROM Review rv WHERE rv.Paper = rp.ID) AS Review_Titles FROM ResearchPaper rp WHERE rp.ID = {st.session_state.p_id};"
    sql.execute(query)
    data = sql.fetchall()

    columns = [desc[0] for desc in sql.description]
    df = pd.DataFrame(data, columns=columns)
    st.table(df)

    col11, col12, x, x = st.columns(4, gap="small")
    if st.session_state.logged_in:
        with col11:
            st.button("Delete", on_click=p_del)
        with col12:
            st.button("Add Review", on_click=p_add_rev)

all_authors_dict = {}
sql.execute("select ID, Name from Researcher;")
data = sql.fetchall()
for i in data:
    all_authors_dict[i[0]] = i[1]
all_authors = []
for key, value in all_authors_dict.items():
    all_authors.append(key)

if st.session_state.add_click and not st.session_state.p_add_rev:
    ptitle = st.text_input("Title")
    pauth = st.multiselect("Authors", all_authors)

    st.button(
        "Done",
        on_click=p_done_add,
        args=(
            ptitle,
            pauth,
        ),
    )

if st.session_state.p_id != "NULL" and st.session_state.p_add_rev:
    rtitle = st.text_input("Review")
    st.button("Done", on_click=p_done_rev, args=(rtitle,))
