# This thing serves a web page that reads and parses the basic auth headers

from bottle import auth_basic, request, route, run, response, hook
import base64

port = 8080
debug = True


def read_basic_auth(username, password):
    auth = request.get_header('Authorization')
    if auth:
        basic, encoded = auth.split(' ')
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(':')
        print(f"Username: {username}\nPassword: {password}")
    return True


@route('/')
@auth_basic(read_basic_auth)
def index():
    print(json.dumps(dict(request.headers), indent=4, sort_keys=True))
    response.status = 200
    return "Hello, world!"


if __name__ == '__main__':
    run(host='0.0.0.0', port=port, debug=debug, reloader=True)           


