import os
import pickle
import time
from typing import Any
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

MODEL_PATH = os.getenv("MODEL_PATH", "sentiment_analysis_model.pkl")

REQUEST_TIME = Histogram(
    "sentiment_request_duration_seconds",
    "Tempo impiegato dalle richieste /predict",
)

PREDICTION_ERRORS = Counter(
    "sentiment_prediction_errors_total",
    "Numero di errori durante la predizione",
)

PREDICTIONS = Counter(
    "sentiment_predictions_total",
    "Numero totale di predizioni",
    ["sentiment"],
)


def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


model = None


def get_model():
    global model
    if model is None:
        model = load_model()
    return model


def calcola_confidenza(pipeline, review):
    # Se il modello supporta predict_proba prendiamo la probabilità più alta.
    # Altrimenti restituiamo None, perché non tutti i modelli espongono una confidence.
    if hasattr(pipeline, "predict_proba"):
        probabilities = pipeline.predict_proba([review])[0]
        return round(float(max(probabilities)), 4)
    return None


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    start_time = time.time()

    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({"error": "Il corpo della richiesta deve essere un JSON valido"}), 400

        review = data.get("review")

        if not isinstance(review, str) or not review.strip():
            return jsonify({"error": "Il campo 'review' è obbligatorio"}), 400


        pipeline = get_model()

        prediction = pipeline.predict([review])
        sentiment = str(prediction[0])
        confidence = calcola_confidenza(pipeline, review)

        PREDICTIONS.labels(sentiment=sentiment).inc()

        response: dict[str, Any] = {"sentiment": sentiment}

        if confidence is not None:
            response["confidence"] = confidence

        return jsonify(response)

    except Exception as exc:
        PREDICTION_ERRORS.inc()
        return jsonify({"error": "Errore durante la predizione", "details": str(exc)}), 500

    finally:
        REQUEST_TIME.observe(time.time() - start_time)


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
