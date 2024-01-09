#!/bin/bash

#Before starting the server, make sure you have the playwright browser installed
playwright install

#This command will start the server
gunicorn app:app