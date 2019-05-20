from os import environ as env
from functools import wraps
import json
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


DEBUG_FLAG = get_debug_flag()
app.debug = DEBUG_FLAG
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
def home():
    print('HOME rendering')
    return render_template('home.html')


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    if DEBUG_FLAG is True:
        print('/callback - setting session with userinfo={}'.format(userinfo))

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect(url_for('dashboard'))


@app.route('/login')
def login():
    redirect_uri = env.get('AUTH0_CALLBACK_URL', 'no-value')
    audience = env.get('AUTH0_AUDIENCE', 'no-value')
    if DEBUG_FLAG:
        print('/login - Redirecting to "{}" with redirect_url={}'.format(audience, redirect_uri))
    return auth0.authorize_redirect(
        redirect_uri=redirect_uri,
        audience=audience
    )


@app.route('/dashboard')
@requires_auth
def dashboard():
    if DEBUG_FLAG is True:
        print('/dashboard - profile: {}'.format(session['profile']))
        print('/dashboard - jwt_payload: {}'.format(session['jwt_payload']))
    return render_template(
        'dashboard.html',
        userinfo=session['profile'],
        userinfo_pretty=json.dumps(
            session['jwt_payload'],
            indent=4
        )
    )


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('home', _external=True), 
        'client_id': 'KGqKt6tqXfXQwFlKVyKKsXUUu0Wz1wf6',
    }
    final_uri = '{}/v2/logout?{}'.format(
        auth0.api_base_url,
        urlencode(params)
    )
    if DEBUG_FLAG:
        print('/logout - redirecting to {}'.format(final_uri))
    return redirect(final_uri)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 5000))

# EOF
