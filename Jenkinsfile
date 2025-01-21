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
                sh 'docker build -t flask-app:latest .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker run -d --name api-app -p 192.168.33.10:5000:5000 flask-app:latest'
            }
        }
    }
}
