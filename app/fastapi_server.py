import uuid
from fastapi import FastAPI, HTTPException, Query
from typing import Dict
from icecream import ic
ic.configureOutput(includeContext=True)
from app.question_answer_pair import AnswerPair, SessionData, QASet
import uvicorn

app = FastAPI()

# A global dictionary:
#   Key: session_id (str)
#   Value: SessionData (which includes a "pairs" dict of questions -> AnswerPair)
sessions: Dict[str, SessionData] = {}

# A default set of questions that will be added when a new session is created.
DEFAULT_QUESTIONS = [
    "What is your name?",
    "What is your favorite color?",
    "What is the capital of France?"
]

@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Welcome to the QA Session API!"}

def init_session() -> SessionData:
    """
    Initialize a new session with a unique session ID and a set of default questions.

    This function generates a new session ID using UUID, creates an empty answer set for each
    default question, and stores the session data in the global sessions dictionary.

    Returns:
        SessionData: The initialized session data containing the session ID and the QA set.
    """
    session_id = str(uuid.uuid4())
    qa_set = {}
    for question in DEFAULT_QUESTIONS:
        qa_set[question] = AnswerPair(primary="", transformed="")
    session_data = SessionData(session_id=session_id, qa_set=QASet(qa_set=qa_set))
    sessions[session_id] = session_data
    return session_data

@app.get("/new_session", response_model=SessionData)
def create_new_session() -> SessionData:
    """
    Create a new session.

    This function initializes a new session and returns the session data.

    Returns:
        SessionData: The data for the newly created session.
    """
    session_data = init_session()
    return session_data

@app.get("/qa")
def get_questions(session_id: str = Query(..., description="The session ID")) -> SessionData:
    """
    Args:
        session_id (str): The session ID.

    Returns:
        SessionData: The session data containing questions and answers.

    If the session doesn't exist, it creates a new session with default questions and empty answers.
    """
    if session_id not in sessions:
        # Create a new session with default questions, but empty answers
        session_data = init_session()
    else:
        session_data = sessions[session_id]
    ic(session_data)
    return session_data

@app.post("/submit_answers")
def submit_answers(submission: SessionData):
    """
        Args:
            submission (SessionData): The submission data containing the session ID and QA set.

        Raises:
            HTTPException: If the session ID is not found in the sessions.

        Returns:
            QASet: The updated QA set for the session.
    """
    session_id = submission.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    qa_set : QASet = submission.qa_set
    for question, pair in qa_set.qa_set.items():
        pair.transformed = "result from llm transform call with data " + pair.primary
    sessions[session_id].qa_set = qa_set
    ic(sessions[session_id])

    return sessions[session_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.fastapi_server:app", host="127.0.0.1", port=8000, log_level="info")