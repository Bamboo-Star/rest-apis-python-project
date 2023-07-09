'''
allow clients to
1. create stores, each with a name and a list of stocked items.
2. create an item within a store, each with a name and a price.
3. retrieve a list of all stores and their items.
4. given its name, retrieve an individual store and all its items.
5. given a store name, retrieve only a list of item within it.
'''

import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST
import models # sqlalchemy needs model to create tables

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__) # create a flask app

    app.config["PROPAGATE_EXCEPTIONS"] = True # raise errors
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3" # the standard api version to use
    app.config["OPENAPI_URL_PREFIX"] = "/" # where the route starts
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui" # see documentation in: http://localhost:5000/swagger-ui
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") # if-else
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config['JWT_SECRET_KEY'] = "94561599961646450988182109774598601486"
    jwt = JWTManager(app)


    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"description": "The token has been revoked.",
                     "error": "token_revoked"}),
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify({"description": "The token is not fres.",
                     "error": "fresh_token_required"}),
            401,
        )

    # add extra information to jwt when create it
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # need to look into the database and see who are admins
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.",
                     "error": "token_expired"}),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error): # if there is no jwt, use an error in argument
        return (
            jsonify({"message": "Sigature verification failed.",
                     "error": "invalid_token"}),
            401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"description": "Request does not contain an access token.",
                     "error": "authorization_required"}),
            401,
        )
    


    @app.before_first_request
    def create_tables():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app