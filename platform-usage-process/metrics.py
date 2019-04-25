from datetime import datetime as dt

from repository import Repository


class Metrics:
    def __init__(self, net_id):
        self.net_id = net_id
        self.repo = Repository(net_id)

    def handle_request_type(self, params):
        try:
            insrt_dm_rq_sts = "INSERT INTO daemon_request_stats (ethereum_json_rpc_endpoint, group_id, input_data_size, " \
                              "organization_id, registry_address_key, request_id, request_received_time, service_id, " \
                              "service_method, row_created, row_updated) " \
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            dm_req_params = (params['ethereum_json_rpc_endpoint'], params['group_id'], params['input_data_size'],
                       params['organization_id'], params['registry_address_key'], params['request_id'],
                       params['request_received_time'][:19], params['service_id'], params['service_method'],
                       dt.utcnow(),
                       dt.utcnow())
            self.repo.execute(insrt_dm_rq_sts, dm_req_params)
        except Exception as e:
            print(repr(e))
            raise e

    def handle_response_type(self, params):
        try:
            insrt_dm_rs_sts = "INSERT INTO daemon_response_stats (error_message, ethereum_json_rpc_endpoint, group_id, " \
                              "organization_id, registry_address_key, request_id, request_received_time, response_code, " \
                              "response_sent_time, response_time, service_id, service_method, row_created, row_updated) " \
                              "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            dm_rs_params = (params['error_message'], params['ethereum_json_rpc_endpoint'], params['group_id'],
                            params['organization_id'], params['registry_address_key'], params['request_id'],
                            params['request_received_time'][:19], params['response_code'], params['response_sent_time'][:19],
                            params['response_time'], params['service_id'], params['service_method'], dt.utcnow(),
                            dt.utcnow())
            self.repo.execute(insrt_dm_rs_sts, dm_rs_params)
        except Exception as e:
            print(repr(e))
            raise e
