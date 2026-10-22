"""FinBERT sentiment for a list of news headlines.

The model (ProsusAI/finbert, ~438 MB) is loaded lazily on first use, not at import.
"""

from __future__ import annotations

from functools import lru_cache

MODEL_NAME = "ProsusAI/finbert"
# ProsusAI/finbert's label order (config.id2label): 0 positive, 1 negative, 2 neutral.
labels = ["positive", "negative", "neutral"]


@lru_cache(maxsize=1)
def load_model(model_name: str = MODEL_NAME):
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    model.eval()
    return tokenizer, model, device


def estimate_sentiment(news: list[str], tokenizer=None, model=None) -> tuple[float, str]:
    """Return ``(probability, label)`` for the combined headlines.

    Logits of all headlines are summed before the softmax, so the result is one
    aggregate sentiment. No headlines -> ``(0.0, "neutral")``.
    """
    if not news:
        return 0.0, labels[-1]

    import torch

    if tokenizer is None or model is None:
        tokenizer, model, _ = load_model()
    device = next(model.parameters()).device

    tokens = tokenizer(news, return_tensors="pt", padding=True, truncation=True, max_length=512).to(device)
    with torch.no_grad():
        logits = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])["logits"]
    result = torch.nn.functional.softmax(torch.sum(logits, 0), dim=-1)
    idx = int(torch.argmax(result))
    return float(result[idx]), labels[idx]


if __name__ == "__main__":
    probability, sentiment = estimate_sentiment(
        ["markets responded negatively to the news!", "traders were displeased!"]
    )
    print(f"{probability:.4f} {sentiment}")
