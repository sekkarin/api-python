pipeline {
    agent any
    environment {
        GIT_BRANCH = env.GIT_BRANCH.replace('origin/', '')
        BRANCH_NAME = "${GIT_BRANCH}-${BUILD_ID}"
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
                        sh 'docker tag flask-app:latest $DOCKER_USERNAME/flask-app:$BRANCH_NAME'
                        sh 'docker push $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker push $DOCKER_USERNAME/flask-app:$BRANCH_NAME'
                        sh 'docker rmi $DOCKER_USERNAME/flask-app:latest'
                        sh 'docker rmi $DOCKER_USERNAME/flask-app:$BRANCH_NAME'
                        sh 'docker rmi flask-app:latest'
                        // sh 'docker image prune -af --filter "until=30m"'
                    }
                }
            }
        }
        stage('Deploy to Kubernetes') {
            agent {
                docker { image 'alpine/k8s:1.29.13' }
            }
            environment {
                KUBECONFIG_FILE = '/tmp/kubeconfig' // Path inside the container
            }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-k3s', variable: 'KUBECONFIG_PATH')]) {
                    sh '''
                        echo "Deploying with Helm..."
                        cp "$KUBECONFIG_PATH" "$KUBECONFIG_FILE"
                        helm --kubeconfig="$KUBECONFIG_FILE" list -a
                    '''
                }
            }
        }
    }
}

