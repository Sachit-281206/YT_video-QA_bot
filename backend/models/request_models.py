from pydantic import BaseModel


class VideoRequest(BaseModel):
    youtube_url: str


class QuestionRequest(BaseModel):
    question: str
    video_id: str
    
class SummaryRequest(
    BaseModel
):
    video_id: str