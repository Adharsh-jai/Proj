pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Adharsh-jai/Proj.git'
            }
        }

        stage('Build Image') {
            steps {
                bat 'docker build -t fastapi-app .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d -p 5000:5000 fastapi-app'
            }
        }
    }
}
