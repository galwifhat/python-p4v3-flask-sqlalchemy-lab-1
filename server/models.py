from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)


# Add models here
class Earthquake(db.Model, SerializerMixin):
    __tablename__ = "earthquakes"

    id = db.Column(db.Integer, primary_key=True)
    magnitude = db.Column(db.Float)
    location = db.Column(db.String)
    year = db.Column(db.Integer)

    # avoid writing body it manually every time
    # make python object JSON serializable
    # best practice
    # no need for the to dict fun when using serializartion, it removes the need for to_dict func
    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "magnitude": self.magnitude,
    #         "location": self.location,
    #         "year": self.year,
    #     }

    # Then in routes (app.py)
    # return make_response(quake.to_dict(), 200)

    def __repr__(self):
        return f"<Earthquake {self.id} {self.magnitude} {self.location} {self.year}>"
