# feh --bg-fill ~/Pictures/wallpapers/grave.jpg
# compton -b
xfce4-power-manager &
bash ~/scripts/status-refresh.sh &
xset s 0
xset dpms 0 0 0
fcitx5 &
./tap_to_click.sh
./setxkbmap-qwery.sh
#xsetroot -name "vegeta"

