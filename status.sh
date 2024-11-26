#!/bin/bash
# Screenshot: http://s.natalian.org/2013-08-17/dwm_status.png
# Network speed stuff stolen from http://linuxclues.blogspot.sg/2009/11/shell-script-show-network-speed.html

# This function parses /proc/net/dev file searching for a line containing $interface data.
# Within that line, the first and ninth numbers after ':' are respectively the received and transmited bytes.
#function get_bytes {
## Find active network interface
#interface=$(ip route get 8.8.8.8 2>/dev/null| awk '{print $5}')
#line=$(grep $interface /proc/net/dev | cut -d ':' -f 2 | awk '{print "received_bytes="$1, "transmitted_bytes="$9}')
#eval $line
#now=$(date +%s%N)
#}

print_dash() {
  echo -e "\x01——"
}

dwm_network() {
  CONNAME=$(nmcli -a | grep '已连接' | awk 'NR==1{print $4}')
  if [ "$IDENTIFIER" = "unicode" ]; then
    echo "🌐 $CONNAME"
  else
    echo "NET $CONNAME"
  fi
}

# Function which calculates the speed using actual and old byte number.
# Speed is shown in KByte per second when greater or equal than 1 KByte per second.
# This function should be called each second.

#function get_velocity {
#value=$1
#old_value=$2
#now=$3

#timediff=$(($now - $old_time))
#velKB=$(echo "1000000000*($value-$old_value)/1024/$timediff" | bc)
#if test "$velKB" -gt 1024
#then
#echo $(echo "scale=2; $velKB/1024" | bc)MB/s
#else
#echo ${velKB}KB/s
#fi
#}

# Get initial values
#get_bytes
#old_received_bytes=$received_bytes
#old_transmitted_bytes=$transmitted_bytes
#old_time=$now

print_volume() {
  volume="$(amixer get Master | tail -n1 | sed -r 's/.*\[(.*)%\].*/\1/')"
  if test "$volume" -gt 0; then
    echo -e "\uE05D${volume}"
  else
    echo -e "Mute"
  fi
}

print_network() {
  network_name=$(nmcli | grep 'connected to ' | awk -F 'connected to ' '{print $2}')
  if [[ $network_name ]]; then
    echo -e "\x01[${network_name}]"
  fi
}

print_mem() {
  memfree=$(($(grep -m1 'MemAvailable:' /proc/meminfo | awk '{print $2}') / 1024))
  echo -e "\x04[${memfree}M]"
}

print_temp() {
  test -f /sys/class/thermal/thermal_zone0/temp || return 0
  echo $(head -c 2 /sys/class/thermal/thermal_zone0/temp)C
}

#!/bin/bash

#get_time_until_charged() {

#sum_remaining_charge=$(acpitool -B | grep -E 'Last full capacity' | awk '{print $5}' | grep -Eo "[0-9]+" | paste -sd+ | bc);

#sum_remaining_charge_percent=$(acpitool -B | grep -E 'Remaining capacity' | awk '{print $5}' | grep -Eo "[0-9.]+" | paste -sd+ | bc);

#sum_remaining_charge=$sum_remaining_charge*$sum_remaining_charge_percent/100;
## finds the rate at which the batteries being drained at
#present_rate=$(acpitool -B | grep -E 'Present rate' | awk '{print $4}' | grep -Eo "[0-9]+" | paste -sd+ | bc);

## divides current charge by the rate at which it's falling, then converts it into seconds for `date`
#seconds=$(bc <<< "scale = 10; ($sum_remaining_charge / $present_rate) * 3600");

## prettifies the seconds into h:mm:ss format
#pretty_time=$(date -u -d @${seconds} +%T);

#echo $pretty_time;
#}

get_battery_combined_percent() {

  # get charge of all batteries, combine them
  total_charge=$(expr $(acpi -b | awk '{print $4}' | grep -Eo "[0-9]+" | paste -sd+ | bc))

  # get amount of batteries in the device
  battery_number=$(acpi -b | wc -l)

  percent=$(expr $total_charge / $battery_number)

  echo $percent
}

get_battery_charging_status() {

  if $(acpi -b | grep --quiet Discharging); then
    echo "🔋"
  else # acpi can give Unknown or Charging if charging, https://unix.stackexchange.com/questions/203741/lenovo-t440s-battery-status-unknown-but-charging
    echo "🔌"
  fi
}

