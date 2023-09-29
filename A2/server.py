import grpc
import computeandstorage_pb2
import computeandstorage_pb2_grpc
import boto3
from concurrent import futures
from urllib.parse import urlparse

class EC2OperationsServicer(computeandstorage_pb2_grpc.EC2OperationsServicer):
    #the below line of code from lines 11-17 has been referred from the below source and has been modified to include aws_session_token.
    #Source: https://stackoverflow.com/questions/45981950/how-to-specify-credentials-when-connecting-to-boto3-s3
    s3 = boto3.client(
        's3',
        aws_access_key_id="",
        aws_secret_access_key="",
        
aws_session_token=""
    )
    s3storage = 'a2-bucket-grpc'
    text = 'welcome.txt'
    def StoreData(self, request, context):

        text_requested = request.data
        #the below line of code from lines 26-30 has been referred from the below source.
        #Source: https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3

        self.s3.put_object(
            Body=text_requested,
            Bucket=self.s3storage,
            Key=self.text
        )

        s3_uri = f'https://s3.amazonaws.com/{self.s3storage}/{self.text}'

        return computeandstorage_pb2.StoreReply(s3uri=s3_uri)

    def AppendData(self, request, context):
        text_requested = request.data

        response = self.s3.get_object(Bucket=self.s3storage, Key=self.text)
        body_response = response['Body'] 
        current_data = ""
        for chunk in body_response.iter_chunks():
            current_data += chunk.decode('utf-8')
        new_data = self.mergetext(text_requested, current_data)

        #the below line of code from lines 48-52 has been referred from the below source.
        #Source: https://stackoverflow.com/questions/40336918/how-to-write-a-file-or-data-to-an-s3-object-using-boto3
        self.s3.put_object(
            Body=new_data,
            Bucket=self.s3storage,
            Key=self.text
        )
        return computeandstorage_pb2.AppendReply()

    def mergetext(self, data, existing_data):
        text_new = ''.join([existing_data, data])        
        return text_new

    def DeleteFile(self, request, context):
        s3_uri = request.s3uri
        updated_text = self.textname(s3_uri)

        #the below line of code in line 66 has been referred from the below source.
        #Source: https://stackoverflow.com/questions/3140779/how-to-delete-files-from-amazon-s3-bucket

        self.s3.delete_object(Bucket=self.s3storage, Key=updated_text)
        return computeandstorage_pb2.DeleteReply()

    def textname(self, s3_uri):
        updated_text = ""
        # the below lines of code from 73-75 has been referred from the below source.
        # Source: https://docs.python.org/3/library/urllib.parse.html
        uri_file_path = urlparse(s3_uri)
        location_file = uri_file_path.path
        updated_text = location_file.rsplit('/', 1)[-1]
        return updated_text


#the below code from lines 80-86 has been taken from [Source:] https://grpc.io/docs/languages/python/basics/ .
def serve():
    grpc_instance = grpc.server(futures.ThreadPoolExecutor())
    computeandstorage_pb2_grpc.add_EC2OperationsServicer_to_server(
        EC2OperationsServicer(), grpc_instance)
    grpc_instance.add_insecure_port('[::]:50051')
    grpc_instance.start()
    grpc_instance.wait_for_termination()

if __name__ == '__main__':
    serve()



