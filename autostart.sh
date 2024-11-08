# feh --bg-fill ~/Pictures/wallpapers/grave.jpg
# compton -b
xfce4-power-manager &
bash ~/scripts/tap_to_click.sh
bash ~/scripts/setxkbmap-qwery.sh
xset s 0
xset dpms 0 0 0
bash ~/scripts/status-refresh.sh &
fcitx5 &
#xsetroot -name "vegeta"
