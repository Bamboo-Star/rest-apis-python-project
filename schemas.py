from marshmallow import Schema, fields

class PainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class ItemSchema(PainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PainStoreSchema(), dump_only=True)
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

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)