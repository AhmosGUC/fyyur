#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODODONE: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


# shows_table = db.Table('shows',
#                        db.Column('venue_id', db.Integer, db.ForeignKey(
#                            'venues.id'), primary_key=True),
#                        db.Column('artist_id', db.Integer, db.ForeignKey(
#                            'artists.id'), primary_key=True),
#                        db.Column('start_time', db.DateTime)
#                        )
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id', ondelete="CASCADE"), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    artist = db.relationship("Artist", back_populates="venues")
    venue = db.relationship("Venue", back_populates="artists")

    def __repr__(self):
        return f'<Show {self.id},{self.venue_id}, {self.artist_id},{self.start_time}>'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120))
    artists = db.relationship(
        "Show", back_populates="venue", cascade="all, delete")

    def __repr__(self):
        return f'<Venue {self.id}, {self.name},{self.state}>'

    # TODODONE: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False)
    seeking_description = db.Column(db.String(120))
    available_days = db.Column(db.Integer, nullable=False)
    venues = db.relationship(
        "Show", back_populates="artist", cascade="all, delete")
    # TODODONE: implement any missing fields, as a database migration using Flask-Migrate

    def __repr__(self):
        return f'<Artist {self.id}, {self.name},{self.state}>'

# TODODONE Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    value = str(value)
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# misc func.
#----------------------------------------------------------------------------#


def days_to_num(lst):
    days = 0
    S = 1 << 6
    Su = 1 << 5
    M = 1 << 4
    T = 1 << 3
    W = 1 << 2
    Th = 1 << 1
    F = 1
    for d in lst:
        if d == "Saturday":
            days = days | S
        elif d == "Sunday":
            days = days | Su
        elif d == "Monday":
            days = days | M
        elif d == "Tuesday":
            days = days | T
        elif d == "Wednesday":
            days = days | W
        elif d == "Thursday":
            days = days | Th
        elif d == "Friday":
            days = days | F
    return days


def num_to_days(x):
    # 0b 0 0 0 0 0 0 0 0
    #      S S M T W T F
    # b = bin(x)
    b = x
    S = 1 << 6
    Su = 1 << 5
    M = 1 << 4
    T = 1 << 3
    W = 1 << 2
    Th = 1 << 1
    F = 1
    days = []
    if b & S > 0:
        days.append("Saturday")
    if b & Su > 0:
        days.append("Sunday")
    if b & M > 0:
        days.append("Monday")
    if b & T > 0:
        days.append("Tuesday")
    if b & W > 0:
        days.append("Wednesday")
    if b & Th > 0:
        days.append("Thursday")
    if b & F > 0:
        days.append("Friday")
    return days

