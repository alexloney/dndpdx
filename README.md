# DnD PDX

## Raspberry Pi Setup
To begin with, this is intended to be ran from a Raspberry Pi, though it could be ran from anywhere else, but it's simplified enough that it can be used in this way.

Begin by doing a normal Raspberry Pi setup and installing Raspbian https://www.raspberrypi.org/downloads/raspbian/

Once Raspbian is installed, you may want to touch "ssh" on the "boot" drive to have SSH automatically enabled, unless you have the hardware to connect a monitor/keyboard/mouse to the Pi and enable SSH yourself. The default username/password is pi:raspberry.

Once Raspbian is installed an you can SSH into the Pi, follow these directions for turning the Pi into an AP that may be accessed. https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md

Follow these directions to add a domain name in dnsmasq.conf.add: https://github.com/RMerl/asuswrt-merlin/wiki/Custom-domains-with-dnsmasq

Follow these directions to set up an Nginx web server: https://www.raspberrypi.org/documentation/remote-access/web-server/nginx.md

Follow these directions to set up a Lets Encrypt SSL certificate: https://certbot.eff.org/lets-encrypt/debianbuster-nginx

### API setup

To get the API portion set up in a more production-ready state, follow these directions: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

### App Setup
In order to get the Angular App to work correctly, I had to use yarn as npm kept giving an error message looking for a "semver" package (even when just executing npm -v), so I installed yarn https://yarnpkg.com/en/docs/install#debian-stable

test update...