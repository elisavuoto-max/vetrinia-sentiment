import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.app import app
from tests.fake_model import FakeSentimentModel


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_predict_positive():
    client = app.test_client()
    with patch("app.app.get_model", return_value=FakeSentimentModel()):
        response = client.post("/predict", json={"review": "This product is amazing! I love it."})
    assert response.status_code == 200
    assert response.get_json()["sentiment"] == "positive"


def test_predict_negative():
    client = app.test_client()
    with patch("app.app.get_model", return_value=FakeSentimentModel()):
        response = client.post("/predict", json={"review": "This product is terrible and bad."})
    assert response.status_code == 200
    assert response.get_json()["sentiment"] == "negative"


def test_predict_neutral():
    client = app.test_client()
    with patch("app.app.get_model", return_value=FakeSentimentModel()):
        response = client.post("/predict", json={"review": "The package arrived yesterday."})
    assert response.status_code == 200
    assert response.get_json()["sentiment"] == "neutral"


def test_missing_review():
    client = app.test_client()
    response = client.post("/predict", json={})
    assert response.status_code == 400
