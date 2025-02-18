from typing import Dict
from pydantic import BaseModel, model_serializer

class AnswerPair(BaseModel):
    """
    Represents a pair of answers (primary and secondary) for a given question.
    Primary is the main response, secondary can be supplemental info.
    """
    primary: str
    secondary: str

class QASet(BaseModel):
    """
    Represents a set of questions and answers for a given session.
    """
    qa_set: Dict[str, AnswerPair]

    @model_serializer
    def serialize(self):
        return {
            "qa_set": {
                question: {"primary": pair.primary, "secondary": pair.secondary}
                for question, pair in self.qa_set.items()
            }
        }

class SessionData(BaseModel):
    """
    Represents the data for a single session, which includes:
      - pairs: a dictionary mapping a question string to an AnswerPair
    """
    session_id: str
    qa_set: QASet

    @model_serializer
    def serialize(self):
        return {
            "session_id": self.session_id,
            "qa_set": self.qa_set.serialize()
        }