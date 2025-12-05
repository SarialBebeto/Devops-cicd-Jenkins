pipeline {
  environment { 
    DOCKER_ID = "sarialbebeto" 
    DOCKER_TAG = "v.${BUILD_ID}.0" 
  }
  agent any 
  stages {

    stage('Install Docker Buildx') {
      steps {
        sh '''
        echo "=== Installing Docker Buildx ==="

        # Create plugins folder if missing
        mkdir -p ~/.docker/cli-plugins

        # Download latest docker buildx binary
        BUILDX_VERSION=$(curl -s https://api.github.com/repos/docker/buildx/releases/latest | grep tag_name | cut -d '"' -f 4)
        echo "Installing buildx version: $BUILDX_VERSION"

        curl -L https://github.com/docker/buildx/releases/download/${BUILDX_VERSION}/buildx-${BUILDX_VERSION}.linux-amd64 \
            -o ~/.docker/cli-plugins/docker-buildx

        chmod +x ~/.docker/cli-plugins/docker-buildx

        echo "=== Buildx installed ==="
        docker buildx version
        '''
            }
        }



    stage('Docker Build images') { // docker build image stage
      steps {
        script {
          sh '''
          export DOCKER_BUILDKIT=1
          export BUILDKIT_PROGRESS=plain
          docker buildx build -t $DOCKER_ID/fastapi-dev:$DOCKER_TAG -f Dockerfile .
          docker buildx build -t $DOCKER_ID/fastapi-prod:$DOCKER_TAG -f Dockerfile.prod .
          sleep 6
          '''
        }
      }
    }

    stage('Docker Push image') { 
      environment {
            DOCKER_PASS = credentials("DOCKER_HUB_PASS") // we retrieve docker password from secret text called docker_hub_pass saved on jenkins
        }
      steps {
        script {
          sh '''
          docker login -u $DOCKER_ID -p $DOCKER_PASS
          docker push $DOCKER_ID/fastapi-dev:$DOCKER_TAG
          docker push $DOCKER_ID/fastapi-prod:$DOCKER_TAG
          '''
        }
      }
    }

    stage('Deployment in dev'){
      environment
      {
        KUBECONFIG = credentials("config") // we retrieve kubeconfig from secret file called config saved on jenkins
      }
      steps {
        script {
          sh '''
          rm -Rf .kube
          mkdir .kube
          ls
          cat $KUBECONFIG > .kube/config
          cp fastapi-deployment/values.yaml values.yml
          cat values.yml
          sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
          helm upgrade --install app fastapi-deployment --values=values.yml --namespace dev --force
          sleep 5
          kubectl get pods -n dev
          kubectl get svc -n dev
          kubectl logs app-fastapi-deployment-db-0 -n dev
          '''
        }
      }
    }

    stage('Deployment in staging') {
      environment {
        KUBECONFIG = credentials("config") 
      }
      steps {
        script {
          sh '''
          rm -Rf .kube
          mkdir .kube
          ls
          cat $KUBECONFIG > .kube/config
          cp fastapi-deployment/values.yaml values.yml
          cat values.yml
          sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
          helm upgrade --install app fastapi-deployment --values=values.yml --namespace staging --force
          '''
        }
      }
    }

    stage('Deployment in prod'){
      environment {
        KUBECONFIG = credentials("config") 
      }
      steps {
      // Create an Approval Button with a timeout of 15 minutes.
      // this requires a manual validation in order to deploy on production environment
        timeout(time: 15, unit: "MINUTES") {
            input message: 'Do you want to deploy in production ?', ok: 'Yes'
        }
        script {
          sh '''
          rm -Rf .kube
          mkdir .kube
          ls
          cat $KUBECONFIG > .kube/config
          cp fastapi-deployment-prod/values.yaml values.yml
          cat values.yml
          sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
          helm upgrade --install app fastapi-deployment-prod --values=values.yml --namespace prod
          '''
        }
      }
    }
  }
}