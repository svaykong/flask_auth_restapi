from flask import request, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from ..models.user_model import User
from ..app import db
from ..utils.constant import baseurl

auth = Blueprint('auth', __name__, url_prefix=baseurl)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    firstName = data.get("firstName")
    lastName = data.get("lastName")
    password = data.get("password")

    if firstName and lastName and email and password:
        user = User.query.filter_by(email=email).first()
        # if user already register with existing email, notify user email has been taken.
        if user:
            return make_response(
                {"message": "Email has been taken"}, 401
            )

        # otherwise register user to database
        user = User(
            email=email,
            password=generate_password_hash(password),
            firstName=firstName,
            lastName=lastName,
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {"message": "User Created"}, 201
        )
    return make_response(
        {"message": "Unable to create user"}, 500
    )


@auth.route("/signin", methods=["POST"])
def signin():
    request_body = request.json
    if not request_body or not request_body.get("email") or not request_body.get("password"):
        return make_response(
            {"message": "Credentials were not provided"}, 401
        )

    # finding user email in database
    user = User.query.filter_by(email=request_body.get("email")).first()
    if not user:
        return make_response(
            {"message": "Please create an account"}, 401
        )
    if check_password_hash(user.password, request_body.get("password")):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        },
            "secret",
            "HS256"
        )
        return make_response({"token": token}, 200)
    return make_response(
        "Please check your credentials", 401
    )
