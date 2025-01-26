pipeline {
    agent any
    //  parameters {
    //         booleanParam(name: 'Clone Repositor', defaultValue: false, description: '...')
    //         booleanParam(name: 'Build Docker Image', defaultValue: false, description: '....')
    //         booleanParam(name: 'Deploy', defaultValue: false, description: '...')
    // }
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
                    withCredentials([usernamePassword(credentialsId: '856b9510-0071-4cae-b516-2217b5cddadf', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                        // Correctly tag the Docker image
                        sh 'docker tag flask-app:latest $DOCKER_USERNAME/flask-app:latest'
                        // Push the image to Docker Hub
                        sh 'docker push $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker rmi $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker rmi flask-app:latest'
                    }
                }
            }
        }
       stage('Deploy to Kubernetes') {
            steps {
                podTemplate(agentInjection: true, cloud: 'k3s', name: 'k3s') {
                     sh """
                        kubectl 
                    //    kubectl apply -f k8s/service.yaml 
                    """
                }
               // container('kubectl') {
             //       sh """
             //           kubectl 
                    //    kubectl apply -f k8s/service.yaml 
           //         """
            //    }
            }
        }
    }
}
