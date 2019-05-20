from os import environ as env
from flask import Flask


app = Flask(__name__)


def get_debug_flag()->bool:
    if int(env.get('DEBUG', '1')) > 0:
        print('DEBUG ENABLED')
        return True
    return False


app.debug = get_debug_flag()


@app.route('/')
def hello_world():
    return 'Hello, World!' 


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 5000))

# EOF
