from flask import Flask, request
import shutil
from botocore.config import Config
import boto3
from PIL import Image
import torch
import json
from flask_cors import CORS

import os

AWS_ACCESS_KEY = 'AKIA3PPYK5BMEPHVRAXP'
AWS_SECRET_ACCESS = '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'

app = Flask(__name__)

CORS(app)
# Helper functions


@app.route("/")
def index():
    return "connected"

# def get_yolov5():
#     # local best.pt
#     model = torch.hub.load('ultralytics/yolov5', 'custom', './model/best.pt', 'local')  # local repo
#     model.conf = 0.5
#     return model
#
#
# model = get_yolov5()

#
# def downloadFromS3(bucket_name, k, path_to_store):
#     my_config = Config(region_name='ap-south-1')
#     # Let's use Amazon S3
#     s3 = boto3.resource("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
#                         aws_secret_access_key=AWS_SECRET_ACCESS)
#     # Print out bucket names
#     s3 = boto3.client("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS)
#     s3.download_file(Bucket=bucket_name, Key=k, Filename=path_to_store)

#
# def uploadToS3File(bucket_name, file_path, k):
#     my_config = Config(region_name='ap-south-1')
#     # Let's use Amazon S3
#     s3 = boto3.resource("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
#                         aws_secret_access_key=AWS_SECRET_ACCESS)
#     # Print out bucket names
#     s3 = boto3.client("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS)
#     s3.upload_file(
#         Filename=file_path,
#         Bucket=bucket_name,
#         Key=k
#     )


@app.route("/predict")
def predict():
    try:
        try:
            shutil.rmtree("./images/labeled")
        except:
            pass
        req = request.get_json()
        imageName = req["image"]
        filename = "./images/rawImages/" + imageName

        my_config = Config(region_name='ap-south-1')
        # Let's use Amazon S3
        s3 = boto3.resource("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_ACCESS)
        # Print out bucket names
        s3 = boto3.client("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS)
        s3.download_file(Bucket="property-images-bucket", Key=imageName, Filename=filename)




        image_obj = Image.open(filename)

        model = torch.hub.load('ultralytics/yolov5', 'custom', './model/best.pt', 'local')  # local repo
        model.conf = 0.5
        results = model(image_obj)
        detect_res = results.pandas().xyxy[0].to_json(orient="records")
        detect_res = json.loads(detect_res)
        results.save(save_dir="./images/labeled")

        labeled_filename = "./images/labeled/" + imageName

        my_config = Config(region_name='ap-south-1')
        # Let's use Amazon S3
        s3 = boto3.resource("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_ACCESS)
        # Print out bucket names
        s3 = boto3.client("s3", config=my_config, aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_SECRET_ACCESS)
        s3.upload_file(
            Filename=labeled_filename,
            Bucket="property-images-detection-bucket",
            Key=imageName
        )






        return {"predict": detect_res, "filename": imageName, "completed": True}

    except:
        return {"predict": [], "filename": "", "completed": False, "message": "Unable to predict the given image"}


if __name__ == '__app__':
    app.run(host="0.0.0.0", port=5002, debug=False)