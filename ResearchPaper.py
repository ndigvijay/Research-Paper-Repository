import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.add_vertical_space import add_vertical_space
from MySQL_Connection import *
# from init import init

# st.sidebar.write(st.session_state)

# init()
conn=connect_to_mysql()
sql = conn.cursor()

st.title("List of all Papers")

add_state("search_btn")
add_state("logged_in")
add_state("p_add_rev")
add_state("p_add_click")

if "p_id" not in st.session_state:
    st.session_state.p_id = "NULL"


def butn_click(id, count):
    st.session_state.p_id = id
    count += 1
    query = f"UPDATE ResearchPaper SET CitationCount = '{count}' WHERE ID = {id};"
    sql.execute(query)
    conn.commit()
    st.session_state.p_add_click=False
    st.session_state.p_add_rev=False


def p_add_click():
    st.session_state.p_add_click = True
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

# trigger
def p_delete():
    query = f"DELETE FROM ResearchPaper WHERE ID = {st.session_state.p_id};"
    sql.execute(query)
    conn.commit()

    trigger_query = """
    CREATE TRIGGER IF NOT EXISTS DeleteRelatedRecords
    AFTER DELETE ON ResearchPaper
    BEGIN
        DELETE FROM Review WHERE Paper = OLD.ID;
        DELETE FROM Authorship WHERE Paper = OLD.ID;
    END;
    """
    sql.executescript(trigger_query)
    conn.commit()

def p_add_rev():
    st.session_state.p_add_rev = True

# procedure
def p_add():
    query="""DELIMITER //
    CREATE PROCEDURE AddAuthorship(IN paper_id INT, IN author_id INT)
    BEGIN
    INSERT INTO Authorship (Paper, Author) VALUES (paper_id, author_id);
    END //
    DELIMITER ;"""
    sql.execute(query)
    conn.commit()


# function
def get_count():
    query="""DELIMITER //
            CREATE FUNCTION GetTotalCitationCountByResearcher(researcher_id INT) RETURNS INT
            BEGIN
                DECLARE total_citation_count INT;
                SELECT SUM(CitationCount) INTO total_citation_count
                FROM ResearchPaper
                WHERE ID IN (SELECT Paper FROM Authorship WHERE Author = researcher_id);
                RETURN total_citation_count;
            END;
            //
            DELIMITER ;"""
    sql.execute(query)
    conn.commit()


def p_done_add(title, date, authors):
    if title=="" or date=="" or len(authors)==0:
        return
    query = f"INSERT INTO ResearchPaper (Title, PublicationDate, CitationCount) VALUES ('{title}', '{date}', 0);"
    sql.execute(query)
    conn.commit()
    query = f"SELECT ID FROM ResearchPaper WHERE Title = '{title}' AND PublicationDate = '{date}';"
    sql.execute(query)
    data = sql.fetchall()
    for author in authors:
        author=author.split("-")
        query = f"INSERT INTO Authorship (Paper, Author) VALUES ('{data[0][0]}', '{author[0]}');"
        sql.execute(query)
        conn.commit()

    st.session_state.p_add_click=False


def p_done_rev(title):
    if title=="":
        return
    query = f"INSERT INTO Review (Paper, Title) VALUES ('{st.session_state.p_id}', '{title}');"
    sql.execute(query)
    conn.commit()

    st.session_state.p_add_rev=False


def click_search_button(text):
    if text != "":
        st.session_state.search_btn = True
        st.session_state.p_add_click = False
        st.session_state.p_add_rev = False
    else:
        st.session_state.search_btn = False
    
    st.session_state.p_id="NULL"


text_input = st.text_input(
    "",
    placeholder="Search for Papers ...",
)
# options = st.radio(
#     "",
#     ["Researcher", "Research Paper", "Year of Publication", "Conference"],
#     horizontal=True,
# )

if text_input!="":
    click_search_button(text_input,)


if st.session_state.logged_in:
    st.button("Add", on_click=p_add_click,use_container_width=True)

col1, col2, col3 = st.columns(3)

if not st.session_state.search_btn:
    query=f"SELECT ID, Title, CitationCount FROM ResearchPaper ORDER BY PublicationDate DESC LIMIT 9;"
    sql.execute(query)
    data=sql.fetchall()
    for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )
            else:
                with col3:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )

if st.session_state.search_btn:
        query = f"SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp WHERE LOWER(Title) LIKE '%{text_input}%' UNION SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp WHERE LOWER(PublicationDate) LIKE '%{text_input}%' UNION SELECT rp.ID, rp.Title, rp.CitationCount FROM ResearchPaper rp INNER JOIN Conference c ON rp.Conference = c.ID WHERE LOWER(c.Title) LIKE '%{text_input}%' UNION SELECT RP.ID, RP.Title, RP.CitationCount FROM ResearchPaper RP JOIN Authorship A ON RP.ID = A.Paper JOIN Researcher R ON A.Author = R.ID WHERE LOWER(R.Name) LIKE '%{text_input}%';"
        sql.execute(query)
        data = sql.fetchall()
        for i, option in enumerate(data):
            if i % 3 == 0:
                with col1:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )
            elif i % 3 == 1:
                with col2:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )
            else:
                with col3:
                    st.button(
                        option[1], on_click=butn_click, args=(option[0], option[2]),use_container_width=True
                    )




if st.session_state.p_id != "NULL" and not st.session_state.p_add_click and not st.session_state.p_add_rev:
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
    all_authors.append(str(key)+"-"+value)

if st.session_state.p_add_click and not st.session_state.p_add_rev:
    ptitle = st.text_input("Title")
    pdate = st.date_input("publication Date")
    pauth = st.multiselect("Authors", all_authors)

    st.button(
        "Done",
        on_click=p_done_add,
        args=(
            ptitle,
            pdate,
            pauth,
        ),
    )

if st.session_state.p_id != "NULL" and st.session_state.p_add_rev:
    rtitle = st.text_input("Review")
    st.button("Done", on_click=p_done_rev, args=(rtitle,))
