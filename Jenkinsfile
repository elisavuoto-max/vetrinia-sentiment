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
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Docker build') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% .'
                bat 'docker tag %IMAGE_NAME%:%BUILD_NUMBER% %IMAGE_NAME%:latest'
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                docker rm -f %CONTAINER_NAME% 2>nul || echo Container precedente non presente
                 docker compose up -d --build
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completata con successo.'
        }

        failure {
            echo 'Pipeline fallita.'
        }
    }
}