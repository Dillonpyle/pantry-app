import models
from flask_login import login_required
from flask_restful import Resource, Api, reqparse, fields, marshal, marshal_with, url_for
from flask import jsonify, Blueprint, abort


recipe_fields = {
	'title' = fields.String,
	'description' = fields.String,
	'image_url' = fields.String,
	'source_url' = fields.String,
	'publisher' = fields.String,
	'publisher_url' = fields.String,
	'social_rank' = fields.String,
	'created_by' = fields.Integer
}


