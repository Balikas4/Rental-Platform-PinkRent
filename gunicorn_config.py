bind = '172.17.0.1:8000'  # Replace with your desired host and port
workers = 3  # Adjust based on your server's resources
pythonpath = '/app/PinkRent'  # Replace with the absolute path to your Django project
module = 'PinkRent.wsgi'  # Replace with the module containing your WSGI application

certfile = "/etc/letsencrypt/live/www.pinkpink.lt/fullchain.pem"
keyfile = "/etc/letsencrypt/live/www.pinkpink.lt/privkey.pem"