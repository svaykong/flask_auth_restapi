from flask import request, make_response, Blueprint
from ..models.user_model import User
from ..models.article_model import Article
from ..utils.constant import baseurl
from ..app import db
import jwt
from functools import wraps

article = Blueprint('article', __name__, url_prefix=baseurl)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return make_response({"message": "Token is missing"}, 401)

        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = User.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(f'exception::{e}')
            return make_response(
                {"message": "Token is invalid"}, 401
            )
        return f(current_user, *args, **kwargs)

    return decorated


@article.route("/articles", methods=["GET"])
@token_required
def getAllArticles(current_user):
    articles = Article.query.filter_by(userId=current_user.id).all()
    return make_response({
        "data": [each_article.serialize for each_article in articles]
    })


@article.route("/articles", methods=["POST"])
@token_required
def createArticle(current_user):
    try:
        data = request.json
        title = data.get("title")
        description = data.get("description")
        if title and description:
            new_article = Article(
                title=title,
                description=description,
                userId=current_user.id
            )
            db.session.add(new_article)
            db.session.commit()
            return new_article.serialize

        return make_response(
            {"message": "title or description is missing."}, 500
        )
    except Exception as e:
        print(f'exception::{e}')
        return make_response({
            "message": "Unknown error",
        }, 500)


@article.route("/articles/<article_id>", methods=["GET"])
@token_required
def getSingleArticle(current_user, article_id):
    try:
        find_article = Article.query.filter_by(userId=current_user.id, id=article_id).first()
        if find_article is None:
            return make_response(
                {"message": "Article not found."}, 404
            )

        return make_response(
            {"data": find_article.serialize}, 200
        )
    except Exception as e:
        print(f'get single article exception::{e}')
        return make_response(
            {"message": "unable to process"}, 409
        )


@article.route("/articles/<article_id>", methods=["PUT"])
@token_required
def updateArticle(current_user, article_id):
    try:
        find_article = Article.query.filter_by(userId=current_user.id, id=article_id).first()
        if find_article is None:
            return make_response(
                {"message": "unable to update"}, 409
            )
        data = request.json
        title = data.get("title")
        description = data.get("description")
        if title and description:
            find_article.title = title
            find_article.description = description
        db.session.commit()
        return make_response(
            {"message": find_article.serialize}, 200
        )
    except Exception as e:
        print(f'update articles exception::{e}')
        return make_response(
            {"message": "unable to process"}, 409
        )


@article.route("/articles/<article_id>", methods=["DELETE"])
@token_required
def deleteArticle(current_user, article_id):
    try:
        find_article = Article.query.filter_by(userId=current_user.id, id=article_id).first()
        if find_article is None:
            return make_response(
                {"message": f"Article with {article_id} not found."}, 404
            )
        db.session.delete(find_article)
        db.session.commit()
        return make_response(
            {"message": "Delete"}, 202
        )
    except Exception as e:
        print(f'delete articles exception::{e}')
        return make_response(
            {"message": "unable to process"}, 409
        )
