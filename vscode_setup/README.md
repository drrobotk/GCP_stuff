## GCP VScode setup (EXPERIMENTAL!)
VScode setup script to connect to a VM instance on GCP via SSH.

You can use this script to install and initialize the gcloud-sdk for a project, create ssh keys locally, add them to the VM instance and setup the SSH extension in VScode. You can optionally create a bash script for the setup steps instead of execution.

# Usage
Before you run the script, a notebook should be created for the VM instance on GCP within a project e.g from the Vertex AI
workbench. The VM IP address can be found from the compute engine metadata.

```
usage: gcp_vscode_setup.py --email email --project_id project_id --vm_instance_name vm_instance_name --vm_ip vm_ip
[--vm_zone vm_zone] [--sdk_version sdk_version] [--bash_script bash_script] [-h]

required arguments:

--email               Email login for GCP
--project_id          Project identifier or name
--vm_instance_name    Name of VM instance on GCP
--vm_ip               External IP address of VM instance

optional arguments:

--vm_zone             Location zone of VM instance (default: `europe-west2-a`)
--sdk_version         SDK version for gcloud install (default: `381.0.0`)
--bash_script         Export setup steps as bash script instead of execution (default: False)
```

This script is still experimental, if you run into any issues then I would suggest using the `--bash_script True` option which will output the setup steps in a bash script (`gcp_setup.sh`) instead of direct execution, which can be used for debugging or performing the steps manually in a terminal window.
