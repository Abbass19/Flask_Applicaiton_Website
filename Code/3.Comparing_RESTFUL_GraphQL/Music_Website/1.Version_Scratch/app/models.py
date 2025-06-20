from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import db

#I will be writing over these lines for more clarity on my side
# I am still learning. So I am doing so weird stuff still
# The Line Below is the primary key of hte table
# This table is parent of Album table.
# back_populates means that the relationships works in a direction
# When written in both tables, we have 2 way relationship

class Artist(db.Model):
    __tablename__ = 'artist'
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    albums = relationship('Album', back_populates='artist')

class Album(db.Model):
    __tablename__ = 'album'
    album_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    artist_id = db.Column(db.Integer, ForeignKey('artist.artist_id'), nullable=False)
    artist = relationship('Artist', back_populates='albums')

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(20), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(30))
    reports_to = db.Column(db.Integer, ForeignKey('employee.employee_id'), nullable=True)
    birth_date = db.Column(DateTime)
    hire_date = db.Column(DateTime)
    address = db.Column(db.String(70))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String(24))
    fax = db.Column(db.String(24))
    email = db.Column(db.String(60))
    manager = relationship('Employee', remote_side=[employee_id], backref='subordinates')

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(80))
    address = db.Column(db.String(70))
    city = db.Column(db.String(40))
    state = db.Column(db.String(40))
    country = db.Column(db.String(40))
    postal_code = db.Column(db.String(10))
    phone = db.Column(db.String(24))
    fax = db.Column(db.String(24))
    email = db.Column(db.String(60))
    support_rep_id = db.Column(db.Integer, ForeignKey('employee.employee_id'))
    support_rep = relationship('Employee', backref='customers')
    comments = relationship('Comment', back_populates='customer', cascade="all, delete-orphan")

class Genre(db.Model):
    __tablename__ = 'genre'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    tracks = relationship('Track', back_populates='genre')

class MediaType(db.Model):
    __tablename__ = 'media_type'
    media_type_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    tracks = relationship('Track', back_populates='media_type')

class Track(db.Model):
    __tablename__ = 'track'
    track_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    album_id = db.Column(db.Integer, ForeignKey('album.album_id'))
    media_type_id = db.Column(db.Integer, ForeignKey('media_type.media_type_id'))
    genre_id = db.Column(db.Integer, ForeignKey('genre.genre_id'))
    composer = db.Column(db.String(220))
    milliseconds = db.Column(db.Integer)
    bytes = db.Column(db.Integer)
    unit_price = db.Column(db.Numeric(10, 2))
    album = relationship('Album', backref='tracks')
    media_type = relationship('MediaType', back_populates='tracks')
    genre = relationship('Genre', back_populates='tracks')
    invoice_lines = relationship('InvoiceLine', back_populates='track')
    playlist_tracks = relationship('PlaylistTrack', back_populates='track')

class Invoice(db.Model):
    __tablename__ = 'invoice'
    invoice_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customer.customer_id'), nullable=False)
    invoice_date = db.Column(DateTime, nullable=False)
    billing_address = db.Column(db.String(70))
    billing_city = db.Column(db.String(40))
    billing_state = db.Column(db.String(40))
    billing_country = db.Column(db.String(40))
    billing_postal_code = db.Column(db.String(10))
    total = db.Column(db.Numeric(10, 2), nullable=False)
    customer = relationship('Customer', backref='invoices')

class InvoiceLine(db.Model):
    __tablename__ = 'invoice_line'
    invoice_line_id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, ForeignKey('invoice.invoice_id'), nullable=False)
    track_id = db.Column(db.Integer, ForeignKey('track.track_id'), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    invoice = relationship('Invoice', backref='invoice_lines')
    track = relationship('Track', back_populates='invoice_lines')

class Playlist(db.Model):
    __tablename__ = 'playlist'
    playlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    playlist_tracks = relationship('PlaylistTrack', back_populates='playlist')

class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_track'
    playlist_id = db.Column(db.Integer, ForeignKey('playlist.playlist_id'), primary_key=True)
    track_id = db.Column(db.Integer, ForeignKey('track.track_id'), primary_key=True)
    playlist = relationship('Playlist', back_populates='playlist_tracks')
    track = relationship('Track', back_populates='playlist_tracks')

class Comment(db.Model):
    __tablename__ = 'comments'
    note_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customer.customer_id'), nullable=False)
    customer_name = db.Column(db.String(255))
    note_text = db.Column(db.Text)
    customer = relationship('Customer', back_populates='comments')