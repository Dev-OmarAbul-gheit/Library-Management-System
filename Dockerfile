FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    # dependencies for building Python packages
    && apt-get install -y build-essential \
    # psycopg2 dependencies
    && apt-get install -y libpq-dev \
    # Translations dependencies
    && apt-get install -y gettext \
    # curl
    && apt-get install -y gdal-bin python3-gdal \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Create and set proper permissions for code directory
RUN mkdir /code

WORKDIR /code

# Install Python dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --cache-dir ~/.pip_cache -r /requirements.txt

# Copy entrypoint and start scripts
# COPY ./compose/local/start.sh /start.sh


# Fix line endings and make scripts executable
# RUN sed -i 's/\r$//g' /start.sh \
#     && chmod +x /start.sh

# Copy application code
COPY . /code/
# Run the application.
CMD  python manage.py runserver 0.0.0.0:8000