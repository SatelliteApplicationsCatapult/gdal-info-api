FROM osgeo/gdal:ubuntu-full-latest

# install pip
RUN apt-get update && apt-get install -y python3-pip
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
ENV IN_GDAL_DOCKER true
COPY . /app
# run main with gunicon
CMD ["gunicorn", "-b", ":5000","--timeout","0", "main:app"] 