pipeline {
    agent any
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
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    // Use a pod template with kubectl installed
                    podTemplate(
                        name: 'kubectl-pod',
                        containers: [
                            containerTemplate(
                                name: 'kubectl',
                                image: 'bitnami/kubectl:latest',
                                command: 'sleep',
                                args: '99999'
                            )
                        ]
                    ) {
                        node('vm2') {
                            container('kubectl') {
                                sh """
                                    kubectl version --client
//                                    kubectl apply -f k8s/deployment.yaml
//                                    kubectl apply -f k8s/service.yaml
                                """
                            }
                        }
                    }
                }
            }
        }
    }
}
