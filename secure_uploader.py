import boto3
import os

# AWS Config
s3 = boto3.client('s3')
kms_key_id = 'arn:aws:kms:us-east-1:783764573196:key/b26b33a6-3f76-44ba-a162-d2c46dc094dc'  
bucket_name = 'my-new-bucket-ib123'  

# Function to upload file with encryption
def upload_secure_file(file_path):
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=file_name,
            ExtraArgs={
                'ServerSideEncryption': 'aws:kms',
                'SSEKMSKeyId': kms_key_id
            }
        )
        print(f"{file_name} uploaded securely to {bucket_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Test the function
upload_secure_file("test.txt")

def is_object_public(bucket, key):
    try:
        acl = s3.get_object_acl(Bucket=bucket, Key=key)
        for grant in acl['Grants']:
            if 'URI' in grant['Grantee'] and 'AllUsers' in grant['Grantee']['URI']:
                return True
        return False
    except Exception as e:
        print(f" Error checking ACL: {e}")
        return False

def upload_secure_file(file_path):
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(
            Filename=file_path,
            Bucket=bucket_name,
            Key=file_name,
            ExtraArgs={
                'ServerSideEncryption': 'aws:kms',
                'SSEKMSKeyId': kms_key_id
            }
        )
        print(f"{file_name} uploaded securely to {bucket_name}")

        # Check for public access
        if is_object_public(bucket_name, file_name):
            print(f"WARNING: {file_name} is publicly accessible!")
        else:
            print(f" {file_name} is private (as expected)")

    except Exception as e:
        print(f"Error uploading file: {e}")
