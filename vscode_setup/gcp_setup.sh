brew update && brew upgrade && cd ~/.

wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-381.0.0-darwin-arm.tar.gz
sudo tar -xvf google-cloud-cli-381.0.0-darwin-arm.tar.gz

./google-cloud-sdk/install.sh 
./google-cloud-sdk/bin/gcloud init 
./google-cloud-sdk/bin/gcloud config set project ons-tddcp-data-collection

~/google-cloud-sdk/bin/gcloud compute ssh usman_kayani_ons_gov_uk@usman --project=ons-tddcp-data-collection --zone=europe-west2-a --command="sudo chown -R usman_kayani_ons_gov_uk /home/jupyter/"
~/google-cloud-sdk/bin/gcloud compute os-login ssh-keys add --key-file=/Users/usmankayani/.ssh/google_compute_engine.pub --project=ons-tddcp-data-collection --quiet

code --install-extension ms-vscode-remote.remote-ssh
tee -a ~/.ssh/config << END
Host usman
    HostName 34.142.46.174
    IdentityFile ~/.ssh/google_compute_engine
    User usman_kayani_ons_gov_uk
END