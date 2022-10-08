# rachiout
A simple python application to purge water from a rachio controlled irrigation system using a small home air compressor

**_Warnings!_** 
- Using excessive pressure to purge an irrigation system can cause damage. Make sure that you understand the limits of your system.  
- Failing to fully purge your system increases the risk of freeze damage.  Make sure to manually verify that your system is fully purged.  

**_I am not responsible for any damage caused to your system._**


To use this application, update `rachio.yml` with your rachio api token and the name of the rachio device for the system that you would like to purge.  You can find this name in your rachio mobile app.

then run `python main.py`

It will cycle through all of your device's enabled zones, running each zone for `blow-out-sec` seconds and then waiting for `compressor-recharge-delay-sec` for the compressor to recharge its air reservoir.  It will repeat this `repetitions` times.  Adjust these times to fit the characteristics of your compressor and irrigation system.