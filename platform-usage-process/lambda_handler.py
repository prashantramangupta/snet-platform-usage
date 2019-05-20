import json

from metrics import Metrics
from register import Token
from utils import Utils

obj_util = Utils()


def request_handler(event, context):
    if 'path' not in event:
        return get_response("400", {"status": "failed",
                                    "error": "Bad Request"})
    try:
        data = None
        payload_dict = None
        path = event['path'].lower()
        payload_dict = payload_check(payload=event['body'], path=path)
        if "/register" == path:
            token_instance = Token()
            data = token_instance.process_token(daemon_id=payload_dict['daemonId'])
        elif "/event" == path:
            obj_metrics = Metrics()
            if payload_dict['type'] == 'request':
                obj_metrics.handle_request_type(payload_dict)
            elif payload_dict['type'] == 'response':
                obj_metrics.handle_response_type(payload_dict)
            data = {}
        else:
            return get_response(500, "Invalid URL path.")

        if data is None:
            response = get_response("400", {"status": "failed",
                                            "error": "Bad Request",
                                            "api": event['path'],
                                            "payload": payload_dict})
        else:
            if data.get('error', '') == '':
                response = get_response("200", {"status": "success", "data": data})
            else:
                error = data['error']
                data.pop('error')
                response = get_response("200", {"status": "failed", "data": data, "error": error})

        return response
    except Exception as e:
        err_msg = {"status": "failed",
                   "error": repr(e),
                   "api": event['path'],
                   "payload": payload_dict,
                   "type": "process"}
        obj_util.report_slack(1, str(err_msg))
        return get_response(500, err_msg)


def payload_check(payload, path):
    payload_dict = None
    if payload is not None and len(payload) > 0:
        payload_dict = json.loads(payload)
    print("Processing [" + str(path) + "] with body [" + str(payload) + "]")
    return payload_dict


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
