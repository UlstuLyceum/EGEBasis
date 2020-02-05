from pymongo import MongoClient
from umongo import Document, Instance, fields

try:
    import src.local_config as config
except ImportError:
    import src.config as config

db = MongoClient(config.DB_HOST)[config.DB_NAME]
instance = Instance(db)


@instance.register
class User(Document):

    name = fields.StringField(required=True)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField()
    confirm_code = fields.StringField()

    class Meta:
        collection = db.user


User.ensure_indexes()
