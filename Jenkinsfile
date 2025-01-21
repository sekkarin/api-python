pipeline {
    agent any
     parameters {
            booleanParam(name: 'Clone Repositor', defaultValue: false, description: '...')
            booleanParam(name: 'Build Docker Image', defaultValue: false, description: '....')
            booleanParam(name: 'Deploy', defaultValue: false, description: '...')
    }
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
      stage('Push to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub using Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                    }
                    // Tag the Docker image with the Docker Hub repository
                    sh 'docker tag flask-app:latest $DOCKER_USERNAME/flask-app:latest'
                    // Push the Docker image to Docker Hub
                    sh 'docker push $DOCKER_USERNAME/flask-app:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker rm -f api-app'
                sh 'docker run -d --name api-app -p 192.168.33.10:5000:5000 flask-app:latest'
            }
        }
    }
}
