"""FastAPI web server for textmood-lite."""

from fastapi import FastAPI
from pydantic import BaseModel

from textmood_lite.core import analyze, dominant_mood

app = FastAPI(
    title="textmood-lite",
    description="A tiny keyword-based mood detector for text",
    version="0.1.0",
)


class TextInput(BaseModel):
    text: str


class MoodResponse(BaseModel):
    text: str
    dominant_mood: str
    scores: dict[str, int]

    model_config = {"from_attributes": True}


@app.get("/")
def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "service": "textmood-lite"}


@app.post("/analyze", response_model=MoodResponse)
def analyze_post(input: TextInput) -> MoodResponse:
    """Analyze mood via POST request with JSON body."""
    return MoodResponse(
        text=input.text,
        dominant_mood=dominant_mood(input.text),
        scores=analyze(input.text),
    )


@app.get("/analyze", response_model=MoodResponse)
def analyze_get(text: str) -> MoodResponse:
    """Analyze mood via GET request with query parameter."""
    return MoodResponse(
        text=text,
        dominant_mood=dominant_mood(text),
        scores=analyze(text),
    )


# """FastAPI web server for textmood-lite"""

# from fastapi import FastAPI
# from pydantic import BaseModel
# from textmood_lite.core import analyze, dominant_mood

# app = FastAPI(
#     title="textmood-lite",
#     description="A tiny keyword-based mood detector for text",
#     version="0.1.0",
# )


# class TextInput(BaseModel):
#     text: str


# class MoodResponses(BaseModel):
#     text: str
#     dominant_mood: str
#     scores: dict[str, int]

#     model_config = {"from_attributes": True}


# @app.get("/")
# def root():
#     """Health check endpoint."""
#     return {"status": "ok", "service": "textmood-lite"}


# @app.get("/analyze", response_model=MoodResponses)
# def analyze_get(text: str) -> MoodResponses:
#     """Analyze mood via GET request with query parameter."""
#     return MoodResponses(
#         text=text,
#         dominant_mood=dominant_mood(text),
#         scores=analyze(text),
#     )


# @app.get("/analyze")
# def analyze_get(text: str):
#     """Analyze mood via GET request with query parameter."""
#     return MoodResponses(
#         text=text,
#         dominant_mood=dominant_mood(text),
#         score=analyze(text),
#     )