# now = datetime.datetime.now()
# print(now.strftime("%A"))
# print(num_to_days(int('001100100', 2)))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():

    topNewVns = db.session.query(Venue.id, Venue.name).order_by(
        Venue.id.desc()).limit(10).all()
    topNewArts = db.session.query(Artist.id, Artist.name).order_by(
        Artist.id.desc()).limit(10).all()
    artists = []
    venues = []
    for v in topNewVns:
        venues.append({"id": v.id, "name": v.name})
    for a in topNewArts:
        artists.append({"id": a.id, "name": a.name})
    return render_template('pages/home.html', artists=artists, venues=venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODODONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    # data = [{
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "venues": [{
    #         "id": 1,
    #         "name": "The Musical Hop",
    #         "num_upcoming_shows": 0,
    #     }, {
    #         "id": 3,
    #         "name": "Park Square Live Music & Coffee",
    #         "num_upcoming_shows": 1,
    #     }]
    # }, {
    #     "city": "New York",
    #     "state": "NY",
    #     "venues": [{
    #         "id": 2,
    #         "name": "The Dueling Pianos Bar",
    #         "num_upcoming_shows": 0,
    #     }]
    # }]
    stateNcity = db.session.query(Venue.state, Venue.city).distinct().all()
    data = []
    for pair in stateNcity:
        elm = {"state": pair[0], "city": pair[1], "venues": []}
        data.append(elm)
    allVenues = Venue.query.all()

    for elm in data:
        for v in allVenues:
            if elm["state"] == v.state and elm["city"] == v.city:
                num_show = Show.query.filter(Show.venue_id == v.id).filter(
                    Show.start_time > datetime.now()).count()
                print(num_show)
                details = {"id": v.id, "name": v.name,
                           "num_upcoming_shows": num_show}
                elm["venues"].append(details)

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODODONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    search_term = '%'+search_term+'%'
    res = Venue.query.filter(Venue.name.ilike(search_term)).all()
    data = []
    for r in res:
        tmp = {"id": r.id, "name": r.name}
        data.append(tmp)
    response = {
        "count": len(res),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODODONE: replace with real venue data from the venues table, using venue_id

    v = Venue.query.get(venue_id)
    joinQry = db.session.query(Show, Artist).filter(Show.venue_id == v.id).join(
        Artist, Show.artist_id == Artist.id).all()

    past_shows = []
    upcoming_shows = []

    for a in joinQry:
        tmpArtist = {
            "artist_id": a[1].id,
            "artist_name": a[1].name,
            "artist_image_link": a[1].image_link,
            "start_time": a[0].start_time
        }
        if tmpArtist["start_time"] < datetime.now():
            past_shows.append(tmpArtist)
        else:
            upcoming_shows.append(tmpArtist)

    data = {
        "id": v.id,
        "name": v.name,
        "genres": v.genres.split(','),
        "address": v.address,
        "city": v.city,
        "state": v.state,
        "phone": v.phone,
        "website": v.website_link,
        "facebook_link": v.facebook_link,
        "seeking_talent": v.seeking_talent,
        "seeking_description": v.seeking_description,
        "image_link": v.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODODONE: insert form data as a new Venue record in the db, instead
    # TODODONE: modify data to be the data object returned from db insertion
    error = False
    try:
        f = request.form
        vf = VenueForm(f)
        if vf.validate_on_submit():
            newVenue = Venue()
            newVenue.name = f.get('name')
            newVenue.state = f.get('state')
            newVenue.city = f.get('city')
            newVenue.address = f.get('address')
            newVenue.phone = f.get('phone')
            newVenue.genres = ','.join(request.form.getlist("genres"))
            newVenue.seeking_talent = True if f.get(
                'seeking_talent', 'y') == 'y' else False
            newVenue.seeking_description = f.get('seeking_description', '')
            newVenue.facebook_link = f.get('facebook_link', None)
            newVenue.website_link = f.get('website_link', None)
            newVenue.image_link = f.get('image_link', None)

            db.session.add(newVenue)
            db.session.commit()
        else:
            for e in vf:
                print(e.errors)
            return render_template('forms/new_venue.html', form=vf)
    except:
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        # TODODONE: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
    else:
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODODONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODODONE: replace with real data returned from querying the database

    allArtist = db.session.query(Artist.id, Artist.name).all()
    data = allArtist
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODODONE: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    search_term = '%'+search_term+'%'
    res = Artist.query.filter(Artist.name.ilike(search_term)).all()
    data = []
    for r in res:
        tmp = {"id": r.id, "name": r.name}
        data.append(tmp)
    response = {
        "count": len(res),
        "data": data
    }

    response = {
        "count": len(res),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODODONE: replace with real venue data from the venues table, using venue_id
    a = Artist.query.get(artist_id)
    joinQry = db.session.query(Show, Venue).filter(Show.artist_id == a.id).join(
        Venue, Show.venue_id == Venue.id).all()

    past_shows = []
    upcoming_shows = []

    for v in joinQry:
        tmpVenue = {
            "venue_id": v[1].id,
            "venue_name": v[1].name,
            "venue_image_link": v[1].image_link,
            "start_time": v[0].start_time
        }
        if tmpVenue["start_time"] < datetime.now():
            past_shows.append(tmpVenue)
        else:
            upcoming_shows.append(tmpVenue)

    data = {
        "id": a.id,
        "name": a.name,
        "genres": a.genres.split(','),
        "available_days": num_to_days(a.available_days),
        "city": a.city,
        "state": a.state,
        "phone": a.phone,
        "website": a.website_link,
        "facebook_link": a.facebook_link,
        "seeking_venue": a.seeking_venue,
        "seeking_description": a.seeking_description,
        "image_link": a.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    a = Artist.query.get(artist_id)
    artist = {
        "id": a.id,
        "name": a.name,
        "genres": a.genres.split(','),
        "available_days": num_to_days(a.available_days),
        "city": a.city,
        "state": a.state,
        "phone": a.phone,
        "website_link": a.website_link,
        "facebook_link": a.facebook_link,
        "seeking_venue": a.seeking_venue,
        "seeking_description": a.seeking_description,
        "image_link": a.image_link
    }
    form = ArtistForm(data=artist)

    # TODODONE: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODODONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    try:
        f = request.form
        a = Artist.query.get(artist_id)
        af = ArtistForm(f)
        if af.validate_on_submit():
            a.name = f.get('name')
            a.city = f.get('city')
            a.state = f.get('state')
            a.phone = f.get('phone')
            a.genres = ','.join(request.form.getlist("genres"))
            a.available_days = days_to_num(
                request.form.getlist("available_days"))
            a.seeking_venue = True if f.get(
                'seeking_venue', 'n') == 'y' else False
            a.seeking_description = f.get('seeking_description', "")
            a.facebook_link = f.get('facebook_link', None)
            a.website_link = f.get('website_link', None)
            a.image_link = f.get('image_link', None)
            db.session.commit()
        else:
            return render_template('forms/edit_artist.html', form=af, artist=a)

    except:
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    v = Venue.query.get(venue_id)
    venue = {
        "id": v.id,
        "name": v.name,
        "genres": v.genres.split(','),
        "city": v.city,
        "state": v.state,
        "address": v.address,
        "phone": v.phone,
        "website_link": v.website_link,
        "facebook_link": v.facebook_link,
        "seeking_talent": v.seeking_talent,
        "seeking_description": v.seeking_description,
        "image_link": v.image_link
    }
    form = VenueForm(data=venue)
    # TODODONE: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODODONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    try:
        f = request.form
        vf = VenueForm(f)
        v = Venue.query.get(venue_id)
        if vf.validate_on_submit():
            v.name = f.get('name')
            v.city = f.get('city')
            v.state = f.get('state')
            v.phone = f.get('phone')
            v.address = f.get('address')
            v.genres = ','.join(request.form.getlist("genres"))
            v.seeking_talent = True if f.get(
                'seeking_talent', 'n') == 'y' else False
            v.seeking_description = f.get('seeking_description', "")
            v.facebook_link = f.get('facebook_link', None)
            v.website_link = f.get('website_link', None)
            v.image_link = f.get('image_link', None)
            db.session.commit()

        else:
            return render_template('forms/edit_venue.html', form=vf, venue=v)

    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODODONE: insert form data as a new Venue record in the db, instead
    # TODODONE: modify data to be the data object returned from db insertion
    error = False
    try:
        f = request.form
        af = ArtistForm(f)
        if af.validate_on_submit():

            newArtist = Artist()
            newArtist.name = f.get('name')
            newArtist.city = f.get('city')
            newArtist.state = f.get('state')
            newArtist.phone = f.get('phone')
            newArtist.genres = ','.join(request.form.getlist("genres"))
            newArtist.available_days = days_to_num(
                request.form.getlist("available_days"))
            newArtist.seeking_venue = True if f.get(
                'seeking_venue', 'n') == 'y' else False
            newArtist.seeking_description = f.get('seeking_description', "")
            newArtist.facebook_link = f.get('facebook_link', None)
            newArtist.website_link = f.get('website_link', None)
            newArtist.image_link = f.get('image_link', None)

            db.session.add(newArtist)
            db.session.commit()
        else:
            return render_template('forms/new_artist.html', form=af)
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')
    else:
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')

    # TODODONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODODONE: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

    joinQry = db.session.query(Show, Venue, Artist).join(
        Venue, Show.venue_id == Venue.id).join(
        Artist, Show.artist_id == Artist.id).order_by(Show.start_time).all()
    past_shows = []
    next_shows = []
    for s in joinQry:
        tmpShow = {
            "venue_id": s[1].id,
            "venue_name": s[1].name,
            "artist_id": s[2].id,
            "artist_name": s[2].name,
            "artist_image_link": s[2].image_link,
            "start_time": s[0].start_time
        }
        if(tmpShow["start_time"] > datetime.now()):
            next_shows.append(tmpShow)
        else:
            past_shows.append(tmpShow)

    return render_template('pages/shows.html', past_shows=past_shows, next_shows=next_shows)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form, error=[])


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODODONE: insert form data as a new Show record in the db, instead
    error = False
    errors = []
    try:
        f = request.form
        sf = ShowForm(f)
        if sf.validate_on_submit():
            artist_id = f.get("artist_id")
            venue_id = f.get("venue_id")
            a = Artist.query.get(artist_id)
            v = Venue.query.get(venue_id)
            start_time = f.get('start_time')
            x = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

            if a is None:
                errors.append('No artist with this id')
            if v is None:
                errors.append('No venue with this id')
            if a:
                day = x.strftime("%A")
                days = num_to_days(a.available_days)
                if not day in days:
                    errors.append('Artist is not available this day')
            if len(errors) == 0:
                newShow = Show(start_time=start_time)
                newShow.artist = a
                newShow.venue = v
                db.session.add(newShow)
                db.session.commit()
            # on successful db insert, flash success
                flash('Show was successfully listed!')
            else:
                error = True
        else:
            error = True
            for e in sf:
                for err in e.errors:
                    errors.append(err)
        if error:
            print(errors)
            return render_template('forms/new_show.html', form=sf, all_errors=errors)
    except:
        error = True
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        flash('Internal Server Error try again later!')
    # TODODONE: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
