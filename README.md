# mechanical-pi-clock
![alt text](https://engineezy.com/cdn/shop/files/IMG_5888_1296x.jpg?raw=true)
(Image Credit Engineezy)

Source project file can be found here<br>
https://engineezy.com/products/the-rack-driven-7-segment-display?srsltid=AfmBOor7DwWkmcx2m0xCc8R6lovWsb5iA31NzDGzMK4fqotRGdzzudYv

Required Hardware:<br>
Raspberry Pi<br>
Adafruit servo hat<br>
https://www.adafruit.com/product/3416?srsltid=AfmBOork7eebJPQc8EZTlTusntxE3_w2fnc24dvU2uT_JZLvEPRV1yyn

Required Python Packages for sound (Optional):<br>
playsound

Auto start steps:<br>
Add the following line to the end of your .bashrc file. There are more elegant ways to start a python script on boot but I've found only this .bashrc method works the the sound. Feel free to use another method if not using sound.<br>
bash ~/clock_code/autolauncher.sh &<br>
This will autostart the python script in the background however you setup the autolauncher script