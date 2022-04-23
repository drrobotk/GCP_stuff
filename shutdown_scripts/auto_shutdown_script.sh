#!/bin/bash

# This script is used to automatically shutdown a VM instance on GCP using a number of triggers.
# Author: Dr. Usman Kayani.

poweroff () {
    # Function to poweroff the VM, with the reason and date appended to the
    # logfile.

    sleep 2
    echo "Powering off VM in 60 seconds. Reason: $1" >> script.log
    echo "Intiated at $(date)." >> script.log
    cat script.log
    sleep 60
    sudo poweroff
}

day_of_week () {
    # Function to check if day of week is outside working days and if so,
    # poweroff VM.
    
    # Check if day is a weekend day.
    _dow="$(date +'%A')"
    if [ $_dow = 'Saturday' ] || [ $_dow = 'Sunday' ]
    then
        poweroff "Outside of working days (day of week: $_dow)."
    fi
}

time_of_day () {
    # Function to check if time of day is outside of working hours and if so,
    # poweroff VM.

    # Check if hour is between 10pm and 6am.
    _hour="$(date +'%H')"
    if [ $_hour -ge 22 ] || [ $_hour -le 6 ]
    then
        poweroff "Outside of working hours (hour: $_hour)."
    fi
}

load_average () {
    # Function to check if load average is above threshold and if so, poweroff
    # VM.

    for (( i=1; i<=$consecutive_checks; i++ ))
    do
        # Get the 15-minute load average and check if it is above the threshold
        # a given number of times in a row.
        _load_average=$(uptime | sed -e 's/.*load averages: //g' | awk '{ print $3 }')
        res=$(echo $_load_average'<'$_threshold | bc -l)

        if [ $res == 1 ]
        then
            # If the VM is Idle after a check, append details to logfile.
            echo "VM idling..." >> script.log
            echo "Check number: $count." >> script.log
            echo "Load average: $_load_average." >> script.log
            echo "Date: $(date)." >> script.log
        else
            break
        fi

        # If afrer a number of consecutive checks, the VM is still idle, then
        # poweroff.
        if [ $i == $consecutive_checks ]
        then
            poweroff "VM is idle after $count checks."
        fi
        sleep 60

    done
}

poweroff_triggers () {  
    # Function to apply the triggers to poweroff the VM, where the triggers to
    # check are specified in a dictionary.

    # If the flag is true, then apply the triggers.
    if [ $day_of_week_check == "true" ]
    then
        day_of_week
    fi
    if [ $time_of_day_check == "true" ]
    then
        time_of_day
    fi
    if [ $load_average_check == "true" ]
    then
        load_average
    fi
}

get_dict () {
    # Function to get the value of a key from a dictionary.

	local _key="$1"
	shift
	local _dict=("$@")
    
	for index in "${_dict[@]}"
	do
		key="${index%%:*}"
		value="${index##*:}"

        # If the key matches the one specified, return the value and break the
        # for loop.
		if [ $key == $_key ]
		then
			value="${index##*:}"
			echo $value
			break
		fi

	done
}

main () {
    # Main function to start the logfile and apply the triggers after a
    # specified time interval.

    echo "-------------------------------------------------------------------------------------------------------------------------" >> script.log
    echo "Started script at: $(date)." >> script.log

    # Get flags for each trigger.
    day_of_week_check=$(get_dict "day_of_week" "${trigger_check_dict[@]}")
    time_of_day_check=$(get_dict "time_of_day" "${trigger_check_dict[@]}")
    load_average_check=$(get_dict "load_average" "${trigger_check_dict[@]}")
    
    while true
    do
        poweroff_triggers
        sleep $(($trigger_interval * 60))
    done
}

# Declare the variables and run the main function.

_threshold=2.0 # Load average threshold.
consecutive_checks=3 # Number of consecutive checks to check if VM is idle.
trigger_check_dict=(
    "day_of_week:true"
    "time_of_day:true"
    "load_average:false"
) 
trigger_interval=30 # Trigger interval in minutes

main
