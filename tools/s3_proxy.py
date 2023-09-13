''' 
Use case
    Need to access a file in a s3 bucket from a Fortigate Threat Feed
    (And I want to run it in a screen)

The curl/socat solusions: 
Proxy  $ 
    socat -v TCP-LISTEN:8081,fork,reuseaddr TCP:s3-eu-west-1.amazonaws.com:443

Client $ 
    curl https://<Proxy_Ip>:8081/<path>/<file> -H "Host: s3-eu-west-1.amazonaws.com" -k
    curl --resolve s3-eu-west-1.amazonaws.com:8081:<Proxy_Ip> https://s3-eu-west-1.amazonaws.com:8081/<path>/<file>

Disclaimer:
    This was the fastest, non-intrusive way I could think of when socat failed due to the limited options in the Fortigate

'''
import json
import bottle
import requests
port = 8081
debug = True


@bottle.get('/s3_proxy')
def proxy():
    try:
        vhost = bottle.request.query['vhost']
        path = bottle.request.query['path']
        _file = bottle.request.query['file']
        if debug:
            print(vhost)
            print(path)
            print(_file)
    except:
        bottle.response.status = 400
        return 'The query parameters needs to be, vhost, path and file'
    bottle.response.status = 200
    url = f'https://{vhost}/{path}/{_file}'
    return requests.get(url).text


if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=port, debug=debug, reloader=True)
