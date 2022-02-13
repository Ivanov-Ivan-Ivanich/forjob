from sqlalchemy import create_engine, ForeignKey,Column, Date, Integer, String

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import query, sessionmaker
 
engine = create_engine ('sqlite:///olx.db',echo = True)

Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()
session._model_changes = {}

class Olx(Base):
    session = Session()

    __tablename__= 'olx'

    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False)
    url = Column(String, unique = True, nullable = False)
    price = Column(String,nullable = True)
    location = Column(String, nullable = False)
    
    def __init__(self,title,url,price,location):
        self.title = title
        self.url = url
        self.price = price
        self.location = location

Olx.metadata.create_all(engine)

def save_db(title,url,price,location):
    ads = session.query(Olx).filter(Olx.url == url).count()
    if not ads:

        advert = Olx(title = title, url = url, price = price, location = location)
        Olx.session.add(advert)
        Olx.session.commit()    