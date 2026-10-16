# Vetrinia - Sentiment Analysis Service

Progetto DevOps semplice per pubblicare un modello di Sentiment Analysis attraverso una API REST.

## Tecnologie

- Python
- Flask
- Docker
- Jenkins
- Prometheus
- Grafana
- cAdvisor
- Pytest



## 1. Modello

Copia il file nella cartella principale del progetto.
Il servizio lo carica con pickle.

```text
sentiment_analysis_model.pkl
```


## 2. Avvio locale senza Docker

Creare un virtual environment:

```bash
python -m venv venv o  py -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

Avviare:

```bash
python app/app.py o py app/app.py
```

Il servizio sarà disponibile su:

```text
http://localhost:5000
```

## 3. Endpoint

### POST /predict

Richiesta:

```json
{
  "review": "This product is amazing! I love it."
}
```

Risposta possibile:

```json
{
  "sentiment": "positive",
  "confidence": 0.56
}
```

Nota: confidence viene restituito solo se il modello reale espone il metodo predict_proba.

### GET /metrics

```text
http://localhost:5000/metrics
```

Restituisce le metriche nel formato Prometheus.

### GET /health

```text
http://localhost:5000/health
```

## 4. Test

```bash
pytest -v
```

Sono presenti test unitari e un test di integrazione.

I test usano un modello finto per non dipendere dal file pickle reale.

## 5. Docker

Creare l'immagine:

```bash
docker build -t vetrinia-sentiment .
```

Avviare il container:

```bash
docker run -d --name vetrinia-sentiment-app -p 5000:5000 vetrinia-sentiment
```

## 6. Prometheus e Grafana

Avviare tutto:

```bash
docker compose up -d --build
```

Servizi:

```text
API         http://localhost:5000
Prometheus  http://localhost:9090
Grafana     http://localhost:3000
cAdvisor    http://localhost:8080
```

Credenziali iniziali Grafana normalmente:

```text
utente: admin
password: admin
```

Grafana chiederà di modificare la password al primo accesso.

La dashboard Vetrinia Sentiment Analysis viene caricata automaticamente.

## 7. Metriche

Sono monitorati:

- tempi di risposta /predict;
- errori di predizione;
- numero di predizioni;
- CPU del container;
- memoria del container.

Le metriche CPU e memoria arrivano da cAdvisor.

## 8. Jenkins

Il Jenkinsfile esegue:

1. checkout del repository;
2. installazione dipendenze;
3. test automatici;
4. build dell'immagine Docker;
5. deploy del nuovo container;
6. messaggio finale di successo o errore.

Il trigger pollSCM controlla periodicamente Git per nuove modifiche. In un repository GitHub reale è preferibile configurare anche un webhook GitHub -> Jenkins, così la pipeline parte immediatamente a ogni push.


## Scelta progettuale

La soluzione è un singolo servizio Flask in Docker, Prometheus per le metriche, Grafana per la dashboard e cAdvisor per CPU/memoria. 
