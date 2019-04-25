from repository import Repository


class Token:
    def __init__(self, net_id):
        self.net_id = net_id
        self.repo = Repository(net_id)

    def validate_token(self, daemon_id, token):
        print("validate_token::daemon_id: ", daemon_id);
        qry = "SELECT * FROM daemon_token WHERE daemon_id = %s and token = %s "
        res = self.repo.execute(qry, [daemon_id, token])
        if len(res) > 0:
            return {'validated': True}
        return {'validated': False}