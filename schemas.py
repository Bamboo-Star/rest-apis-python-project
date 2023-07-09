from marshmallow import Schema, fields

# an instance of either ItemModel or StoreModel contains a nested model of the other
# ItemSchema and StoreSchema need mutual and non-recursive nesting
# so need PainItemSchema and PainStoreSchema

class PainItemSchema(Schema):

    # should this field be used when loading data from request or returning data from our api?
    id = fields.Int(dump_only=True) # we generate the field by ourselves, so only required for returning data inside api
    name = fields.Str(required=True) # require for both ends
    price = fields.Float(required=True)

class PainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):

    # name and price are not required
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # automatically load store data
    store = fields.Nested(PainStoreSchema(), dump_only=True) # Nested to present relationships between objects
    tags = fields.List(fields.Nested(PainTagSchema()), dump_only=True)

class StoreSchema(PainStoreSchema):
    items = fields.List(fields.Nested(PainItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PainTagSchema(), dump_only=True))

class TagSchema(PainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PainTagSchema(), dump_only=True)
    items = fields.List(fields.Nested(PainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    # never return the password to client
    # if we remove load_only=True and get user again, can see hashed password in the result