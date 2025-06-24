from .db import db

class Genre(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Album(db.Model):
    album_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    artist_name = db.Column(db.String)

class Track(db.Model):
    track_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    milliseconds = db.Column(db.Integer)
    unit_price = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'))

    genre = db.relationship('Genre', backref='tracks')
    album = db.relationship('Album', backref='tracks')
