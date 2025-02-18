from typing import Dict
from pydantic import BaseModel, model_serializer

class AnswerPair(BaseModel):
    """
    Represents a pair of answers (primary and secondary) for a given question.
    Primary is the main response, secondary can be supplemental info.
    """
    primary: str
    secondary: str

    @model_serializer(mode="wrap")
    def _serialize(self, handler):
        d = handler(self)
        d['primary'] = self.primary
        d['secondary'] = self.secondary
        return d

class QASet(BaseModel):
    """
    Represents a set of questions and answers for a given session.
    """
    qa_set: Dict[str, AnswerPair]

    @model_serializer(mode="wrap")
    def _serialize(self, handler):
        d = handler(self)
        return {k: v for k, v in d['qa_set'].items()}

class SessionData(BaseModel):
    """
    Represents the data for a single session, which includes:
      - pairs: a dictionary mapping a question string to an AnswerPair
    """
    session_id: str
    qa_set: QASet