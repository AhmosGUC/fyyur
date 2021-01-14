from app import db, Venue, Artist, Show

v1 = Venue(name='Dor Ri Mi', city='New York', state='NY', address='53', phone='24008200', genres='jazz', image_link='https://picsum.photos/200/300',
           facebook_link='https://www.facebook.com/HeshamAhmos', website_link='https://www.facebook.com/HeshamAhmos', seeking_talent=True, seeking_description='yes we do')

a1 = Artist(name='GUNS N PETALS', city='San Francisco', state='CA', phone=' 326-123-5000', genres='ROCK N ROLL', image_link='https://picsum.photos/200/300',
            facebook_link='https://www.facebook.com/HeshamAhmos', website_link='https://www.facebook.com/HeshamAhmos', seeking_venue=True, seeking_description='yes we do')

s1 = Show(start_time='')
