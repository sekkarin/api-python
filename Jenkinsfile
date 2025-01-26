pipeline {
    agent {
        kubernetes {
            cloud 'k3s' // Specify the K3s cloud configured in Jenkins
            label 'kubectl-agent' // Define a unique label for the pod
            yaml """
apiVersion: v1
kind: Pod
metadata:
  labels:
    jenkins: kubectl-agent
spec:
  containers:
  - name: kubectl
    image: bitnami/kubectl:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - name: kube-config
      mountPath: /root/.kube
  volumes:
  - name: kube-config
    hostPath:
      path: /home/jenkins/.kube
      type: Directory
"""
        }
    }
    stages {
        stage('Verify Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                        echo "Checking Kubernetes connectivity..."
                        kubectl version --client
                        kubectl get nodes
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                container('kubectl') {
                    sh '''
                        echo "Deploying to K3s cluster..."
                        kubectl apply -f k8s/service.yaml
                        kubectl get services
                    '''
                }
            }
        }
    }
}
