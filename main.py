from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="name required", required = True)
video_put_args.add_argument("views", type=int, help="views required")
video_put_args.add_argument("likes", type=int, help="likes required")

videos = {}

def abortIfNoExist(video_id):
    if video_id not in videos:
        abort(404, message = "not in database")
        
def abortIfExist(video_id):
    if video_id in videos:
        abort(409, message = "already in database")

class video(Resource):
    def get(self, video_id):
        abortIfNoExist(video_id)
        return videos[video_id]
    
    def post(self, video_id):
        abortIfExist(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return ("Video posted at http://localhost:5000/video/" + str(video_id))
    
    def delete(self, video_id):
        abortIfNoExist(video_id)
        del videos[video_id]
        return ("Video deleted at http://localhost:5000/video/" + str(video_id))
    
api.add_resource(video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)