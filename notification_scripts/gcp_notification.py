"""
Script to send notifications to the user (via emai, sms, slack, phone, etc.) for
triggers on GCP.

This module provides the following functions:

* :func:`trigger_notification`
* :func:`IFTTT_action`
* :func:`get_load_averages`
* :func:`get_ram_usage`
* :func:`get_cpu_usage`
"""

import requests, os, psutil

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
    cpu_threshold = 90
    trigger_dict = {
        'cpu_trigger': [True, cpu_threshold],
        'ram_trigger': [True, 90],
        'load_trigger': [True, 1.5],
        'return_trigger': [True]
    }
    for key, value in trigger_dict.items():
        if value[0]:
            if key == 'cpu_trigger':
                if get_cpu_usage() > value[1]:
                    IFTTT_action('cpu_trigger', IFTTT_key)
            elif key == 'ram_trigger':
                if get_ram_usage('percentage_available') < value[1]:
                    IFTTT_action('ram_trigger', IFTTT_key)
            elif key == 'load_trigger':
                if get_load_averages()['1min'] > value[1]:
                    IFTTT_action('load_trigger', IFTTT_key)
            elif key == 'return_trigger':
                if return_value_check()[0]:
                    IFTTT_action('return_trigger', IFTTT_key)


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
