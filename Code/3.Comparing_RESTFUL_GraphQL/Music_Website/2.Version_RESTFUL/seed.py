from .app import create_app
from app.db import db
from app.models import Track, Genre, Album

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    rock = Genre(name="Rock")
    pop = Genre(name="Pop")
    db.session.add_all([rock, pop])
    db.session.commit()

    album1 = Album(title="Best Hits", artist_name="Queen")
    album2 = Album(title="Smooth Pop", artist_name="Adele")
    db.session.add_all([album1, album2])
    db.session.commit()

    track1 = Track(name="Bohemian Rhapsody", milliseconds=354000, unit_price=1.99, genre_id=rock.genre_id, album_id=album1.album_id)
    track2 = Track(name="Rolling in the Deep", milliseconds=228000, unit_price=1.49, genre_id=pop.genre_id, album_id=album2.album_id)
    db.session.add_all([track1, track2])
    db.session.commit()

    print("DB seeded.")
