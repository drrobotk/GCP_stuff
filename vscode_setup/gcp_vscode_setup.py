"""Script to install the gcloud-sdk on a MacOS and initialize it for vscode via 
SSH.

usage: gcp_vscode_setup.py --email email --project_id project_id
                           --vm_instance_name vm_instance_name --vm_ip vm_ip
                           [--vm_zone vm_zone] [--sdk_version sdk_version]
                           [--bash_script bash_script] [-h]

You can use this script to install and initialize the gcloud-sdk for a project,
create ssh keys locally, add them to the VM instance and setup the SSH extension
in vscode. You can optionally create a bash script for the setup steps.

A notebook should be created for the VM instance on GCP e.g from the Vertex AI
workbench. The VM IP address can be found from the compute engine metadata.
"""
import subprocess, textwrap, argparse

from helpers import progress_bar

__author__ = ['Dr. Usman Kayani']

def gcp_vscode_setup(
    email: str,
    project_id: str,
    vm_instance_name: str,
    vm_ip: str,
    vm_zone: str = 'europe-west2-a',
    sdk_version: str = '387.0.0',
    bash_script: str = False,
) -> None:
    '''
    This function will install and initialize the gcloud-sdk for a project,
    create ssh keys locally, add them to the VM instance and setup the SSH
    extension in vscode. 

    Parameters:
        email: str
            The email address of the user.
        project_id: str
            The project ID of the GCP project.
        vm_instance: str
            The name of the VM instance.
        vm_ip: str
            The IP address of the VM instance.
        vm_zone: optional str, default `europe-west2-a`
            The zone for the VM instance.
        sdk_version: optional str, default `381.0.0`
            The version for the gcloud SDK installation.
        bash_script: optional bool, default False
            export setup as bash script in the home directory as `gcp_setup.sh`
        
    Returns:
        None
    '''
    update_packages = 'brew update && brew upgrade && cd ~/.'

    gcloud_url = f'https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-{sdk_version}-darwin-arm.tar.gz'

    download_gcloud = f'''
    wget {gcloud_url}
    sudo tar -xvf {gcloud_url.split('/')[-1]}'''
    
    install_gcloud = f'''
    ./google-cloud-sdk/install.sh 
    ./google-cloud-sdk/bin/gcloud init 
    ./google-cloud-sdk/bin/gcloud config set project {project_id}'''

    gcp_username = email.replace('@', '_').replace('.', '_')

    vm_jupyter_permissions = f'sudo chown -R {gcp_username} /home/jupyter/'
    generate_ssh_keys = f'''
    gcloud compute ssh {gcp_username}@{vm_instance_name} --project={project_id} --zone={vm_zone} --command="{vm_jupyter_permissions}" --quiet
    gcloud compute os-login ssh-keys add --key-file=~/.ssh/google_compute_engine.pub --project={project_id} --quiet'''

    vscode_ssh_setup = f'''
    code --install-extension ms-vscode-remote.remote-ssh
    tee -a ~/.ssh/config << END
    Host {vm_instance_name}
        HostName {vm_ip}
        IdentityFile ~/.ssh/google_compute_engine
        User {gcp_username}
    END'''

    setup_steps = [
        (update_packages, "Updating packages..."),
        (download_gcloud, "Downloading gcloud SDK..."),
        (install_gcloud, "Installing gcloud SDK..."),
        (generate_ssh_keys, "Generating SSH keys..."),
        (vscode_ssh_setup, "Setting up SSH extension..."),
    ]

    setup_steps = [textwrap.dedent(lines) for lines in setup_steps]

    if bash_script:
        output_file = open('gcp_setup.sh', 'w')
        output_file.write('\n'.join(setup_steps))
        output_file.close()
    else:
        total_steps = len(setup_steps)
        for i, (cmd, message) in enumerate(setup_steps):
            print(message)
            subprocess.call(cmd, shell=True)
            progress_bar(i, total_steps-1)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(add_help=False)

    # Required arguments.
    parser.add_argument('--email', type=str, metavar='email', help='Email login for GCP.', required=True)
    parser.add_argument('--project_id', type=str, metavar='project_id', help='Project ID on GCP.', required=True)
    parser.add_argument('--vm_instance_name', type=str, metavar='vm_instance_name', help='VM instance name on Vertex AI', required=True)
    parser.add_argument('--vm_ip', type=str, metavar='vm_ip', help='VM instance IP for SSH.', required=True)

    # Optional arguments.
    parser.add_argument('--vm_zone', type=str, metavar='vm_zone', help='VM instance zone on GCP.', default='europe-west2-a', required=False)
    parser.add_argument('--sdk_version', type=str, metavar='sdk_version', help='GCP SDK version.', default='381.0.0', required=False)
    parser.add_argument('--bash_script', type=bool, metavar='bash_script', help='Export setup as bash script.', default=False, required=False)
    parser.add_argument('-h', '--help', action='store_true', help='show this help message and exit', required=False)

    args = parser.parse_args()

    kwargs = {x[0]: x[1] for x in args._get_kwargs()}
    gcp_vscode_setup(**kwargs)
