import datetime
from peewee import *
from peewee import JOIN
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from playhouse.db_url import connect
import os



if 'HEROKU' in os.environ:
    DATABASE = connect(os.environ.get('DATABASE_URL'))
    db_proxy.initialize(db)
else:
    DATABASE = SqliteDatabase('mypantry.sqlite')
    ## uncomment below if you want to use postgress locally
    # import config
    # DATABASE = conn or PostgresqlDatabase(
    #     config.DATABASE_URI_PSQL,
    #     user=config.DATABASE_ADMIN,
    #     password=config.DATABASE_PASSWORD
    #     )

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password):
        try:
            cls.select().where(
                (cls.username == username)
            ).get()
        except cls.DoesNotExist:
            user = cls(username=username)
            user.password = generate_password_hash(password)
            user.save()
            return user
        else:
            raise Exception("User with email or username already exists")


class Ingredient(Model):
    name = TextField(default=None)
    typeof = TextField(default=None)

    class Meta:
        database = DATABASE

class Recipe(Model):
    title = CharField()
    description = CharField()
    image_url = CharField()
    created_by = ForeignKeyField(User)

    class Meta:
        database = DATABASE


class RecipeApi(Model):
    title = CharField()
    image_url = CharField()
    source_url = CharField()
    publisher = CharField()
    publisher_url = CharField()
    social_rank = CharField()
    created_by = ForeignKeyField(User)

    class Meta:
        database = DATABASE


class Pantry(Model):
    ingredient_id = ForeignKeyField(Ingredient)
    user_id = ForeignKeyField(User)
    quantity = IntegerField(default=1)
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class IngredientInRecipe(Model):
    recipe_id = ForeignKeyField(Recipe)
    ingredient_id = ForeignKeyField(Ingredient)
    amount = CharField()
    unit = CharField()

    class Meta:
        database = DATABASE


class RecipeOfUser(Model):
    user_id = ForeignKeyField(User)
    recipe_id = ForeignKeyField(Recipe)

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables(
        [User, Ingredient, Recipe, Pantry, IngredientInRecipe, RecipeOfUser], safe=True)
    DATABASE.close()
