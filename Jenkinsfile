pipeline {
    agent any
    environment {
        KUBECONFIG = credentials('kubeconfig-k3s')
    }
    stages {
        stage('Clone Repository') {
            steps {
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
                    withCredentials([usernamePassword(credentialsId: '856b9510-0071-4cae-b516-2217b5cddadf', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                        sh 'docker tag flask-app:latest $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker push $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker rmi $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker rmi flask-app:latest'
                        sh 'docker image prune -af --filter "until=15m'
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            agent {
                docker { image 'alpine/k8s:1.29.13' }
            }
            steps {
                sh 'echo "$KUBECONFIG"'
                sh 'helm --kubeconfig="$kubeconfig" list'
            }
        }
    }
}

