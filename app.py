from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/.well-known/openid-configuration', methods=['GET'])
def wellKnown():
    res = {}

    res["token_endpoint"] = "http://idp.example.com/auth/realm/token"

    return jsonify(res)

@app.route('/clients/<clientId>', methods=['PUT'])
def createOrUpdate(clientId):
    print(clientId)
    print(request.data)

@app.route('/clients/<clientId>', methods=['DELETE'])
def delete(clientId):
    print(clientId)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # pragma: no cover