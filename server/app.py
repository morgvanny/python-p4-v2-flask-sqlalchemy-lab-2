from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import Review, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Flask SQLAlchemy Lab 2</h1>"


@app.route("/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "GET":
        return make_response([review.to_dict() for review in Review.query.all()], 200)
    else:
        comment = request.form.get("comment")
        item_id = request.form.get("item_id")
        customer_id = request.form.get("customer_id")

        r = Review(comment=comment, item_id=item_id, customer_id=customer_id)
        db.session.add(r)
        db.session.commit()
        return make_response(r.to_dict(), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
