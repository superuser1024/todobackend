node {
    checkout scm
    
    try {
        stage 'Run unit/integration tests'
        sh 'make test'
        
        stage 'Build application artifacts'
        sh 'make build'
        
        stage 'Create release environment and run acceptance tests'
        sh 'make release'
        
        stage 'Tag and publish release image'
        sh 'make tag latest \$(git rev-parse --short HEAD) \$(git tag --points-at HEAD)'
        sh 'make buildtag master \$(git tag --points-at HEAD)'
        withEnv(["DOCKER_USER=${DOCKER_USER}",
                         "DOCKER_PASSWORD=${DOCKER_PASSWORD}"]) {
                     sh 'make login'
                 }
        sh 'make publish'

        stage 'Deploy release'
        build job: 'todobackend-deploy', parameters: [string(name: 'IMAGE_TAG', value: 'reboot87/todobackend:latest'), string(name: 'TASKS', value: ''), password(description: 'Database password', name: 'db_password', value: <object of type hudson.util.Secret>)]
        
    }
    finally {
        stage 'Collect test reports'
        junit keepLongStdio: true, testResults: '**/reports/*.xml'
        
        stage 'Clean up'
        sh 'make clean'
        sh 'make logout'
    }
}
