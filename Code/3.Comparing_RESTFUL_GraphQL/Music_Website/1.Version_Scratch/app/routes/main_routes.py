from datetime import datetime

from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from sqlalchemy import func
from ..models import *




main = Blueprint('main', __name__)



#Classes and Objects to Be created:
class TrackElement:
    def __init__(self, name, genre, album_name, time, price):
        self.name = name
        self.genre = genre
        self.album_name = album_name
        self.time = time
        self.price = price

class Album_Front_End_Object:
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


class ArtistSimple:
    def __init__(self, name, total_sold):
        self.name = name
        self.total_sold = total_sold

#Queries for All sort of things preparing to the function to Work


#Constant Queries


#This returns list of track_element : track_block
def get_top_tracks(n=4):
    # This returns a list of tuples: (Track instance, total_sold)
    results = (
        db.session.query(
            Track,
            func.sum(InvoiceLine.quantity).label('total_sold')
        )
        .join(InvoiceLine, Track.track_id == InvoiceLine.track_id)
        .group_by(Track.track_id)
        .order_by(func.sum(InvoiceLine.quantity).desc())
        .limit(n)
        .all()
    )

    track_elements = []
    for track, total_sold in results:
        # Format milliseconds to time string (e.g. "3:45")
        minutes = (track.milliseconds or 0) // 60000
        seconds = ((track.milliseconds or 0) % 60000) // 1000
        time_str = f"{minutes}:{seconds:02d}"

        # Build TrackElement object
        te = TrackElement(
            name=track.name,
            genre=track.genre.name if track.genre else "Unknown",
            album_name=track.album.title if track.album else "Unknown",
            time=time_str,
            price=float(track.unit_price) if track.unit_price else 0.0
        )
        track_elements.append(te)
    return track_elements


def get_explore(genre=None, keyword=None, max_time=None, n=30):
    print(f"Asking for {n} music of genre {genre} and Keyword {keyword} and max time {max_time}")

    query = (
        db.session.query(
            Track,
            func.sum(InvoiceLine.quantity).label('total_sold')
        )
        .join(InvoiceLine, Track.track_id == InvoiceLine.track_id)
        .group_by(Track.track_id)
        .order_by(func.sum(InvoiceLine.quantity).desc())
    )

    if genre:
        query = query.join(Genre).filter(Genre.name == genre)

    if keyword:
        query = query.filter(Track.name.ilike(f'%{keyword}%'))

    # if max_time is not None:
    #     max_time_ms = int(max_time) * 1000
    #     query = query.filter(Track.milliseconds <= max_time_ms)

    results = query.limit(n).all()
    print(f"the results found has {len(results)} elements")

    track_elements = []
    for track, total_sold in results:
        minutes = (track.milliseconds or 0) // 60000
        seconds = ((track.milliseconds or 0) % 60000) // 1000
        time_str = f"{minutes}:{seconds:02d}"

        te = TrackElement(
            name=track.name,
            genre=track.genre.name if track.genre else "Unknown",
            album_name=track.album.title if track.album else "Unknown",
            time=time_str,
            price=float(track.unit_price) if track.unit_price else 0.0
        )
        track_elements.append(te)

    print(f"Outputting a list of {len(track_elements)} elements")
    return track_elements





# 8 Popular Albums
def get_top_albums(n=8):
    # Query to sum quantities of tracks grouped by album
    results = (
        db.session.query(
            Album,
            func.sum(InvoiceLine.quantity).label('total_sold')
        )
        .join(Track, Track.album_id == Album.album_id)
        .join(InvoiceLine, InvoiceLine.track_id == Track.track_id)
        .group_by(Album.album_id)
        .order_by(func.sum(InvoiceLine.quantity).desc())
        .limit(n)
        .all()
    )

    albums_list = []
    for album, total_sold in results:
        artist_name = album.artist.name if album.artist else "Unknown"
        album_obj = Album_Front_End_Object(
            name=album.title,
            artist=artist_name
        )
        albums_list.append(album_obj)
    return albums_list

