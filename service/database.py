import json

import boto3
import datetime


with open("../config.json") as json_data:
    config = json.load(json_data)


class Dynamodb:
    def __init__(self):
        self.dynamo_db = boto3.resource(
            config["database"], region_name=config["region_name"],
            endpoint_url=config["endpoint_url"]
        )
        # boto3.set_stream_logger('botocore', level='DEBUG')
        client = boto3.client(
            config["database"], region_name=config["region_name"],
            endpoint_url=config["endpoint_url"]
        )
        try:
            client.describe_table(
                TableName=config["table_name"]
            )
        except client.exceptions.ResourceNotFoundException:
            self.dynamo_db.create_table(
                TableName=config["table_name"],
                KeySchema=[
                    {
                        'AttributeName': 'session_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'session_id',
                        'AttributeType': 'S'
                    },
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        self.table = self.dynamo_db.Table('user_session')

    def save_session(self, user_id, session_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = self.table.put_item(
            Item={
                'user_id': user_id,
                'session_id': session_id,
                'creation_date': current_time,
                'last_checked': current_time
            }
        )

    def get_item_by_session_id(self, session_id):
        pass

    def load(self, session_id):
        try:
            response = self.table.get_item(
                Key={
                    'session_id': session_id,
                }
            )
            item = response['Item']
            creation_date = item['creation_date']
            last_checked = item['last_checked']
            if self.check_session_creation(creation_date) and self.check_session_last_use(last_checked):
                self.update_last_check(session_id)
                return item['user_id']
            else:
                return None

        except KeyError:
            return None

    def renew(self, session_id):
        try:
            response = self.table.get_item(
                Key={
                    'session_id': session_id,
                }
            )
            item = response['Item']
            last_checked = item['last_checked']
            if self.check_session_last_use(last_checked):
                self.update_last_check(session_id)
                return True
            else:
                return False

        except KeyError:
            return False

    def update_last_check(self, session_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.table.update_item(
            Key={
                'session_id': session_id
            },
            UpdateExpression="set last_checked = :lc",
            ExpressionAttributeValues={
                ':lc': current_time
            },
            ReturnValues="UPDATED_NEW"
        )

    def delete(self, session_id):
        try:
            response = self.table.get_item(
                Key={
                    'session_id': session_id,
                }
            )
            item = response['Item']['session_id']

            self.table.delete_item(
                Key={
                    'session_id': session_id
                }
            )
        except KeyError:
            return False
        else:
            return True

    def check_session_creation(self, creation_time):
        session_expiry_time = datetime.datetime.now() - datetime.timedelta()
        return creation_time > session_expiry_time.strftime('%Y-%m-%d %H:%M:%S')

    def check_session_last_use(self, last_used):
        five_minutes_before_date_time = datetime.datetime.now() - datetime.timedelta(minutes=config["last_check_timer"])
        return last_used > five_minutes_before_date_time.strftime('%Y-%m-%d %H:%M:%S')
