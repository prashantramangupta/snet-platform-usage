import json
import os

from authorizer import Token
from constant import METRICS_NETWORK_ID


def request_handler(event, context):
    if 'path' not in event:
        return get_response("400", {"status": "failed", "error": "Bad Request"})
    try:
        path = event['path'].lower()
        data = None
        if "/events" == path:
            try:
                payload_dict = event['headers']
                print("Processing [" + str(path) + "] with body [" + str(payload_dict) + "]")
                net_id = METRICS_NETWORK_ID
                token_instance = Token(net_id)
                data = token_instance.validate_token(daemon_id=payload_dict['x-daemonid'],
                                                     token=payload_dict['x-token'])
                response = get_lambda_authorizer_response_format(event=event, allow=data['validated'])
            except Exception as e:
                print(repr(e))
                response = get_lambda_authorizer_response_format(event=event, allow=False)


    except Exception as e:
        response = get_response(500, {"status": "failed",
                                      "error": repr(e)})

    return response


# Generate response JSON that API gateway expects from the lambda function
def get_response(status_code, message):
    return {
        'statusCode': status_code,
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
            "X-Requested-With": '*',
            "Access-Control-Allow-Headers": 'Access-Control-Allow-Origin, Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with',
            "Access-Control-Allow-Origin": '*',
            "Access-Control-Allow-Methods": 'GET,OPTIONS,POST'
        }
    }


def get_lambda_authorizer_response_format(event, allow):
    response = {
        "principalId": os.environ['principalId'],
        "policyDocument": {
            "Version": '2012-10-17',
            "Statement": [
                {
                    "Action": 'execute-api:Invoke',
                    "Resource": event['methodArn']
                }
            ]
        }
    }
    if allow:
        response["policyDocument"]["Statement"][0]["Effect"] = 'Allow'
    else:
        response["policyDocument"]["Statement"][0]["Effect"] = 'Deny'
    return response
