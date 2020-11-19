from flask import Flask, request, jsonify
import logging, requests, os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/.well-known/openid-configuration', methods=['GET'])
def get_openid_configuration():
    tls_verify = True
    
    if os.environ.get("IDP_VERIFY_TLS") == "false":
        tls_verify = False

    response = requests.get("{}/.well-known/openid-configuration".format(os.environ.get("IDP_REALM_URL")), verify=tls_verify)

    return response.json()


@app.route('/clients/<clientId>', methods=['PUT'])
def create_or_update(clientId):
    app.logger.info(clientId)

    return request.data


@app.route('/clients/<clientId>', methods=['DELETE'])
def delete(clientId):
    app.logger.info(clientId)

    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # pragma: no cover
