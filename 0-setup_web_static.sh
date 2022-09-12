#!/usr/bin/env bash
# Script that sets up your web servers for the deployment of web_static

# Install Nginx if it not already installed
sudo apt -y update
sudo apt -y upgrade
sudo apt -y install nginx
# Create the folders
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
# Create a fake HTML file
    echo "<html>
    <head>
    </head>
    <body>
        Holberton School
    </body>
    </html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
# Create a symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
# Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/
# Update the Nginx configuration to serve the content
sudo sed -i '48i \\tlocation /hbnb_static {\n\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
# Restart Nginx
sudo service nginx restart
