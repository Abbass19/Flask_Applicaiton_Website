from app import create_app
from app.db import db
from app.models import Genre, Album, Track

app = create_app()

with app.app_context():
    db.create_all()

    # Clear tables (optional)
    db.session.query(Track).delete()
    db.session.query(Album).delete()
    db.session.query(Genre).delete()

    # Add Genres
    rock = Genre(name="Rock")
    pop = Genre(name="Pop")
    db.session.add_all([rock, pop])
    db.session.commit()

    # Add Albums
    album1 = Album(title="Best Hits", artist_name="Queen")
    album2 = Album(title="Smooth Pop", artist_name="Adele")
    db.session.add_all([album1, album2])
    db.session.commit()

    # Add Tracks
    track1 = Track(name="Bohemian Rhapsody", milliseconds=354000, unit_price=1.99, genre_id=rock.genre_id, album_id=album1.album_id)
    track2 = Track(name="Rolling in the Deep", milliseconds=228000, unit_price=1.49, genre_id=pop.genre_id, album_id=album2.album_id)
    db.session.add_all([track1, track2])
    db.session.commit()

    print("Database seeded with sample data.")
