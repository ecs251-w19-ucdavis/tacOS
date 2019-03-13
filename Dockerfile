# Use an official Python runtime as a parent image
FROM python:3.6-slim

RUN apt-get update &&\
    apt-get install -y curl
    # apt-get install -y net-tools &&\
    # apt-get install -y iputils-ping &&\
    # apt-get install -y procps &&\
    # apt-get install -y telnet

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src /app

RUN chmod +x ./taco

RUN mkdir ./test_files &&\
    curl http://www.effigis.com/wp-content/uploads/2015/02/DigitalGlobe_WorldView2_50cm_8bit_Pansharpened_RGB_DRA_Rome_Italy_2009DEC10_8bits_sub_r_1.jpg \
    -o ./test_files/satellite_image.jpg; exit 0

ENV PORT 8000

# Run app.py when the container launches
CMD ["python", "node.py"]
