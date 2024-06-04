# PinkRent: Your Sustainable Item Rental Platform

## HOW TO RUN

Assuming you are running on a Virtual Private Server Linux based. Note it should have docker. Also you have made your domain A tags to redirect to your VPS. <br>

Clone git:<br>
`git clone https://github.com/Balikas4/Rental-Platform-PinkRent.git`<br>
Go into directory<br>
`cd Rental-Platform-PinkRent`<br>
Install venv, activate<br>
`apt install python3.10-venv`<br>
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
Install requirements<br>
`pip install -r requirements.txt`<br>
Add local_settings.py with your dajngo and postgres password and save. this file should be next to settings.py<br>
`cd PinkRent/PinkRent/`<br>
`nano local_settings.py` or `vim local_settings.py`<br>
```python
SECRET_KEY = your_django_key
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'your_database_host',
        'PORT': 'your_database_port',
    }
}
```
Edit docker-compose.yml with your postgres credentials, it should be same as DATABASES in local_settings.py: <br>
`POSTGRES_PASSWORD: postgres_password`<br>
Add your domain to settings.py allowed hosts. Check for debug to be FALSE<br>
`ALLOWED_HOSTS = ['localhost', 'postgres', 'your_domain.com', 'www.your_domain.com']`<br>
`DEBUG=False`<br>
Install certbot-nginx for SSL HTTPS secure connection and run trough configuration.<br>
`sudo apt install certbot python3-certbot-nginx`<br>
`sudo certbot --nginx`<br>
`sudo systemctl stop nginx`<br>
Navigate to manage.py and check for migrations<br>
`./manage.py migrate`<br>
Run docker compose<br>
`docker-compose up -d`<br>
Create django admin superuser inside docker<br>
`docker exec -it project.dev bash`<br>
`./manage.py createsuperuser`<br>
Populate db trough website admin or following json file:<br>
`./manage.py loaddata fixtures/initial_data.json`

## Overview

Welcome to PinkRent, your premier platform for item rental. Our mission is to simplify your life by offering a convenient space where users can easily rent the items they need for a short period. We believe in the power of sharing resources to save both money and the environment.

## Platform Features

### 1. User and admin accounts

PinkRent provides a structure for platfrom to manage on different levels.

### 2. User-Friendly Experience

Our platform is designed to be user-friendly, making it easy for users to browse, select, and rent items hassle-free.

### 3. Sustainability

We are committed to promoting a sustainable lifestyle by encouraging the sharing of resources. Renting items reduces waste and contributes to a more eco-friendly way of living.

## How It Works

1. **Register and browse:** Explore our catalog of items available for rent.

2. **Lend & Rent:** Choose the items you need and proceed with the offer process. Or Lend your own items.

3. **Community Sharing:** Join a community of like-minded individuals who believe in the power of sharing resources.

## Why PinkRent?

- **Cost-Effective:** Save money by renting items instead of purchasing them for short-term use.

- **Environmental Impact:** Contribute to a greener planet by participating in a sharing economy.

- **Community Building:** Connect with others who share a similar mindset about sustainability and responsible consumption.

## Future Enhancements

We are continuously working to enhance the PinkRent experience. Future updates may include:

- **Expanded Catalog Filters** Update our catalog with a wider range of filters to meet diverse needs.

- **Partners :** Create partner account and offer renting service for renters.

- **UI UX :** Change the way website looks.

## Join PinkRent Today!

Embrace a more sustainable and cost-effective lifestyle by joining PinkRent. Browse our catalog, rent items, and be part of a community that values sharing and environmental responsibility.

Currently running on VPS domain www.pinkpink.lt

Happy renting!
