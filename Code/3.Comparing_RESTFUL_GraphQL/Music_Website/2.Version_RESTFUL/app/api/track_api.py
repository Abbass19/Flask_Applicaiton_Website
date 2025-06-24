from flask import Blueprint
from flask_restful import Resource, Api, abort
from app.models import *
from app.db import *

track_api = Blueprint("track_api", __name__)
api = Api(track_api)

def track_to_dict(track):
    minutes = (track.milliseconds or 0) // 60000
    seconds = ((track.milliseconds or 0) % 60000) // 1000
    return {
        "id": track.track_id,
        "name": track.name,
        "genre": track.genre.name if track.genre else "Unknown",
        "album": track.album.title if track.album else "Unknown",
        "time": f"{minutes}:{seconds:02d}",
        "price": float(track.unit_price),
    }

class TrackListResource(Resource):
    def get(self):
        tracks = Track.query.limit(10).all()
        return [track_to_dict(t) for t in tracks], 200

class TrackResource(Resource):
    def get(self, track_id):
        track = Track.query.get(track_id)
        if not track:
            abort(404, message="Track not found")
        return track_to_dict(track), 200

api.add_resource(TrackListResource, "/api/tracks")
api.add_resource(TrackResource, "/api/tracks/<int:track_id>")
