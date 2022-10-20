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
    try:
        result = subprocess.run(command + filePath, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        error = result.stderr.decode('utf-8')
        if error:
            if "ERROR 1" in error:
                return json.dumps({"error": "File not found"}), 404
            else:
                return json.dumps({"error": error}), 400
        # print("Error: ", result.stderr.decode('utf-8'))
        # print("Output: ", result.stdout.decode('utf-8'))
        return json.loads(result.stdout.decode('utf-8'))
    except json.decoder.JSONDecodeError as e:
        return {'error': "File you are pointing to might not exist or is not a valid file."}, 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7002)
