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


@instance.register
class Subject(Document):

    name = fields.StringField(required=True, unique=True)
    label = fields.StringField(required=True)
    hidden = fields.BooleanField(default=False)


@instance.register
class TaskType(Document):

    number = fields.StringField(required=True, unique=True)
    points = fields.IntegerField(required=True, default=1)

    subject = fields.ReferenceField(Subject)


@instance.register
class Task(Document):

    task_type = fields.ReferenceField(TaskType)


@instance.register
class TaskTypeLink(Document):

    task_type = fields.ReferenceField(TaskType)
    user = fields.ReferenceField(User)
    status = fields.IntegerField(default=0)


@instance.register
class TaskLink(Document):

    task = fields.ReferenceField(Task)
    user = fields.ReferenceField(User)
    done = fields.BooleanField(default=False)


User.ensure_indexes()
Subject.ensure_indexes()
TaskType.ensure_indexes()
Task.ensure_indexes()
TaskTypeLink.ensure_indexes()
TaskLink.ensure_indexes()
