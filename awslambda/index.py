
__author__  = "venkaatprasads@gmail.com"
__version__ = "1.0"

import boto3

class Govtech():
    def __init__(self):
        pass

    def run(self):
        print("Hello GovTech!")

def handler(event, context):
    """
    handler(). parses sys arguments for execution
    :param: event
    :param: context
    :return: None
    """

    gov = Govtech()
    gov.run()

    return {
        'statusCode': 200,
        'body': 'Successful!'
    }