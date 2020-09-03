import os
import boto3
from datetime import datetime, timezone, timedelta

def create_boto_session(aws_access_key=None, aws_secret_key=None, aws_region=None):
    if aws_access_key is not None and aws_secret_key is not None:    
        return boto3.Session(aws_access_key_id=aws_access_key,
                             aws_secret_access_key=aws_secret_key,
                             region_name=aws_region)
    return None

def create_dynamo_client(aws_access_key=None, aws_secret_key=None, aws_region=None):
        local_dynamo = os.getenv('BOTO_DEV',None)
        session = create_boto_session(aws_access_key=aws_access_key,
                                      aws_secret_key=aws_access_key,
                                      aws_region=aws_region)
        if bool(local_dynamo):
            client = session.client('dynamodb', endpoint_url='http://localhost:8000')
            resource = session.resource('dynamodb', endpoint_url='http://localhost:8000')
        return client, resource

def create_tables(dynamo_client):
    existing_tables = dynamo_client.list_tables()
    cases_table = { }
    cases_table['TableName'] = 'UAF_cases'
    cases_table['BillingMode'] = 'PAY_PER_REQUEST'
    cases_table['AttributeDefinitions'] = [
        {'AttributeName':'timestamp', 'AttributeType':'S'}
    ]
    cases_table['KeySchema'] = [
        {'AttributeName':'timestamp', 'KeyType':'HASH'}
    ]
    if 'UAF_cases' not in existing_tables['TableNames']:
        dynamo_client.create_table(AttributeDefinitions=cases_table['AttributeDefinitions'],
                                   TableName=cases_table['TableName'], BillingMode=cases_table['BillingMode'],
                                   KeySchema=cases_table['KeySchema'])

def add_case_count(resource, cumulative_cases):
    current_datetime = datetime.now(tz=timezone.utc)
    date = str(current_datetime.date())
    cases_table = resource.Table('UAF_cases')
    yesterday = current_datetime - timedelta(days=1)
    yesterday = str(yesterday.date())
    yesterday_results = cases_table.get_item(Key={'timestamp':yesterday})
    yesterday_exists = True
    try:
        cumulative_yesterday = yesterday_results['Item']['cumulative_cases']
    except KeyError:
        yesterday_exists = False
    new_case_entry = {
        'timestamp': date,
        'cumulative_cases': cumulative_cases
    }
    if yesterday_exists:
        new_case_entry['new_cases'] = str(int(cumulative_cases) - int(cumulative_yesterday))
    cases_table.put_item(Item=new_case_entry)
