# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr && \
    apt-get install -y libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Set the TESSDATA_PREFIX environment variable
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/

ADD https://github.com/tesseract-ocr/tessdata_best/jpn.traineddata /usr/share/tesseract-ocr/jpn.traineddata
ADD https://github.com/tesseract-ocr/tessdata_best/jpn_vert.traineddata /usr/share/tesseract-ocr/jpn_vert.traineddata

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]