print_bat() {
  #hash acpi || return 0
  #onl="$(grep "on-line" <(acpi -V))"
  #charge="$(awk '{ sum += $1 } END { print sum }' /sys/class/power_supply/BAT*/capacity)%"
  #if test -z "$onl"
  #then
  ## suspend when we close the lid
  ##systemctl --user stop inhibit-lid-sleep-on-battery.service
  #echo -e "${charge}"
  #else
  ## On mains! no need to suspend
  ##systemctl --user start inhibit-lid-sleep-on-battery.service
  #echo -e "${charge}"
  #fi
  #echo "$(get_battery_charging_status) $(get_battery_combined_percent)%, $(get_time_until_charged )";
  echo "$(get_battery_charging_status)$(get_battery_combined_percent)%"
}

print_date() {
  #echo '📆 '; date '+%Y-%m-%d | %H:%M'
  # printf "📆 %s" "$(date "+%a %y-%m-%d $%T")"
  # printf "\x03%s" "$(date "+[%a %y-%m-%d]——[%T]")"
  echo -e "\x03$(date '+[%a %y-%m-%d]\x01——\x03[%T]')"
}

show_record() {
  test -f /tmp/r2d2 || return
  rp=$(cat /tmp/r2d2 | awk '{print $2}')
  size=$(du -h $rp | awk '{print $1}')
  echo " $size $(basename $rp) "
}

dwm_alsa() {
  VOL=$(amixer get Master | tail -n1 | sed -r "s/.*\[(.*)%\].*/\1/")
  printf "%s" "$SEP1"
  if [ "$IDENTIFIER" = "unicode" ]; then
    if [ "$VOL" -eq 0 ]; then
      printf "🔇"
    elif [ "$VOL" -gt 0 ] && [ "$VOL" -le 33 ]; then
      printf "🔈 %s%%" "$VOL"
    elif [ "$VOL" -gt 33 ] && [ "$VOL" -le 66 ]; then
      printf "🔉 %s%%" "$VOL"
    else
      printf "🔊 %s%%" "$VOL"
    fi
  else
    if [ "$VOL" -eq 0 ]; then
      printf "MUTE"
    elif [ "$VOL" -gt 0 ] && [ "$VOL" -le 33 ]; then
      printf "VOL %s%%" "$VOL"
    elif [ "$VOL" -gt 33 ] && [ "$VOL" -le 66 ]; then
      printf "VOL %s%%" "$VOL"
    else
      printf "VOL %s%%" "$VOL"
    fi
  fi
  printf "%s\n" "$SEP2"
}

LOC=$(readlink -f "$0")
DIR=$(dirname "$LOC")
export IDENTIFIER="unicode"

#. "$DIR/dwmbar-functions/dwm_transmission.sh"
#. "$DIR/dwmbar-functions/dwm_cmus.sh"
#. "$DIR/dwmbar-functions/dwm_resources.sh"
#. "$DIR/dwmbar-functions/dwm_battery.sh"
#. "$DIR/dwmbar-functions/dwm_mail.sh"
#. "$DIR/dwmbar-functions/dwm_backlight.sh"
#. "$DIR/dwmbar-functions/dwm_alsa.sh"
#. "$DIR/dwmbar-functions/dwm_pulse.sh"
#. "$DIR/dwmbar-functions/dwm_weather.sh"
#. "$DIR/dwmbar-functions/dwm_vpn.sh"
#. "$DIR/dwmbar-functions/dwm_network.sh"
#. "$DIR/dwmbar-functions/dwm_keyboard.sh"
#. "$DIR/dwmbar-functions/dwm_ccurse.sh"
#. "$DIR/dwmbar-functions/dwm_date.sh"

#get_bytes
# Calculates speeds
#vel_recv=$(get_velocity $received_bytes $old_received_bytes $now)
#vel_trans=$(get_velocity $transmitted_bytes $old_transmitted_bytes $now)

#xsetroot -name " 💿$(print_mem)G | $(dwm_network) ⬇️ $vel_recv ⬆️ $vel_trans $(dwm_alsa) [$(print_bat)]$(show_record) $(print_date) "

# xsetroot -name " $(print_mem)$(print_space)$(print_date)"
xsetroot -name "$(print_network)$(print_dash)$(print_mem)$(print_dash)$(print_date)"
# xsetroot -name "$(print_mem)$(print_date)"

# Update old values to perform new calculations
#old_received_bytes=$received_bytes
#old_transmitted_bytes=$transmitted_bytes
#old_time=$now

exit 0
