pipeline {
    agent any

    environment {
        AWS_REGION = 'us-east-1'      // Just for boto3 initialization
        PYTHON_SCRIPT = 'delete_old_unattached_ebs.py'
    }

    triggers {
        cron('0 1 * * 0') // Every Sunday at 1:00 AM UTC
    }

    stages {
        stage('Verify IAM Role') {
            steps {
                sh '''
                echo "🔒 Verifying IAM Role from instance metadata..."
                curl -s http://169.254.169.254/latest/meta-data/iam/info || echo "⚠️ Unable to verify IAM role. Ensure agent has IAM role: delete-ebs-role"
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install boto3
                '''
            }
        }

        stage('Run EBS Cleanup Script') {
            steps {
                sh '''
                . venv/bin/activate
                python ${PYTHON_SCRIPT}
                '''
            }
        }
    }

    post {
        success {
            echo '✅ EBS cleanup completed successfully.'
        }
        failure {
            echo '❌ EBS cleanup failed. Check the logs.'
        }
    }
}
