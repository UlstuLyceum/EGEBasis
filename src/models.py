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
    reset_code = fields.StringField(default="")
    is_admin = fields.BooleanField(default=False)
    is_math_basic = fields.BooleanField(default=True)

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
    cods = fields.ListField(fields.StringField)
    description = fields.StringField()
    count_of_tasks = fields.IntegerField(default=0)
    subject = fields.ReferenceField(Subject)


@instance.register
class Text(Document):

    body = fields.StringField(required=True)


@instance.register
class Task(Document):

    task_type = fields.ReferenceField(TaskType)
    description = fields.StringField()
    options = fields.ListField(fields.StringField)
    answers = fields.ListField(fields.StringField)
    explanation = fields.StringField()
    text = fields.ReferenceField(Text, allow_none=True)


@instance.register
class TaskTypeLink(Document):

    task_type = fields.ReferenceField(TaskType)
    user = fields.ReferenceField(User)
    status = fields.IntegerField(default=0)
    done_tasks = fields.IntegerField(default=0)


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
Text.ensure_indexes()
