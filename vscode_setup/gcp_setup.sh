brew update && brew upgrade && cd ~/.

wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-381.0.0-darwin-arm.tar.gz
sudo tar -xvf google-cloud-cli-381.0.0-darwin-arm.tar.gz

./google-cloud-sdk/install.sh 
./google-cloud-sdk/bin/gcloud init 
./google-cloud-sdk/bin/gcloud config set project project_name

gcloud compute ssh —-project=project_name --zone=europe-west2-a test_domain_com@vm_name1 --command="sudo chown -R test_domain_com /home/jupyter/" --quiet
gcloud compute os-login ssh-keys add --key-file=~/.ssh/google_compute_engine.pub —-project=project_name --quiet

code --install-extension ms-vscode-remote.remote-ssh
tee -a ~/.ssh/config << END
Host vm_name1
    HostName 1.1.1.1
    IdentityFile ~/.ssh/google_compute_engine
    User test_domain_com
END