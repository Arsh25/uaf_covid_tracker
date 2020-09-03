import os

from web_parser import parse_html
import dynamo_helpers
from helpers import get_raw_html


if __name__ == '__main__':
    os.environ['BOTO_DEV'] = 'true'
    client, resource = dynamo_helpers.create_dynamo_client(aws_access_key='fakekey', aws_secret_key='fakesecret',
                                  aws_region='us-west-2')
    dynamo_helpers.create_tables(client)
    print(client.list_tables())
    data = parse_html(get_raw_html('https://sites.google.com/alaska.edu/coronavirus/uaf/dashboard'))
    if data is not None:
        dynamo_helpers.add_case_count(resource, data['cumulative_cases'])
    cases_table = resource.Table('UAF_cases')
    print(cases_table.get_item(Key={'timestamp':'2020-09-01'}))


