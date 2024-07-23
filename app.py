from flask import Flask,url_for,session,redirect,render_template,jsonify,request
from authlib.integrations.flask_client import OAuth
import json
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests

app = Flask(__name__)
CORS(app)
appConf = {
    "OAUTH2_CLIENT_ID":"65896343084-arc4inpsmt2fl459cl2b7iik3gagbm08.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET":"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",
    "OAUTH2_META_URL":"https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET":"bcd89865-59ee-45f1-96e3-d3841c358c4b",
    "FLASK_PORT":5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register("myApp",
    client_id = appConf.get("OAUTH2_CLIENT_ID"),
    client_secret = appConf.get("OAUTH2_CLIENT_SECRET"),
    server_metadata_url=appConf.get("OAUTH2_META_URL"),
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/api/google-login')
def googleLogin():
    ans = oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback",_external=True))
    # print(ans.location)
    # url_data = list(enumerate(ans.headers))
    # url =json.dumps(url_data)
    return ans.location
    # return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback",_external=True))


@app.route('/signin-google')
def googleCallback():
    token = oauth.myApp.authorize_access_token()
    user_token = json.dumps(token)
    user_json_token = json.loads(user_token)
    print(user_json_token['access_token'])
    session['user'] = token
    return redirect(url_for("home"))

@app.route('/api/logout', methods=['GET'])
def logout():
    session.pop("user",None)
    return redirect("http://localhost:9000",code=200)

@app.route('/api/userdetails', methods = ["POST","GET"])
def userdetails():
    user_data = request.get_json(silent=True)
    idinfo = id_token.verify_oauth2_token(user_data['credential'], requests.Request(), '220563333877-ufu5dunsmssl9q382p2080ab61dsrdin.apps.googleusercontent.com')
    session['user'] = idinfo
    session_value=session.get("user")
    # json_object = json.dumps(session_value, indent = 4) 
    return jsonify(session_value)

@app.route('/api/check-user', methods=['GET'])
def checkuser():
    if session.get("user") != '':
        session_value=session.get("user")
        return jsonify(session_value)
    else:
        return redirect("http://localhost:9000",code=200)

@app.route('/',methods=['GET', 'POST'])
def home():
    # return render_template("home.html",session=session.get("user"),pretty=json.dumps(session.get("user"),indent = 4))
    session_value=session.get("user"),
    pretty=json.dumps(session.get("user"),indent = 4)
    return redirect('http://localhost:9000/#/main?name{}'.format(session_value))


if __name__ == "__main__" :
    app.run(host="0.0.0.0",port=5000,debug=True)