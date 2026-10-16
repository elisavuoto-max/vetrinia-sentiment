pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vetrinia-sentiment'
        CONTAINER_NAME = 'vetrinia-sentiment-app'
       URL_PYTHON = 'C:\\Users\\vuotoe\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
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
                bat '"%URL_PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Tests') {
            steps {
                bat '"%URL_PYTHON%" -m pytest -v'
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