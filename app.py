from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route('/.well-known/openid-configuration', methods=['GET'])
def wellKnown():
    res = {}
    app.logger.info("test")

    res["token_endpoint"] = "http://idp.example.com/auth/realm/token"

    return jsonify(res)


@app.route('/clients/<clientId>', methods=['PUT'])
def createOrUpdate(clientId):
    app.logger.info(clientId)
    app.logger.info(request.data)

    return request.data


@app.route('/clients/<clientId>', methods=['DELETE'])
def delete(clientId):
    app.logger.info(clientId)

    return None


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # pragma: no cover
