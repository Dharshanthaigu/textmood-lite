"""Core mood-detection logic for textmood-lite"""

import re

_LEXICON={
    "happy": {"happy", "joy", "great", "excited", "love", "wonderful", "glad"},
    "sad": {"sad", "down", "unhappy", "depressed", "cry", "miserable", "lonely"},
    "angry": {"angry", "mad", "furious", "annoyed", "hate", "rage"},
    "anxious": {"worried", "nervous", "anxious", "scared", "afraid", "stressed"},
}

def _tokenize(text:str) -> list[str]:
    return re.findall(r"[a-zA-Z']+", text.lower())

def analyze (text:str) -> dict[str,int]:
    """Return a score for each moodf found in the text"""
    tokens = _tokenize(text)
    scores = {mood : 0 for mood in _LEXICON}
    for token in tokens:
        for mood , words in _LEXICON.items():
            if token in words:
                scores[mood] +=1
    return scores

def dominant_mood(text: str)-> str:
    """Return the single mood with the highest score , or 'neutral'."""
    scores = analyze(text)
    if not any(scores.values()):
        return "neutral"
    return max(scores,key=scores.get)

