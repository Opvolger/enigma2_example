https://github.com/technic/enigma2
https://github.com/technic/enigma2_example
https://github.com/OpenPLi/enigma2-plugins/blob/74a4d3e8438557cb1fc68630ced1e05e1c038ef2/zdfmediathek/src/plugin.py

opkg install hlsdl
opkg install gstreamer1.0-plugins-good-rtsp

doet te veel, disk vol
opkg install gstreamer1.0-plugi*


scp src/plugin.py root@192.168.2.55:/usr/lib/enigma2/python/Plugins/Extensions/Example/

gst-play-1.0 url

[opvolger@opvolger ~]$ export GST_DEBUG="*:3"
[opvolger@opvolger ~]$ gst-play-1.0 http://manifest.us.rtl.nl/rtlxl/v166/network/pc/adaptive/components/videorecorder/42/426250/426308/5cf65d84-a494-3f1c-adc7-60a9c1aaeff3.ssm/5cf65d84-a494-3f1c-adc7-

Certificaat is verlopen van rtlxl

date +%Y%m%d -s "2020-04-03"

https://github.com/GStreamer/gst-plugins-good/blob/master/ext/soup/gstsouphttpsrc.c

regel 130 naar FALSE (voor rtlxl)