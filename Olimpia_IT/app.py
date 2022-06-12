from flask import jsonify, render_template, redirect, url_for, flash, abort,  request
from token_fuctions import validateToken, writeToken
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from models.ModelUSer import ModelUser
from models.entities.user import User
from flask import Flask,  Blueprint
from serialization import InfoSchema
from config import config
from rpa import Rpa
import warnings

warnings.filterwarnings("ignore")
app = Flask(__name__)

db = SQLAlchemy(app)

csrf = CSRFProtect()
login_path = Blueprint("login_path", __name__)

@app.route('/')
def index():
    return render_template("index.html")

@login_path.route('/api')
def api():
    search = request.args.get('search', None)
    depto = request.args.get('depto', None)
    number = request.args.get('number', None)
    try:
        token = request.headers['Authorization'].split(" ")[1]
        if validateToken(token, output=True) != True:
            return validateToken(token, output=True)
    except:
        response = jsonify({"message": "You need an authorization token."})
        response.status_code = 401
        return response
    else:
        if search is None or search == "":
            abort(400)
        else:
            if depto is None or depto == "":
                abort(400)
            else:
                if number is None:
                    number = 10
                else:
                    if Rpa.stringInt(number):
                        number = int(number)
                    else:
                        abort(400)
        api_js = Rpa(search,depto, number)
        api_js.driverHandling()
        s = InfoSchema()
        response = jsonify(api_js.info)
        if len(s.dump(api_js.info)) == 0:
            if "Error" in api_js.info["message"]:
                response.status_code = 404
            elif "There" in api_js.info["message"] :
                response.status_code = 501
            elif "ND" in api_js.info["message"] :
                abort(400)
            else:
                response.status_code = 200
            return response
        response.status_code = 200
        return jsonify(s.dump(api_js.info))
    
@app.route('/token/<string:id>')
def token(id):
    return render_template("token.html", token = id)

@login_path.route('/token_generator', methods=['GET', 'POST'])
def token_generator():

    if request.method == 'POST':
        user = User(request.form['username'],request.form['password'])
        logged_user = ModelUser.login(db,user)
        form = request.form.to_dict(flat=False)
        for i in form.keys():
            form[i] = form[i][0]
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('token', id = writeToken(auth=form)))
            else:
                flash("Invalid password. Try again ...")
                return render_template("token_generator.html")
        else:
            flash("User not found. Try again ...")
            return render_template("token_generator.html") 
    else:
        return render_template("token_generator.html")

app.register_blueprint(login_path)

if __name__ == "__main__":
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run()