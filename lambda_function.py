import json
import boto3
import logging
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("Lambda function started")
    
    secrets_client = boto3.client('secretsmanager')
    s3_client = boto3.client('s3')

    secret_id = 'MySecret'  # Your secret name
    bucket_name = 'my-unique-bucket-name-cfpractask-jun'  # Your bucket name
    
    logger.info(f"Attempting to retrieve secret: {secret_id}")
    logger.info(f"Attempting to access S3 bucket: {bucket_name}")

    try:
        # Get secret value
        logger.info("Calling Secrets Manager...")
        secret_response = secrets_client.get_secret_value(SecretId=secret_id)
        logger.info("Successfully retrieved secret from Secrets Manager")
        
        secret_string = secret_response.get('SecretString')
        secret = json.loads(secret_string) if secret_string else {}
        logger.info(f"Secret parsed successfully. Username: {secret.get('username', 'N/A')}")

        # List objects in the S3 bucket
        logger.info("Calling S3 list_objects_v2...")
        s3_response = s3_client.list_objects_v2(Bucket=bucket_name)
        logger.info("Successfully retrieved S3 objects list")
        
        s3_objects = [obj['Key'] for obj in s3_response.get('Contents', [])]
        logger.info(f"Found {len(s3_objects)} objects in S3 bucket")
        
        response_data = {
            'message': 'Success',
            'secret': secret.get('username'),
            's3Objects': s3_objects
        }
        
        logger.info("Lambda function completed successfully")
        return {
            'statusCode': 200,
            'body': json.dumps(response_data)
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"AWS ClientError occurred: {error_code} - {error_message}")
        logger.error(f"Full error details: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'AWS Client Error',
                'errorCode': error_code,
                'errorMessage': error_message
            })
        }
    
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Unexpected Error',
                'error': str(e),
                'errorType': type(e).__name__
            })
        }
    
    finally:
        logger.info("Lambda function execution completed")
