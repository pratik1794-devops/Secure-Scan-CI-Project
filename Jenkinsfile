pipeline {
    agent any
    
    environment {
        SCANNER_CONFIG = '/app/config/policies.yaml'
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t secure-scan-ci .'
            }
        }
        
        stage('Scan') {
            steps {
                sh '''
                docker run --rm \
                -v ${WORKSPACE}/reports:/app/reports \
                -v ${WORKSPACE}/config:/app/config \
                secure-scan-ci
                '''
            }
        }
        
        stage('Report') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                archiveArtifacts artifacts: 'reports/*.pdf', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}