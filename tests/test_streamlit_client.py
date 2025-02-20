import pytest
import streamlit as st
from streamlit.testing import StreamlitTestCase
from unittest.mock import patch, MagicMock
from app.streamlit_client import create_new_session, answer_questions, review_and_confirm, main

class TestStreamlitClient(StreamlitTestCase):

    @patch("app.streamlit_client.requests.get")
    def test_create_new_session(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "session_id": "test_session_id",
            "qa_set": {"qa_set": {}}
        }
        mock_get.return_value = mock_response

        create_new_session()
        self.assertEqual(st.session_state["session_id"], "test_session_id")
        self.assertIn("qa_set", st.session_state)

    @patch("app.streamlit_client.requests.post")
    @patch("app.streamlit_client.st.text_input")
    @patch("app.streamlit_client.st.button")
    def test_answer_questions(self, mock_button, mock_text_input, mock_post):
        st.session_state["session_id"] = "test_session_id"
        st.session_state["qa_set"] = {"qa_set": {"Question 1": {"primary": "Answer 1", "transformed": ""}}}

        mock_text_input.return_value = "Updated Answer 1"
        mock_button.return_value = True

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "session_id": "test_session_id",
            "qa_set": {"qa_set": {"Question 1": {"primary": "Updated Answer 1", "transformed": "Transformed Answer 1"}}}
        }
        mock_post.return_value = mock_response

        next_page = answer_questions()
        self.assertEqual(next_page, "Review and Confirm")
        self.assertEqual(st.session_state["qa_set"]["qa_set"]["Question 1"]["primary"], "Updated Answer 1")
        self.assertEqual(st.session_state["qa_set"]["qa_set"]["Question 1"]["transformed"], "Transformed Answer 1")

    @patch("app.streamlit_client.requests.get")
    def test_review_and_confirm(self, mock_get):
        st.session_state["session_id"] = "test_session_id"
        st.session_state["qa_set"] = {"qa_set": {"Question 1": {"primary": "Answer 1", "transformed": "Transformed Answer 1"}}}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "session_id": "test_session_id",
            "qa_set": {"qa_set": {"Question 1": {"primary": "Answer 1", "transformed": "Transformed Answer 1"}}}
        }
        mock_get.return_value = mock_response

        review_and_confirm()
        self.assertIn("qa_set", st.session_state)
        self.assertEqual(st.session_state["qa_set"]["qa_set"]["Question 1"]["primary"], "Answer 1")
        self.assertEqual(st.session_state["qa_set"]["qa_set"]["Question 1"]["transformed"], "Transformed Answer 1")

    @patch("app.streamlit_client.create_new_session")
    @patch("app.streamlit_client.st.sidebar.selectbox")
    def test_main(self, mock_selectbox, mock_create_new_session):
        mock_selectbox.return_value = "Answer Questions"
        main()
        mock_create_new_session.assert_called_once()

if __name__ == "__main__":
    pytest.main()