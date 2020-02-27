# Pull base image
FROM python:3.7

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /petal

# Install dependencies
COPY Pipfile Pipfile.lock /petal/
RUN pip install pipenv && pipenv install --system
#
# mark a file as 'executable' since this is a linux container on a windows host
#RUN ["chmod", "+x", "executable.sh"]
#chmod +rwx manage.py

# Copy project
COPY . /petal/