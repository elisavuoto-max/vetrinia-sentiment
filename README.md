# Vetrinia - Sentiment Analysis Service

Questo progetto nasce con l'obiettivo di classificare rapidamente una recensione come positiva, negativa o neutra attraverso una semplice API REST, utilizzando le predizioni di un modello di **Sentiment Analysis** già addestrato su testi in lingua inglese.

L'idea è quella di simulare un piccolo flusso DevOps completo: 
-	il codice viene versionato su GitHub, 
-	Jenkins esegue automaticamente test, build e deploy, 
-	Prometheus e Grafana permettono di monitorare il comportamento dell'applicazione e dei container.



## 1. Tecnologie utilizzate

Il progetto utilizza:

- **Python** e **Flask** per realizzare il servizio REST che espone il modello di Sentiment Analysis.  
- **Pytest** per eseguire i test automatici.  
- **Docker** permette di creare un'immagine dell'applicazione e di eseguirla in modo isolato.  
- **Docker Compose** per avviare insieme l'applicazione, Prometheus, Grafana e cAdvisor.  
- **Jenkins** gestisce la pipeline CI/CD.  
- **Prometheus** raccoglie le metriche dell'applicazione e dei container, 
- **Grafana** permette di visualizzare le metriche tramite dashboard.  
- **Git e GitHub** vengono utilizzati per il versionamento del progetto.



## 2. Modello di Sentiment Analysis

Il modello è reperibile nell'url https://github.com/Profession-AI/progetti-devops/blob/main/Deploy%20e%20monitoraggio%20di%20un%20modello%20di%20sentiment%20analysis%20per%20recensioni/sentiment_analysis_model.pkl

Il file è presente nella cartella principale del progetto con il nome:

sentiment_analysis_model.pkl

All'avvio dell'applicazione Flask, il modello viene caricato tramite il modulo pickle di Python e viene poi utilizzato per effettuare le previsioni sulle recensioni ricevute tramite API.


## 3. Avvio locale senza Docker

L'applicazione può essere eseguita anche senza Docker, direttamente tramite Python.
Eseguendo i seguenti comandi per Windows:

```
python -m venv venv
```

oppure:

```bash
py -m venv venv
```

Successivamente l'ambiente può essere attivato con:

```
venv\Scripts\activate
```


Una volta attivato l'ambiente virtuale, si installano tutte le dipendenze definite nel file requirements.txt:

```
pip install -r requirements.txt
```

A questo punto l'applicazione può essere avviata con:

```
python app/app.py
```

oppure:

```
py app/app.py
```

Il servizio sarà disponibile all'indirizzo: http://localhost:5000


## 4. Endpoint REST

Il servizio Flask espone tre endpoint principali.

### POST /predict

L'endpoint /predict viene utilizzato per inviare una recensione al modello e ricevere il sentimento previsto.
Esempio di richiesta json:

```
{
  "review": "This product is amazing! I love it."
}
```

Una possibile risposta è:

```
{
	"confidence": 0.56,
	"sentiment": "positive"
  
}
```

Il campo sentiment contiene il risultato della classificazione, mentre confidence viene restituita la probabilità. 


### GET /health

L'endpoint /health serve per verificare velocemente che il servizio sia in esecuzione.
È disponibile all'indirizzo: http://localhost:5000/health


### GET /metrics

L'endpoint /metrics espone le metriche dell'applicazione in un formato compatibile con Prometheus.
È disponibile all'indirizzo: http://localhost:5000/metrics
Prometheus utilizza questo endpoint per raccogliere periodicamente informazioni sul funzionamento del servizio.

---

## 5. Test automatici

Il progetto contiene test automatici eseguiti tramite Pytest.
Per eseguire tutti i test manualmente è possibile utilizzare:

```
pytest -v
```

oppure:

```
python -m pytest -v
```

Sono presenti test unitari e test di integrazione che verificano sia il comportamento dell'API sia il corretto utilizzo del modello.
Durante i test viene utilizzato anche un modello finto. Questa scelta permette di verificare il funzionamento dell'applicazione senza dover dipendere sempre dal file pickle reale e rende i test più semplici e ripetibili.
Gli stessi test vengono eseguiti automaticamente da Jenkins durante la pipeline.


## 6. Docker

L'applicazione può essere eseguita all'interno di un container Docker.
Per creare l'immagine:

```
docker build -t vetrinia-sentiment .
```

Una volta completata la build, è possibile avviare il container con:

```
docker run -d --name vetrinia-sentiment-app -p 5000:5000 vetrinia-sentiment
```

Il servizio sarà raggiungibile su: http://localhost:5000

## 7. Docker Compose

Per evitare di avviare manualmente ogni singolo componente, il progetto utilizza Docker Compose.
Con un unico comando è possibile avviare l'applicazione Flask insieme a Prometheus, Grafana e cAdvisor:

```
docker compose up -d --build
```

Dopo l'avvio, i servizi principali sono disponibili ai seguenti indirizzi:

