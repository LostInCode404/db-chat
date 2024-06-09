# Start from slim debian python image
FROM python:3.11.9-slim-bookworm

# Install python dependencies
COPY ./app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Setup app dir
RUN mkdir /app
WORKDIR /app
COPY ./app/*.py ./
COPY ./vector-db /app/vector-db

# Run app
CMD [ "streamlit", "run", "main.py" ]
