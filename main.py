# create a flask app with hello world route
from flask import Flask, request
app = Flask(__name__)
import subprocess
import os
import json

IN_GDAL_DOCKER = os.environ.get('IN_GDAL_DOCKER', False)
command = """docker run --rm osgeo/gdal:ubuntu-full-latest gdalinfo -json """
if IN_GDAL_DOCKER:
    command = """gdalinfo -json """


@app.route('/', methods=['POST'])
def get_info():
    filePath = request.json['file_url']
    # call the gdalinfo command with the filePath
    result = subprocess.run(command + filePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # return the result as json response
    return json.loads(result.stdout)

if __name__ == '__main__':
    app.run()
