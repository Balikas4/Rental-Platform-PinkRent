# PinkRent: Your Sustainable Item Rental Platform

## HOW TO RUN

Assuming you are running on a Virtual Private Server Linux based. Note it should have docker. <br>

Clone git:
`git clone https://github.com/Balikas4/Rental-Platform-PinkRent.git`<br>
Go into directory
`cd Rental-Platform-PinkRent`<br>
Install venv if not present
`apt install python3.10-venv`<br>
Crete venv and activate
`python3 -m venv venv`<br>
`source venv/bin/activate`<br>
Install requirements
`pip install -r requirements.txt` <br>
Add local_settings.py with your password and save. this file should be next to settings.py
`cd PinkRent/`<br>
`nano local_settings.py` or `vim local_settings.py`<br>
`SECRET_KEY = your_django_key`<br>
Add your domain to settings.py allowed hosts
`ALLOWED_HOSTS = ['localhost', 'postgres', 'your_domain']`<br>
Change your database host from postgres to VPS IP adress:
`'HOST': 'postgres',` to `'HOST': 'vps_ip',`<br>
Create admin superuser
`./manage.py createsuperuser`<br>
Run docker compose
`docker-compose up -d`<br>

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

Currently running on VPS domain www.pinkrent.lt

Happy renting!
