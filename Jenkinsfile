pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vetrinia-sentiment'
        CONTAINER_NAME = 'vetrinia-sentiment-app'
    }

    triggers {
        pollSCM('* * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                sh 'python -m pytest -v'
            }
        }

        stage('Docker build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:${BUILD_NUMBER} .'
                sh 'docker tag $IMAGE_NAME:${BUILD_NUMBER} $IMAGE_NAME:latest'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker rm -f $CONTAINER_NAME || true'
                sh 'docker run -d --name $CONTAINER_NAME -p 5000:5000 $IMAGE_NAME:latest'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completata con successo.'
            // Esempio con plugin Email Extension:
            // emailext subject: 'SUCCESS - Scholar Sentiment', body: 'Deploy completato', to: 'team@example.com'
        }
        failure {
            echo 'Pipeline fallita.'
            // emailext subject: 'FAILED - Scholar Sentiment', body: 'Controllare Jenkins', to: 'team@example.com'
        }
    }
}
