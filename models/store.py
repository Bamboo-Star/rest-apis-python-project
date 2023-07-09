from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    
    # back_populates tells SqlAlchemy which relationship name to link with when it joins the two tables
    # lazy="dynamic" caches and speeds up the program
    # cascade="all, delete" deletes the children (items) when we delete the parent (store)

    