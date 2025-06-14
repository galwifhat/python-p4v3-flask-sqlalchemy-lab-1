# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/")
def index():
    body = {"message": "Flask SQLAlchemy Lab 1"}
    return make_response(body, 200)


# Add views here
@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id=None):
    quake = Earthquake.query.filter_by(
        id=id
    ).first()  # this is a python object not JSON
    # Flask (and its underlying JSON serializer) doesn't know how to
    #  automatically turn your Earthquake model object into a valid JSON response
    if not quake:
        status_code_bad = 404
        body = {"message": f"Earthquake {id} not found."}
        return make_response(body, status_code_bad)
        # return make_response({"message": f"Earthquake {id} not found."}, 404)
    else:
        # extracting the fields from the Earthquake object into a plain dictionary
        # something Flask can serialize to JSON and send back to the client - using sqlalchemy-serializer
        # body = {
        #     "id": quake.id,
        #     "location": quake.location,
        #     "magnitude": quake.magnitude,
        #     "year": quake.year,
        # }

        body = quake.to_dict()
        status_code_good = 200
        headers = {}

        return make_response(body, status_code_good, headers)
        return make_response(quake.to_dict(), status_code_good, headers)


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquake_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    if not quakes:
        status_code_bad = 200
        body = {"count": 0, "quakes": []}
        return make_response(body, status_code_bad)
        return make_response({"count": 0, "quakes": []}, 200)
    else:
        status_code_good = 200
        headers = {}
        body = {
            "count": len(quakes),
            "quakes": [quake.to_dict() for quake in quakes],
        }  # quake is an individual Earthquake object
        return make_response(body, status_code_good, headers)
        return make_response(
            {"count": len(quakes), "quakes": [quake.to_dict() for quake in quakes]},
            200,
            {},
        )


if __name__ == "__main__":
    app.run(port=5555, debug=True)
