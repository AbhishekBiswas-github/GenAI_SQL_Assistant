import streamlit as st
import schema as sch
import query as qry
from langchain_openai.chat_models import ChatOpenAI


st.set_page_config("SQL GENERATOR", layout='wide')
st.title("SQL GENERATOR USING OPENAI")

if "schema_status" not in st.session_state:
    st.session_state.schema_status = False
if "schema_validated" not in st.session_state:
    st.session_state.schema_validated = False
if "query_status" not in st.session_state:
    st.session_state.query_status = False
if 'intent' not in st.session_state:
    st.session_state.intent = False


st.session_state.chat_model = ChatOpenAI(model='gpt-4', seed=25, max_completion_tokens=50, temperature=0)


if not st.session_state.schema_status and not st.session_state.query_status:
    st.header("Define the Schema", divider='blue')
    col1, col2 = st.columns([1,1])
    with col1:
        sch.get_schema()
    with col2:
        if st.session_state.schema_validated:
            st.text_area("Validated Schema",
                    value=f"""Name of the table {st.session_state.table_name}\n\nBelow is the Column Schema\n{st.session_state.column_details}""", 
                    height=330,
                    disabled=True
                )
            if st.button("Proceed", type="primary"):
                st.session_state.schema_status = True

elif st.session_state.schema_status and not st.session_state.query_status:
    st.header("Business Query", divider="red")
    col1, col2 = st.columns([1,2])
    with col1:
        qry.get_query()
    with col2:
        if st.session_state.intent:
            st.text_input("Business Intent", value=st.session_state.intent['business_intent'], disabled=True)
            st.text_input("Metrix", value=st.session_state.intent['metrics'][0], disabled=True)
            st.text_input("Filters", value=st.session_state.intent['filters'], disabled=True)
            if st.button("Generate", type="primary"):
                st.session_state.query_status = True
            # st.write(st.session_state.intent)

elif st.session_state.query_status:
    st.header("Generated_SQL", divider='yellow')