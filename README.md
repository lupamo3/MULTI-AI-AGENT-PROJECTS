# Multi AI Agent Project
# poetry run python -m app.main
#docker build -t multi-agent-app . 
# 


#
docker run -d --name multi-agent-app \                     
  --privileged \
  -p 8080:8080 -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
 multi-agent-app
 #

 #32fdb60a57dd4b01a48b6f6adac79ecc
/var/jenkins_home/secrets/initialAdminPassword


#docker restart jenkins-dind


