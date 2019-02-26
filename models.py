import datetime
import config
from peewee import *
from flask_bcrypt import generate_password_hash
from flask_login import UserMixin

DATABASE = SqliteDatabase('pantry.sqlite')

class User(UserMixin, Model):
	username: CharField(unique=True),
	password: CharField(),
	photo: CharField()

	class Meta:
		database = DATABASE

	@classmethod
	def create_user(cls, username, password, photo):
		try:
			cls.select().where(
				(cls.username==username)
				).get()
		except cls.DoesNotExist:
			user = cls(username=username)
			user.password = generate_password_hash(password)
			user.save()
			return user
		else:
			raise Exception("User with email or username already exists")


