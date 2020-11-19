from flask import Flask, request, jsonify
import logging
import requests
import os

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

app = Flask(__name__)


def get_auth_token():
    data = {
        'grant_type': 'password',
        'username': os.environ.get('IDP_USERNAME'),
        'password': os.environ.get('IDP_PASSWORD'),
        'client_id': 'admin-cli'
    }

    response = requests.post('{}/protocol/openid-connect/token'.format(
        os.environ.get('IDP_MASTER_REALM_URL')), verify=tls_verify(), data=data)

    app.logger.info(response.json())

    return response.json()['access_token']


def tls_verify():
    if os.environ.get('IDP_VERIFY_TLS') == 'false':
        return False

    return True


def get_client(clientId):
    response = requests.get('{}/clients'.format(os.environ.get('IDP_ADMIN_REALM_URL')),
                            verify=tls_verify(),
                            headers={'Authorization': 'Bearer {}'.format(get_auth_token())})

    clients = response.json()
    
    for client in clients:
        app.logger.info(client)
        if client['clientId'] == clientId:
            app.logger.info(client['id'])
            return client

    return None


@app.route('/.well-known/openid-configuration', methods=['GET'])
def get_openid_configuration():
    response = requests.get('{}/.well-known/openid-configuration'.format(
        os.environ.get('IDP_REALM_URL')), verify=tls_verify())

    return response.json()


@app.route('/clients/<clientId>', methods=['PUT'])
def create_or_update(clientId):
    data = request.json

    new_or_updated_client = {
        'clientId': data['client_id'],
        'secret': data['client_secret'],
        'enabled': True,
        'publicClient': False
    }

    client = get_client(clientId)

    if client is not None:
        requests.put('{}/clients/{}'.format(os.environ.get('IDP_ADMIN_REALM_URL'),
                                            client['id']),
                                json=new_or_updated_client,
                                verify=tls_verify(),
                                headers={'Authorization': 'Bearer {}'.format(get_auth_token())})
        
    else:
        requests.post('{}/clients'.format(os.environ.get('IDP_ADMIN_REALM_URL')),
                      json=new_or_updated_client,
                      verify=tls_verify(),
                      headers={'Authorization': 'Bearer {}'.format(get_auth_token())})

    return jsonify(success=True)


@app.route('/clients/<clientId>', methods=['DELETE'])
def delete(clientId):
    client = get_client(clientId)

    requests.delete('{}/clients/{}'.format(os.environ.get('IDP_ADMIN_REALM_URL'),
                                           client['id']),
                    verify=tls_verify(),
                    headers={'Authorization': 'Bearer {}'.format(get_auth_token())})

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # pragma: no cover
