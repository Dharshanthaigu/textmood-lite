from textmood_lite.core import dominant_mood


def test_happy_text():
    assert dominant_mood("I am so happy and excited today") == "happy"


def test_empty_text():
    assert dominant_mood("") == "neutral"


def test_no_keywords():
    assert dominant_mood("The sky is blue") == "neutral"
