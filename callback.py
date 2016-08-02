from flask import Flask, abort, request
import requests, requests.auth

STATE_FILE_PATH = 'states.txt'
CLIENT_ID = 'REDACTED'
CLIENT_SECRET = 'REDACTED'
REDIRECT_URI = 'REDACTED'
USER_AGENT_STRING = 'shnoo: cli wrapper for reddit'

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return '<a href="%s">Authenticate with your Reddit account</a>' % make_url()

@app.route('/callback')
def callback():
    error = request.args.get('error', '')
    if error:
        return error
    state = request.args.get('state')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    token = get_token(code)
    return "Your info is %s" % get_username(token)

def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {'grant_type': 'authorization_code',
                 'code': code,
                 'redirect_uri': REDIRECT_URI}
    response = requests.post('https://ssl.reddit.com/api/v1/access_token',
                             auth=client_auth,
                             headers = {'User-agent': USER_AGENT_STRING},
                             data=post_data)
    return response.json()['access_token']

def is_valid_state(state):
    with open(STATE_FILE_PATH) as f:
        for line in f:
            if state == line:
                return True
    return False

def make_url():
    from uuid import uuid4
    from urllib.parse import urlencode
    state = str(uuid4())
    with open(STATE_FILE_PATH, 'w') as f:
        f.write(state)
    params = {'client_id': CLIENT_ID,
              'response_type': 'code',
              'state': state,
              'redirect_uri': REDIRECT_URI,
              'duration': 'temporary',
              'scope': 'identity'}
    return 'https://ssl.reddit.com/api/v1/authorize?' + urlencode(params)

def get_username(access_token):
    headers = {'User-agent': USER_AGENT_STRING,
               'Authorization': 'bearer ' + access_token}
    response = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
