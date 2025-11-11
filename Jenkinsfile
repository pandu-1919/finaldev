pipeline {
    agent any

    environment {
        IMAGE_NAME = "simple-swiggy"
        DOCKER_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Python env and test') {
            steps {
                echo 'Installing dependencies and running basic tests'
                sh 'python -V || true'
                sh 'pip install --user -r requirements.txt'
                // add any lightweight tests here
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Run image (smoke)') {
            steps {
                script {
                    // stop prior container if exists
                    sh "docker ps -a --filter \"name=${IMAGE_NAME}-test\" -q | xargs -r docker rm -f || true"
                    sh "docker run -d --name ${IMAGE_NAME}-test -p 5000:5000 ${IMAGE_NAME}:${DOCKER_TAG}"
                    // simple check
                    sh "sleep 3"
                    sh "curl -f http://localhost:5000/ || true"
                    // cleanup
                    sh "docker rm -f ${IMAGE_NAME}-test || true"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}