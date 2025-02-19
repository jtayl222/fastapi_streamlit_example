from pprint import pprint

import streamlit as st
import requests
from question_answer_pair import AnswerPair, SessionData, QASet
from typing import Dict
from icecream import ic
ic.configureOutput(includeContext=True)

API_BASE_URL = "http://127.0.0.1:8000"  # Adjust if your FastAPI runs elsewhere

def create_new_session():
    resp = requests.get(f"{API_BASE_URL}/new_session")
    if resp.status_code == 200:
        rest_json_to_st_state(resp)
    else:
        st.error(f"Failed to create a new session: {resp.text}")

def rest_json_to_st_state(resp):
    session_data = SessionData.model_validate(resp.json())
    try:
        st.session_state["session_id"] = session_data.session_id
        st.session_state["qa_set"] = session_data.qa_set
        ic(dict(st.session_state))
    except KeyError as e:
        st.error(f"Missing key in response data: {e}")

def answer_questions():
    next_page = "Answer Questions"
    st.title("Answer Questions")

    if "session_id" not in st.session_state:
        create_new_session()

    if "qa_set" not in st.session_state:
        st.error("QA set not found in session state.")
        return

    qa_set: QASet = st.session_state["qa_set"]
    ic(qa_set)

    for question, ap in qa_set.qa_set.items():
        primary_ans = st.text_input(
            f"Primary answer ({question})",
            value=ap.primary
        )
        qa_set.qa_set[question] = AnswerPair(primary=primary_ans, transformed=ap.transformed)

    ic(qa_set)
    st.session_state["qa_set"] = qa_set
    ic(dict(st.session_state))

    if st.button("Submit and Transform Answers"):
        session_data = SessionData(session_id=st.session_state["session_id"], qa_set=qa_set)
        resp = requests.post(f"{API_BASE_URL}/submit_answers", json=session_data.model_dump())
        if resp.status_code == 200:
            rest_json_to_st_state(resp)
            st.success("Answers submitted successfully!")
            next_page = "Review and Confirm"
        else:
            st.error(f"Failed to submit answers: {resp.text}")

    return next_page

def review_and_confirm():
    st.title("Review and Confirm Answers")

    resp = requests.get(f"{API_BASE_URL}/qa", params={"session_id": st.session_state["session_id"]})
    if resp.status_code == 200:
        rest_json_to_st_state(resp)

    if "qa_set" not in st.session_state:
        st.warning("No questions loaded. Please go to the 'Answer Questions' page to load and answer questions.")
        return

    qa_set: QASet = st.session_state["qa_set"]
    ic(qa_set)

    st.subheader("Review your answers")

    for question, answer_pair in qa_set.qa_set.items():
        st.write(f"**Question:** {question}")
        st.write(f"**Primary Answer:** {answer_pair.primary}")
        st.write(f"**Transformed Data:** {answer_pair.transformed}")
        st.write("---")

    if st.button("Confirm All Answers"):
        st.success("All answers confirmed!")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select a page", ["Answer Questions", "Review and Confirm"])

    if "session_id" not in st.session_state:
        create_new_session()

    if page == "Answer Questions":
        page = answer_questions()
    elif page == "Review and Confirm":
        review_and_confirm()

if __name__ == "__main__":
    main()