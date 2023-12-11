from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databse.db'
db = SQLAlchemy(app)


class videoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name ={self.name}, views = {self.views}, likes = {self.likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="name required", required=True)
video_put_args.add_argument("views", type=int, help="views required")
video_put_args.add_argument("likes", type=int, help="likes required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video with ID {} doesn't exist".format(video_id))
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
        video = videoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return (video, 201)

    def delete(self, video_id):
        return ("Video deleted at http://localhost:5000/video/" + str(video_id))


api.add_resource(video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
