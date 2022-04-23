"""
Script to send notifications to the user (via emai, sms, slack, phone, etc.) for
triggers on GCP.

This module provides the following functions:

* :func:`trigger_notification` (main entry point)
* :func:`IFTTT_action`
* :func:`get_load_averages`
* :func:`get_ram_usage`
* :func:`get_cpu_usage`
"""

import requests, os, psutil, time, logging

# Declare global variables for trigger configuration.
CPU_threshold = 90
RAM_threshold = 8
load_threshold = 1.5
return_status_vals = [0,1]
trigger_check_period = 1 # In minutes.

trigger_conf = {
    'cpu': {
        'enabled': True,
        'threshold': CPU_threshold
    },
    'ram': {
        'enabled': True,
        'threshold': RAM_threshold
    },
    'load': {
        'enabled': True,
        'threshold': load_threshold
    },
    'return_status': {
        'enabled': True,
        'values': return_status_vals
    }
}

def trigger_notification(
    IFTTT_key: str,
) -> None:
    """
    Trigger notification via IFTTT.
    
    Parameters:
        trigger_type: str
            The trigger type.
        IFTTT_key: str
            The IFTTT key.
    
    Returns:
        None
    """
    trigger_vals = {
        'cpu': get_cpu_usage(),
        'ram': get_ram_usage()['percentage_available'],
        'load': get_load_averages()['1min'],
        'return': return_value_check()
    }
    for key, value in trigger_conf.items():
        if value['enabled'] and trigger_vals[key] >= value['threshold']:
            logger.info(f'Triggering {key} notification.')
            IFTTT_action(key, IFTTT_key)


def IFTTT_action(
    action: str, 
    key: str
) -> None:
    """
    Trigger action via IFTTT.
    
    Parameters:
        action: str
            The action to trigger.
        key: str
            The IFTTT key.
    
    Returns:
        None
    """
    requests.post(f'https://maker.ifttt.com/trigger/{action}/with/key/{key}')


def get_load_averages():
    """
    Get the load averages.
    
    Returns:
        list
            The load averages.
    """
    load1, load5, load15 = os.getloadavg()
    return {'1min': load1, '5min': load5, '15min': load15}


def get_ram_usage(key: str = None) -> None:
    """
    Get the RAM usage.
    
    Returns:
        dict
            The RAM usage.
    """
    memory_dict = psutil.virtual_memory()._asdict()
    memory_dict['percentage_available'] = (memory_dict['available']*100)/ memory_dict['total']
    if key:
        return psutil.virtual_memory()._asdict()[key]
    return psutil.virtual_memory()._asdict()


def get_cpu_usage(interval: int = 1) -> None:
    """
    Get the CPU usage.
    
    Returns:
        dict
            The CPU usage.
    """
    return psutil.cpu_percent(interval=interval)


def return_value_check():
    """
    Check if function returns a value.
    
    Returns:
        bool
            True if the function returns a value, False otherwise.
    """
    scripts = ['test1.py', 'test2.py']
    for i, script in enumerate(scripts):
        return os.path.exists(i), script


if __name__ == '__main__':
    logger = logging.getLogger('GCP_notification')
    logger.setLevel(logging.DEBUG)
    logger.info(f'Starting GCP notification script at {time.time()}.')

    while True:
        logger.info('Checking for triggers.')
        trigger_notification(
            IFTTT_key=os.environ['IFTTT_key']
        )
        time.sleep(trigger_check_period*60)
