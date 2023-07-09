from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

# each blueprint has its unique name
blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True)) # an instance of ItemSchema to validate multiple items
    def get(self):
        return ItemModel.query.all()

    # the 2nd argument item_data is payload from user
    # it would first pass through ItemSchema and would pass to the post() function after validation
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema) # response decorator should be deeper than input
    def post(self, item_data):
        item = ItemModel(**item_data) # "**" turns the dictionary into keyword arguments

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="An item with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item
    


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin previlege required.")

        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    # item_data in front of other parameters
    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        # if the item does not exist, need to pass an extra store_id
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item



