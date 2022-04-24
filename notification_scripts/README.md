## GCP Notification scripts

This Script will send notifications to the user (via email, sms, slack, phone, etc.) for triggers on GCP. These notifications for these triggers would also need to be set up on the <a href="https://ifttt.com/">IFTTT</a> website.

## Usage

In order to run the script, you can either set it as a startup script within the metadata for the VM instance on GCP or run it directly from a terminal using screen:

```bash
screen -d -m python gcp_notification.py
```

### Trigger configuration

The configuration for the triggers can be set in the `trigger.conf` file:

```yaml
triggers:
    cpu:
        {
            enabled: True,
            threshold: 90,
            action: 'sms',
        }
    memory:
        {
            enabled: True,
            threshold: 8,
            action: 'sms',
        }
    load_average:
        {
            enabled: True,
            threshold: 1.5,
            action: 'sms',
        }
    return_status_vals:
        {
            enabled: True,
            vals: [0,1],
            action: 'sms',
        }
```

### Environment Variables

The following environment variables should be set.

| Key | Value | Notes |
| --- | --- | --- |
| `IFTTT_key` | <your_unique_key> | IFTTT key unique to your account |

The unique key can be found from by visiting the Webhooks service page and clicking Documentation on IFTTT. This can be set in python using:

```python
import os; os.environ["IFTTT_key"] = 'your_unique_key'
```
## What is IFTTT?
<img src="https://user-images.githubusercontent.com/51001263/164946362-da457b19-99f2-47fb-a770-165107f7a445.png" width="20%" />

IFTTT (IF This Then That) is a free web-based service that people use to create chains of simple conditional statements, called applets, which will coordinate small tasks between Internet and web services.

<img src="https://user-images.githubusercontent.com/51001263/164946431-099c7100-e82a-46dc-99f0-693cc5a124ac.png" width="44%" /> <img src="https://user-images.githubusercontent.com/51001263/164946394-b321227c-613e-4bc8-932a-8c1deccd8f72.png" width="32%" /> 

In particular, this script makes use of the maker `webhooks` service: https://ifttt.com/maker_webhooks

<img src="https://user-images.githubusercontent.com/51001263/164946245-2541355b-1a6c-4be2-a845-44e5061a1923.png" width="35%" />

A Webhook allows you to integrate with services that are not already on IFTTT using simple web requests. These Webhooks are unique to you using your own unique URL key, which can be found in the Documentation section of the Webhooks service page. A Webhook can act as both a trigger and an action, so the web requests are extremely flexible and customizable.

For more information on webhooks, see:

https://ifttt.com/maker_webhooks/details

https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ

An example of a phone call notification can be set up using the webhook as a trigger and the phone call service as the notification:

<img src="https://user-images.githubusercontent.com/51001263/164946264-5138db3b-e586-4f52-9d50-9ad8efb7974e.png" width="30%" />
