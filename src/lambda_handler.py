import boto3
from web_parser import parse_html
import dynamo_helpers
from helpers import get_raw_html

def handler(event, context):
    client = boto3.client('dynamodb')
    resource = boto3.resource('dynamodb')
    dynamo_helpers.create_tables(client)
    
    data = parse_html(get_raw_html('https://sites.google.com/alaska.edu/coronavirus/uaf/dashboard'))
    if data is not None:
        dynamo_helpers.add_case_count(resource, data['cumulative_cases'])
    
