#!/bin/bash

# Load configuration from environment variables or default values
_threshold=${LOAD_AVERAGE_THRESHOLD:-2.0}
consecutive_checks=${CONSECUTIVE_CHECKS:-3}
trigger_check_dict=(
    "day_of_week:true"
    "time_of_day:true"
    "load_average:false"
) 
trigger_interval=${TRIGGER_INTERVAL:-30} # Trigger interval in minutes

poweroff () {
    # Function to poweroff the VM, with the reason and date appended to the
    # syslog.

    sleep 2
    logger -t auto_shutdown "Powering off VM in 60 seconds. Reason: $1"
    logger -t auto_shutdown "Initiated at $(date)."
    sleep 60
    sudo poweroff || logger -t auto_shutdown "Failed to power off VM"
}

day_of_week () {
    _dow="$(date +'%A')"
    if [[ $_dow = 'Saturday' ]] || [[ $_dow = 'Sunday' ]]
    then
        poweroff "Outside of working days (day of week: $_dow)."
    fi
}

time_of_day () {
    _hour="$(date +'%H')"
    if [[ $_hour -ge 22 ]] || [[ $_hour -le 6 ]]
    then
        poweroff "Outside of working hours (hour: $_hour)."
    fi
}

load_average () {
    for (( i=1; i<=$consecutive_checks; i++ ))
    do
        _load_average=$(uptime | awk '{ print $10 }')
        if (( $(echo "$_load_average < $_threshold" | bc -l) ))
        then
            logger -t auto_shutdown "VM idling, load average: $_load_average"
        else
            break
        fi

        if (( i == consecutive_checks ))
        then
            poweroff "VM is idle after $i checks."
        fi
        sleep 60
    done
}

poweroff_triggers () {  
    day_of_week_check=$(get_dict_val "day_of_week" "${trigger_check_dict[@]}")
    time_of_day_check=$(get_dict_val "time_of_day" "${trigger_check_dict[@]}")
    load_average_check=$(get_dict_val "load_average" "${trigger_check_dict[@]}")
    
    if [[ $day_of_week_check == "true" ]]
    then
        day_of_week
    fi
    if [[ $time_of_day_check == "true" ]]
    then
        time_of_day
    fi
    if [[ $load_average_check == "true" ]]
    then
        load_average
    fi
}

get_dict_val () {
	local _key="$1"
	shift
	local _dict=("$@")
    
	for index in "${_dict[@]}"
	do
		key="${index%%:*}"
        
        if [[ $key == $_key ]]
        then
			value="${index##*:}"
			echo $value
			break
		fi

	done
}

main () {
    logger -t auto_shutdown "Started script at: $(date)."

    while true
    do
        poweroff_triggers
        sleep $(($trigger_interval * 60))
    done
}

# Run the main function.
main