#The 10 Popular Artist
def get_top_artists(n=5):
    results = (
        db.session.query(
            Artist,
            func.sum(InvoiceLine.quantity).label('total_sold')
        )
        .join(Album, Album.artist_id == Artist.artist_id)
        .join(Track, Track.album_id == Album.album_id)
        .join(InvoiceLine, InvoiceLine.track_id == Track.track_id)
        .group_by(Artist.artist_id)
        .order_by(func.sum(InvoiceLine.quantity).desc())
        .limit(n)
        .all()
    )

    top_artists = []
    for artist, total_sold in results:
        top_artists.append(ArtistSimple(name=artist.name, total_sold=total_sold))

    return top_artists

#Parameter Based Queries



@main.route('/home', methods=["GET", "POST"])
def home():
    if not session.get("user_id"):
        flash("Please login first to Enter the home page")
        return redirect(url_for('/login'))

    comments = [
        {'user_name': 'Alice', 'text': 'Great site!'},
        {'user_name': 'Bob', 'text': 'Love the music selection.'},
    ]



    return render_template('home.html' ,
                           popular_tracks=get_top_tracks(4),
                           popular_albums=get_top_albums(8),
                           popular_artists=get_top_artists(6),
                           comments=comments)


@main.route('explore')
def explore():

    genre = db.session.query(Genre).all()
    genre_list = []
    for gen in genre:
        genre_list.append(gen.name)

    input_genre = request.args.get('genre')
    input_Keyword = request.args.get('keyword', '')
    input_time = request.args.get('minutes', 10)
    print(f" Input genre {input_genre}")
    explore_track_block = get_explore(genre= input_genre, keyword=input_Keyword, max_time=input_time)
    return render_template("explore_filters.html", genres = genre_list, tracks = explore_track_block)


@main.route('/check_out', methods=['GET', 'POST'])
@main.route('/Check_out', methods=['GET', 'POST'])
@main.route('/check_out/', methods=['GET', 'POST'])
@main.route('/Check_out/', methods=['GET', 'POST'])
def checkout():
    # Check user login
    if not session.get('user_id'):
        flash("Please login to access checkout.")
        return redirect(url_for('auth.login'))  # or wherever your login route is

    # Get the purchase list from session
    to_purchase = session.get('to_purchase', [])
    if not to_purchase:
        flash("Your cart is empty.")
        return redirect(url_for('main.home'))  # or cart page

    # Query tracks info from DB by track name (assuming 'to_purchase' stores track names)
    tracks = Track.query.filter(Track.name.in_(to_purchase)).all()

    # Calculate total price
    total_price = sum(track.unit_price for track in tracks)

    if request.method == 'POST':

        customer = Customer.query.get(session['user_id'])
        if not customer:
            flash("Customer not found.")
            return redirect(url_for('main.home'))

        # Create new Invoice
        new_invoice = Invoice(
            customer_id=customer.customer_id,
            invoice_date=datetime.utcnow(),
            billing_address=customer.address,
            billing_city=customer.city,
            billing_state=customer.state,
            billing_country=customer.country,
            billing_postal_code=customer.postal_code,
            total=total_price
        )
        db.session.add(new_invoice)
        db.session.flush()  # flush to get new_invoice.invoice_id

        # Add invoice lines for each track (quantity = 1 for now)
        for track in tracks:
            line = InvoiceLine(
                invoice_id=new_invoice.invoice_id,
                track_id=track.track_id,
                unit_price=track.unit_price,
                quantity=1
            )
            db.session.add(line)
        db.session.commit()
        # Clear the cart after checkout
        session['to_purchase'] = []
        flash("Checkout successful! Your invoice has been created.")
        return redirect(url_for('main.home'))

    # Render checkout page (GET)
    return render_template('check_out.html', tracks=tracks, total=total_price)



@main.route('/artist')
@main.route('/Artist')
@main.route('/artist/')
@main.route('/Artist/')
def artist():

    artist = ["Michael Jackson"]


    return render_template("artist.html")


@main.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    track_name = request.form.get('track_name')
    if not track_name:
        flash("No track specified.")
        return redirect(url_for('home'))

    # Initialize cart in session if doesn't exist
    if 'to_purchase' not in session:
        session['to_purchase'] = []

    # Add the track name to the cart list
    cart = session['to_purchase']
    cart.append(track_name)
    session['to_purchase'] = cart  # re-assign to trigger session update

    flash(f"Added '{track_name}' to cart!")
    next_page = request.form.get('next')
    if next_page:
        return redirect(next_page)
    else:
        return redirect(url_for('main.home'))