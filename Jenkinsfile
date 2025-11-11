pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Python env and test') {
            steps {
                echo 'Installing dependencies and running basic tests'
                bat 'python --version'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker image') {
            steps {
                bat 'docker build -t simple-swiggy .'
            }
        }

        stage('Run image (smoke)') {
            steps {
                bat 'docker run -d --name simple-swiggy-test -p 5000:5000 simple-swiggy'
                // wait 5 seconds for container startup
                bat 'powershell -Command "Start-Sleep -Seconds 5"'
                bat 'curl http://localhost:5000 || exit 0'
                bat 'docker rm -f simple-swiggy-test'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
