pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps{
                script {
                     checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/sekkarin/api-python.git']])
                }   
            }
                    
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d -p 0.0.0.0:5000:5000 flask-app'
            }
        }
    }
}
