import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    secrets_client = boto3.client('secretsmanager')
    s3_client = boto3.client('s3')

    secret_id = 'MySecret'  # Your secret name
    bucket_name = 'my-unique-bucket-name-cfpractask-jun'  # Your bucket name

    try:
        # Get secret value
        secret_response = secrets_client.get_secret_value(SecretId=secret_id)
        secret_string = secret_response.get('SecretString')
        secret = json.loads(secret_string) if secret_string else {}

        # List objects in the S3 bucket
        s3_response = s3_client.list_objects_v2(Bucket=bucket_name)
        s3_objects = [obj['Key'] for obj in s3_response.get('Contents', [])]

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Success',
                'secret': secret.get('username'),
                's3Objects': s3_objects
            })
        }

    except ClientError as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Failed',
                'error': str(e)
            })
        }

