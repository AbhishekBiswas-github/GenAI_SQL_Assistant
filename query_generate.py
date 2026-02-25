import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage
import json
from streamlit_js_eval import streamlit_js_eval
import time

def generate_query():
    st.write("")
    prompt = f"""You are a SQL Expert.

    Schema:
    Name of the table\n{st.session_state.table_name}\n\nBelow is the Column Schema\n{st.session_state.column_details}

    Business Intent: 
    {st.session_state.intent['business_intent']}
    
    Metrics:
    {st.session_state.intent['metrics']}
    
    Filters: 
    {st.session_state.intent['filters']}

    Rules:
    - Use SELECT only
    - No DELETE / UPDATE / DROP
    - Use explicit column names

"""
    systemPrompt = """
Generate an optimised SQL query.
        Return the output STRICTLY in this JSON format ONLY:

        {
            "code": "<SQL QUERY HERE>",
            "explanation": "<DETAILED EXPLANATION>"
        }

        DO NOT return any text outside of the JSON.
        DO NOT include markdown.
        DO NOT include backticks.

"""

    with st.spinner("Generating Query...."):
        query_generated = st.session_state.chat_model.invoke([
            SystemMessage(content=systemPrompt),
            HumanMessage(content=prompt)
        ])

        response = json.loads(query_generated.content)
        st.code(response["code"], language="SQL")
        st.subheader("Explanation")
        st.info(f"""{response['explanation']}""")
        st.toast("✅ SQL Query Generated Successfully.")



    if st.button("Reset Everything....", type="secondary", key="reset_btn"):
        st.session_state["do_reload"] = True

    # Execute JS reload only ONCE
    if st.session_state.get("do_reload", False):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
        st.session_state["do_reload"] = False



    