import os
import json
import boto3
import pandas as pd


def lambda_handler(event, context):

    S3_folder = os.environ["S3BUCKET"]
    final_file_obj = os.environ["S3OBJECT"]

    notification = json.loads(event["Records"][0]["Sns"]["Message"])["JobId"]

    record_number = data_extract(notification)

    download_file = "download.csv"
    pandas = pd.DataFrame(record_number.items())
    pandas.columns = ["PageNo", "Text"]
    pandas.to_csv(f"/tmp/{download_file}", index=False)

    folder = boto3.client("s3")
    folder_filename = f"/tmp/{download_file}"
    folder_key = f"{final_file_obj}/{download_file}"
    folder.upload_file(Filename=folder_filename, Bucket=S3_folder, Key=folder_key)
    return {"statusCode": 200, "body": json.dumps("File uploaded !")}


def data_extract(notification):
    aws_object = boto3.client("textract")

    output = {}
    records = []

    output = aws_object.get_document_text_detection(JobId=notification)
    records.append(output)

    other_data = None
    if "NextToken" in output:
        other_data = output["NextToken"]

    return get_row_number(aws_object, notification, other_data, records)


def get_row_number(aws_object, notification, other_data, records):
    while other_data:
        output = aws_object.get_document_text_detection(
            JobId=notification, NextToken=other_data
        )
        records.append(output)
        other_data = None
        if "NextToken" in output:
            other_data = output["NextToken"]
    row_number = {}

    i=0
    while i < len(records):
        j = 0
        row = records[i]
        while j < len(row["Blocks"]):
            if subjects["BlockType"] == "LINE":
                    row_number[subjects["Page"]].append(subjects["Text"])
            j += 1
        i += 1

    return row_number


