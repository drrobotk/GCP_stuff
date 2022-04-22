## GCP shutdown scripts

# Usage:
In order to add the automatic shutdown script to the VM instance on GCP, you need to run the following command:
```
gcloud compute instances add-metadata VM_INSTANCE_NAME \\
[--zone=VM_ZONE] --metadata-from-file startup-script=auto_shutdown_script.sh
```
You can also add the metadata direction from the cloud compute section of the VM instance on GCP.
