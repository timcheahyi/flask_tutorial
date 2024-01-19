# Importing necessary libraries
from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# Creating a Flask app instance
app = Flask(__name__)
# Initializing a RESTful API with the Flask apps
api = Api(app)
# Configuring the SQLite database URI for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Initializing SQLAlchemy with the app
db = SQLAlchemy(app)

# Defining a SQLAlchemy model for videos


class videoModel(db.Model):
    # Defining columns for the model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # Representing the model instance as a string
    def __repr__(self):
        return f"Video(name ={self.name}, views = {self.views}, likes = {self.likes})"


class User(db.Model, UserMixin):
    # Defining columns for the model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')


# Setting up argument parsing for requests
video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video")
video_put_args.add_argument("likes", type=int, help="Likes on the video")

# Defining the fields for serializing responses
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

# Defining a Resource for video


class video(Resource):
    # GET method for retrieving a video by ID
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video with ID {} doesn't exist".format(video_id))
        return result

    # POST method for adding a new video
    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_put_args.parse_args()
        video = videoModel(
            id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return (video, 201)

    # DELETE method for deleting a video
    @marshal_with(resource_fields)
    def delete(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video with ID {} doesn't exist".format(video_id))

        db.session.delete(result)
        db.session.commit()

        return {"message": "Video deleted", "video_id": video_id}, 200


class videos(Resource):
    # GET method for retrieving all videos
    @marshal_with(resource_fields)
    def get(self):
        # Query all records from the videoModel table
        videos = videoModel.query.all()
        return videos


@app.route('/login')
def login():
    return "login"


@app.route('/register')
def register():
    return "register"


# Adding the video resource to the API
api.add_resource(video, "/video/<int:video_id>")
api.add_resource(videos, "/videos")

# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
