import pytest
from fastapi.testclient import TestClient
from app.fastapi_server import app, sessions, DEFAULT_QUESTIONS, init_session
from app.question_answer_pair import SessionData, QASet, AnswerPair

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the QA Session API!"}

def test_create_new_session():
    response = client.get("/new_session")
    assert response.status_code == 200
    session_data = response.json()
    assert "session_id" in session_data
    assert "qa_set" in session_data
    assert len(session_data["qa_set"]["qa_set"]) == len(DEFAULT_QUESTIONS)

def test_get_questions_new_session():
    response = client.get("/new_session")
    session_id = response.json()["session_id"]

    response = client.get(f"/qa?session_id={session_id}")
    assert response.status_code == 200
    session_data = response.json()
    assert session_data["session_id"] == session_id
    assert len(session_data["qa_set"]["qa_set"]) == len(DEFAULT_QUESTIONS)

def test_get_questions_nonexistent_session():
    response = client.get("/qa?session_id=nonexistent")
    assert response.status_code == 200
    session_data = response.json()
    assert "session_id" in session_data
    assert len(session_data["qa_set"]["qa_set"]) == len(DEFAULT_QUESTIONS)

def test_submit_answers():
    response = client.get("/new_session")
    session_id = response.json()["session_id"]

    qa_set = {question: AnswerPair(primary="test answer", transformed="") for question in DEFAULT_QUESTIONS}
    submission = SessionData(session_id=session_id, qa_set=QASet(qa_set=qa_set))

    response = client.post("/submit_answers", json=submission.model_dump())
    assert response.status_code == 200
    session_data = response.json()
    assert session_data["session_id"] == session_id
    for question, pair in session_data["qa_set"]["qa_set"].items():
        assert pair["primary"] == "test answer"
        assert pair["transformed"].startswith("result from llm transform call with data")

if __name__ == "__main__":
    pytest.main()