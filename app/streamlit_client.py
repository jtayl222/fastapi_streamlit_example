import os
import streamlit as st
import requests
from app.question_answer_pair import AnswerPair, SessionData, QASet
from icecream import ic
ic.configureOutput(includeContext=True)

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def create_new_session():
    """
    Sends a GET request to the API to create a new session.

    This function sends a GET request to the endpoint specified by 
    `API_BASE_URL` with the path `/new_session`. If the request is 
    successful (status code 200), it processes the response JSON and 
    updates the Streamlit state. If the request fails, it displays an 
    error message in the Streamlit app.

    Returns:
        None
    """
    resp = requests.get(f"{API_BASE_URL}/new_session")
    if resp.status_code == 200:
        rest_json_to_st_state(resp)
    else:
        st.error(f"Failed to create a new session: {resp.text}")

def rest_json_to_st_state(resp):
    """
    Updates the Streamlit session state with data from a JSON response.

    Args:
        resp: The response object containing JSON data.

    Raises:
        KeyError: If a required key is missing in the response data.

    The function extracts session data from the JSON response, validates it,
    and updates the Streamlit session state with the session ID and QA set.
    If a required key is missing, an error message is displayed in Streamlit.
    """
    session_data = SessionData.model_validate(resp.json())
    try:
        st.session_state["session_id"] = session_data.session_id
        st.session_state["qa_set"] = session_data.qa_set
        ic(dict(st.session_state))
    except KeyError as e:
        st.error(f"Missing key in response data: {e}")

def answer_questions():
    """
    Handles the process of answering questions in a Streamlit app.

    This function sets up the "Answer Questions" page, retrieves the QA set from the session state,
    allows the user to input primary answers for each question, and submits the answers to an API
    endpoint for transformation.

    Returns:
        str: The next page to navigate to after submitting answers.
    """
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
    """
    Displays a Streamlit interface for reviewing and confirming answers.

    This function performs the following steps:
    1. Sets the title of the Streamlit app to "Review and Confirm Answers".
    2. Sends a GET request to the QA API to retrieve the QA set for the current session.
    3. If the request is successful, updates the Streamlit session state with the retrieved data.
    4. Checks if the QA set is loaded in the session state. If not, displays a warning message and exits.
    5. Displays the questions and their corresponding answers from the QA set.
    6. Provides a button to confirm all answers. If clicked, displays a success message.

    Note:
        - The function assumes that `API_BASE_URL` and `rest_json_to_st_state` are defined elsewhere in the code.
        - The function uses the `ic` function from the `icecream` library for debugging purposes.
        - The function relies on the `st` object from the Streamlit library for UI rendering.

    Returns:
        None
    """
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
    """
    Main function to render the Streamlit sidebar and handle page navigation.

    This function sets up the sidebar with a title and a selectbox for page navigation.
    It checks if a session ID exists in the session state and creates a new session if not.
    Depending on the selected page, it calls the appropriate function to render the page content.

    Pages:
    - "Answer Questions": Calls the answer_questions() function.
    - "Review and Confirm": Calls the review_and_confirm() function.
    """
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