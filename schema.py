import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

if 'table_name' not in st.session_state:
    st.session_state.table_name = False

if 'column_details' not in st.session_state:
    st.session_state.column_details = False

def get_schema():
    get_table_name()
    get_column_names()
    get_optimization_info()
    validate_btn = st.button("Validate the schema", type='primary')
    if validate_btn:
        validate_status = validate_col_details()
        if (
            st.session_state.table_name and 
            st.session_state.column_details and 
            validate_status.content == 'Yes'
        ):
            st.session_state.schema_validated = True
            st.toast("✅ Schema Validated Successfully.")



def get_table_name():
    st.session_state.table_name = st.text_input("Table Information: ", placeholder="Enter the table name", value="Songs")

def get_column_names():
    st.session_state.column_details = st.text_area("Column Information: ", placeholder="""Enter as below format:
1. order_id (int)
2. order_date (date)
3. region (string)
4. revenue (float)""", value="""1. track_name (string)
2. artist(s)_name (string)
3. artist_count (int)
4. released_year (int)
5. released_month (int)
6. released_day (int)
7. in_spotify_playlists (int)
8. in_spotify_charts (int)
9. streams (int)
10. in_apple_playlists (int)
11. in_apple_charts (int)
12. in_deezer_playlists (int)
13. in_deezer_charts (int)
14. in_shazam_charts (int)
15. bpm (int)
16. key (string)
17. mode (string)
18. danceability_% (int)
19. valence_% (int)
20. energy_% (int)
21. acousticness_% (int)
22. instrumentalness_% (int)
23. liveness_% (int)
24. speechiness_% (int)
25. cover_url (stirng)""", height=250)

def get_optimization_info():
    st.session_state.optimize = st.text_input("SQL Optimization Instruction", placeholder="Enter instruction", value=None)

def validate_col_details():
   
    prompt = f"""Check the below column details entered by the user\n{st.session_state.column_details}\n is enetered in list pattern with column name and their datatype in parenthesis.\nReply only in one word (Yes or No)"""
    validate_response = st.session_state.chat_model.invoke([
        SystemMessage("You are a bot checking the column details entered by the user"),
        HumanMessage(content=prompt)
    ])
    return validate_response