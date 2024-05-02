FROM python:3.10

# Install nano text editor
RUN apt-get update && apt-get install -y nano

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory in the Docker container
WORKDIR /app

# Copy the Django project files into the Docker container
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# COMMENTED BECAUSE docker-compose.yml 

# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate
# CMD ["gunicorn", "-b", "0.0.0.0:8000", "PinkRent.wsgi"]


# # Command to run the Django application
# CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
