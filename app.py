import flask
from werkzeug.utils import secure_filename
from flask import  abort,request,send_file,jsonify, make_response
from model import Model
model=Model()

from flask_cors import CORS, cross_origin
app = flask.Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "API for Question Answer is working"
@app.route('/trainmodel', methods = ['GET', 'POST'])
def train_model():
   json_data = flask.request.json
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
       result=model.trainmodel()
       return _corsify_actual_response(jsonify(result))
      
   else:
      return "error"
@app.route('/predictmodel', methods = ['GET', 'POST'])
def predict_model():
   json_data = flask.request.json
   if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
   elif request.method == 'GET':
      #data = request.values
      if json_data["Question"]!="":
          
          result=model.predict(json_data["Question"])
          return _corsify_actual_response(jsonify(result))
      else:
          return _corsify_actual_response(jsonify({"success":False,"message":"Invalid Question"}))
   else:
      return "error"
  

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    #response.headers.add('Access-Control-Allow-Headers', "*")
    #response.headers.add('Access-Control-Allow-Methods', "*")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host= "0.0.0.0", port = 3000, threaded=True,debug=True, use_reloader=True)