```
API         http://localhost:5000
Prometheus  http://localhost:9090
Grafana     http://localhost:3000
cAdvisor    http://localhost:8081
```

Per verificare quali container sono attivi:

```
docker ps
```

Per fermare e rimuovere i container creati da Docker Compose:

```
docker compose down
```

Se invece si desidera soltanto fermarli senza rimuoverli:

```
docker compose stop
```

e successivamente possono essere riavviati con:

```
docker compose start
```


## 8. cAdvisor

cAdvisor viene utilizzato per raccogliere informazioni relative all'utilizzo delle risorse da parte dei container come utilizzo della CPU, memoria, rete, filesystem e stato dei container.
È disponibile all'indirizzo: http://localhost:8080
Queste metriche vengono poi raccolte da Prometheus e possono essere utilizzate nelle dashboard Grafana.


## 9. Prometheus 

Prometheus viene utilizzato per raccogliere le metriche dell'applicazione.
Il servizio Flask espone le proprie metriche tramite /metrics.
L'interfaccia di Prometheus è disponibile su: http://localhost:9090
Per verificare che Prometheus riesca realmente a comunicare con i servizi configurati è possibile aprire:http://localhost:9090/targets
ITra le informazioni monitorate ci sono i tempi di risposta delle richieste, il numero di predizioni effettuate e gli eventuali errori di predizione. Grazie a cAdvisor raccoglie i dati relativi all'utilizzo dei container.


## 10. Grafana

Grafana viene utilizzato per visualizzare in modo grafico i dati raccolti da Prometheus.
L'interfaccia è disponibile su: http://localhost:3000
Al primo accesso le credenziali normalmente utilizzate sono:

```
utente: admin
password: admin
```

Grafana può chiedere di modificare la password al primo accesso.
Grafana comunica con Prometheus attraverso il datasource: http://prometheus:9090
Viene utilizzato il nome prometheus perché i due servizi si trovano all'interno della stessa rete Docker. Per questo motivo non viene utilizzato localhost.



## 11. GitHub

Il progetto è versionato con Git e pubblicato su GitHub, al momento con vibilità pubblica, all'indirizzo:
https://github.com/elisavuoto-max/vetrinia-sentiment.git
Il branch principale è main
Il normale flusso di lavoro per pubblicare una modifica è:

```
git add .
git commit -m "Descrizione della modifica"
git push
```

Dopo il push, Jenkins può rilevare la nuova versione e avviare automaticamente la pipeline.

## 12. Jenkins e pipeline CI/CD

Jenkins viene utilizzato per automatizzare il processo che porta una modifica dal repository GitHub fino al deploy.
La pipeline è definita nel file **Jenkinsfile** presente nella cartella principale del progetto e segue il seguente flusso:
Checkout repository -> Installazione dipendenze -> Test automatici -> Docker build -> Deploy
Cioè viene scaricato il codice dal repository GitHub, installate le dipendenze Python ed eseguiti i test automatici, se i test terminano correttamente viene creata l'immagine Docker, infine l'immagine viene utilizzata per eseguire il servizio.
La pipeline è stata testata utilizzando Jenkins installato su Windows. Per questo motivo nel Jenkinsfile vengono utilizzati comandi di tipo:
```
bat 'comando'
```

Su un agente Jenkins Linux, gli stessi comandi devono essere adattati utilizzando sh invece di bat.

Il job Jenkins è configurato come una Pipeline, (Pipeline script from SCM) e Jenkins legge il Jenkinsfile direttamente dal repository.


### Avvio automatico della pipeline

Nel progetto viene utilizzato pollSCM per permettere a Jenkins di controllare periodicamente il repository:

```
triggers {
    pollSCM('* * * * *')
}
```

In questo modo Jenkins verifica se sono presenti nuovi commit.


### Notifiche della pipeline

Il Jenkinsfile contiene anche una sezione post, utilizzata per gestire il risultato finale della pipeline.


```
post {
    success {
        echo 'Pipeline completata con successo.'
    }

    failure {
        echo 'Pipeline fallita.'
    }
}
```

In questo modo il log Jenkins mostra chiaramente se l'esecuzione è terminata correttamente oppure se uno degli stage ha generato un errore. 


### Python e Docker sulla macchina Jenkins

La macchina che esegue Jenkins deve avere a disposizione gli strumenti utilizzati dalla pipeline, in particolare deve essere installato:
- Python e deve essere disponibile nel PATH.
- Docker ed essere disponibile da riga di comando.



## 13. Architettura generale

Dal punto di vista applicativo, il funzionamento può essere rappresentato così:
Il client invia una recensione all'API. Flask riceve il testo, lo passa al modello e restituisce il risultato della previsione.
La parte DevOps segue invece il flusso:

GitHub -> Jenkins -> Test, Docker Build, Deploy

In questo modo il codice viene controllato automaticamente prima di essere distribuito.
La parte di osservabilità è invece composta da Prometheus, Grafana e cAdvisor:

Flask /metrics -> cAdvisor -> Prometheus  -> Grafana



