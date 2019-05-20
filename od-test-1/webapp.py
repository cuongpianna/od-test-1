from os import environ as env
from functools import wraps
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode


app = Flask(__name__)


def get_debug_flag()->bool:
    if int(env.get('DEBUG', '1')) > 0:
        print('DEBUG ENABLED')
        return True
    return False


app.debug = get_debug_flag()
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=env.get('AUTH0_CLIENT_ID', 'no-value'),
    client_secret=env.get('AUTH0_CLIENT_SECRET', 'no-value'),
    api_base_url=env.get('AUTH0_BASE_URL', 'no-value'),
    access_token_url='{}/oauth/token'.format(env.get('AUTH0_BASE_URL', 'no-value')),
    authorize_url='{}/authorize'.format(env.get('AUTH0_BASE_URL', 'no-value')),
    client_kwargs={
        'scope': 'openid profile',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    return 'Hello, World!' 


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


@app.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=env.get('AUTH0_CALLBACK_URL', 'no-value'),
        audience=env.get('AUTH0_AUDIENCE', 'no-value')
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 5000))

# EOF
