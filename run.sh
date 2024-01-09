#!/bin/bash

#Install playwright dependencies
sudo apt-get update
sudo apt-get install -y libicu66 libevent-2.1-7 libjpeg8 enchant libsecret-1-0 libffi7 libgles2

#Before starting the server, make sure you have the playwright browser installed
playwright install

#This command will start the server
gunicorn app:app