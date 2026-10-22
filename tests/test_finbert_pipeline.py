"""estimate_sentiment with a TINY STAND-IN model, not FinBERT.

FinBERT (~438 MB) is not downloaded in tests. A ~1 MB randomly initialised BERT
from Hugging Face's test fixtures, given a 3-way head, checks only the code path
(tokenise -> sum logits -> softmax -> label). Its outputs are meaningless as
sentiment. Needs network access to the Hugging Face Hub.
"""

import pytest
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import finbert_utils as fu

TINY = "hf-internal-testing/tiny-random-BertForSequenceClassification"


@pytest.fixture(scope="module")
def tiny():
    torch.manual_seed(0)
    tok = AutoTokenizer.from_pretrained(TINY)
    model = AutoModelForSequenceClassification.from_pretrained(TINY, num_labels=3, ignore_mismatched_sizes=True)
    model.eval()
    return tok, model


def test_returns_python_float_and_known_label(tiny):
    tok, model = tiny
    prob, label = fu.estimate_sentiment(["stocks rally", "earnings beat estimates"], tok, model)
    assert isinstance(prob, float) and 1 / 3 <= prob <= 1.0
    assert label in fu.labels


def test_long_headline_is_truncated(tiny):
    tok, model = tiny
    prob, _ = fu.estimate_sentiment(["word " * 3000], tok, model)
    assert 0.0 <= prob <= 1.0


def test_no_news_is_neutral_without_loading_a_model(monkeypatch):
    monkeypatch.setattr(fu, "load_model", lambda *a: pytest.fail("must not load"))
    assert fu.estimate_sentiment([]) == (0.0, "neutral")


def test_import_does_not_load_finbert():
    # Regression: importing finbert_utils downloaded/loaded the 438 MB model at import time.
    import subprocess
    import sys

    from conftest import REPO

    code = "import sys, finbert_utils; print('transformers' in sys.modules, 'torch' in sys.modules)"
    out = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True, text=True, check=True)
    assert out.stdout.split() == ["False", "False"]
