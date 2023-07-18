import boto3
import json
import hashlib
import psycopg2
import re


# Function to encode version numbers to integers
def encode_version(version):
    # If version is None, return a default value
    if version is None:
        return 999

    # Check invalid format
    if not re.match(r'\d+(\.\d+){2}', version):
        # Convert to string to avoid type issues
        version = str(round(float(version)))

    try:
        # Split version
        major, minor, patch = version.split(".")

        # Handle leading zeros
        major = major.zfill(2)
        minor = minor.zfill(2)
        patch = patch.zfill(2)

        # Convert to ints after splitting
        major = int(major)
        minor = int(minor)
        patch = int(patch)

        # Encode as integer
        major *= 1000
        minor *= 1000
        encoded = (major << 16) + (minor << 8) + patch

    except ValueError:
        return 0

    return encoded


# AWS SQS configurations
queue_url = 'http://localhost:4566/000000000000/login-queue'
sqs = boto3.client('sqs', region_name='us-east-2', endpoint_url=queue_url)

# PostgreSQL database configurations
pg_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

# Receive messages from the SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url,
    MaxNumberOfMessages=100,
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

# Check if there are messages in the response
if 'Messages' in response:
    message = response['Messages'][0]
    message_body = json.loads(message['Body'])
    print(message_body)
    user_id = message_body.get('user_id')
    device_type = message_body.get('device_type')
    locale = message_body.get('locale')
    app_version = message_body.get('app_version')

    # Encode the app_version to an integer
    app_version = encode_version(app_version)

    device_id = message_body.get('device_id', '19991')
    ip = message_body.get('ip', '0.0.0.0')

    # Hash the device_id and ip for masking
    masked_device_id = hashlib.md5(device_id.encode()).hexdigest()
    masked_ip = hashlib.md5(ip.encode()).hexdigest()

    # Create a new message body with masked device_id and ip
    masked_message_body = {**message_body, 'device_id': masked_device_id, 'ip': masked_ip}

    print(masked_ip)
    print(masked_message_body)
    print(app_version)

    # Connect to PostgreSQL database
    with psycopg2.connect(**pg_config) as conn:
        with conn.cursor() as cur:
            # Insert the record into the user_logins table
            insert_query = """ INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date)  VALUES (%s, %s, %s, %s, %s, %s, NOW());       """
            cur.execute(insert_query, (user_id, device_type, masked_ip, masked_device_id, locale, app_version))
            conn.commit()

    # Write the original message body to a JSON file
    with open('C:\\Users\\najmu\\OneDrive\\Desktop\\user_login_message.json', 'a') as file:
        json.dump(message_body, file)
        file.write('\n')

    # Delete the message from the queue after processing
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=message['ReceiptHandle']
    )
else:
    print('No messages in the queue')
