# GCP Stuff

A collection of helpful scripts for Virtual Machine (VM) Instances on the Google Cloud Platform (GCP).

These scripts have been tested with VM instances created from the Vertex AI workbench.
## Scripts

Current available scripts are:

# GCP Stuff

A collection of helpful scripts for Virtual Machine (VM) Instances on the Google Cloud Platform (GCP).

These scripts have been tested with VM instances created from the Vertex AI workbench.
## Scripts

Current available scripts are:

* Visual Studio Code (VScode) setup for GCP via SSH: [`vscode_setup/gcp_vscode_setup.py`](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/vscode_setup/gcp_vscode_setup.py) (python) [README.md](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/vscode_setup/README.md)
* GCP auto shutdown script with various triggers: [`shutdown_scripts/auto_shutdown_script.sh`](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/shutdown_scripts/auto_shutdown_script.sh) (bash) [README.md](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/shutdown_scripts/README.md)
* GCP notification script with various triggers: [`notification_scripts/gcp_notification.py`](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/notification_scripts/gcp_notification.py) (python) [README.md](https://github.com/drrobotk/GCP_stuff/blob/5a7e0d5f813acc7bd7c104ea8ada07b30faf29f4/notification_scripts/README.md)

See the `README.md` in each directory for more information on each script.
### Directory layout:
    .
    ├── LICENSE
    ├── README.md
    ├── notification_scripts
    │   ├── README.md
    │   ├── gcp_notification.py
    │   └── trigger.conf
    ├── shutdown_scripts
    │   ├── README.md
    │   └── auto_shutdown_script.sh
    └── vscode_setup
        ├── README.md
        ├── gcp_setup.sh
        ├── gcp_vscode_setup.py
        └── helpers.py
