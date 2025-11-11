pipeline {
    agent any

    environment {
        IMAGE_NAME = "simple-swiggy"
        CONTAINER_NAME = "simple-swiggy-test"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Fetching code from GitHub...'
                checkout scm
            }
        }

        stage('Build Python env and test') {
            steps {
                echo 'Installing dependencies and verifying Python setup...'
                bat 'python --version'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Build Docker image') {
            steps {
                echo 'Building Docker image...'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Run container (deploy)') {
            steps {
                echo 'Running container...'
                // 🔹 Remove old container if it exists
                bat "docker rm -f %CONTAINER_NAME% || exit 0"
                
                // 🔹 Run new container (detached mode)
                bat "docker run -d --name %CONTAINER_NAME% -p 5000:5000 %IMAGE_NAME%"
                
                // 🔹 Wait a few seconds for Flask to start
                bat 'powershell -Command "Start-Sleep -Seconds 5"'
                
                // 🔹 Check if container is running
                bat "docker ps"
                echo "Container started successfully! Visit http://localhost:5000 to see your app."
            }
        }
    }

    post {
        success {
            echo "✅ Jenkins pipeline completed successfully. Swiggy app is running at http://localhost:5000"
        }
        failure {
            echo "❌ Build failed. Check the console logs above."
        }
        always {
            echo "Pipeline finished (finaldev project)."
        }
    }
}
