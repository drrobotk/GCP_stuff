## GCP shutdown scripts

This shutdown script can automatically poweroff a GCP VM instance on specified triggers such as the time of day, day of week or the load average to determine when the VM has been idle for a given time.

# Usage:
In order to add the automatic shutdown script to the VM instance on GCP, you need to run the following command:
```
gcloud compute instances add-metadata VM_INSTANCE_NAME --metadata-from-file startup-script=auto_shutdown_script.sh
```
You can also add the metadata directly from the cloud compute section of the VM instance on GCP.

### Config

The trigger config can be set within the script from the parameters:

```bash
_threshold=2.0 # Load average threshold.
consecutive_checks=3 # Number of consecutive checks to check if VM is idle.
trigger_check_dict=(
    "day_of_week:true"
    "time_of_day:true"
    "load_average:false"
) 
trigger_interval=30 # Trigger interval in minutes
```
