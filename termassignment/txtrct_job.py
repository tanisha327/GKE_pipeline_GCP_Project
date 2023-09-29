import os
import json
import boto3
from urllib.parse import unquote_plus

intermediate_object = os.environ["S3Bucket"]
intermediate_file_name = os.environ["S3Object"]
notification_arn = os.environ["SNSTOPIC"]
notification_role = os.environ["SNSROLE"]


def lambda_handler(event, context):

    aws_object= boto3.client("textract")
    if event:
        document_rec = event["Records"][0]
        object_descrip = str(document_rec["s3"]["bucket"]["name"])
        key_name = unquote_plus(str(document_rec["s3"]["object"]["key"]))

        aws_return = doc_extraction(aws_object, key_name, object_descrip)
        return response_final(aws_return)

def response_final(aws_return):
    if aws_return["ResponseMetadata"]["HTTPStatusCode"] == 200:
        send_back = {
            "statusCode": 200
        }
        return send_back
    else:
        send_back = {
            "statusCode": 500
        }
        return send_back


def doc_extraction(aws_object, key_name, object_descrip):
    aws_return = aws_object.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": object_descrip, "Name": key_name}},
        OutputConfig={"S3Bucket": intermediate_object, "S3Prefix": intermediate_file_name},
        NotificationChannel={"SNSTopicArn": notification_arn, "RoleArn": notification_role},
    )
    return aws_return