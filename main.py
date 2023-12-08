from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

names = {"tim" : {"age" : 25, "gender":"male"},
         "wach" : {"age" : 23, "gender":"female"}}

class homePage(Resource):
    def get(self):
        return{"data":"home page"}

class name(Resource):
    def get(self, name):
        return names[name]

api.add_resource(homePage, "/")
api.add_resource(name, "/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)