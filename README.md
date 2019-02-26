#Pantry App Idea

## Endpoints

### User
Register a new user

Login

Logout

View User

#### Admin specific
Edit User 

Delete User

### Ingredients
View Ingredients (Pantry)

Add Ingredient

Delete Ingredient - use or spoilage

### Recipe
Search Recipe
	Search based on ingredients

Add Recipe

Edit Recipe

View Recipe

Delete Recipe


## Models

### User
		id: IntegerField()
		username: CharField()
		password: CharField()
		photo: CharField()

### Ingredient
		id: IntegerField(),
		name: CharField(),
		type: CharField(),
		expiration: DateField(),

### Recipe
		id: IntegerField(),
		title: CharField(),
		image_url: CharField(),
		source_url: CharField(),
		publisher: CharField(),
		publisher_url: CharField(),
		social_rank: CharField(),
		created_by: ForeignKeyField()

### Ingredient of User (Pantry)
		id: IntegerField(),
		ingedient_id: ForeignKeyField()
		user_id: ForeignKeyField()

### Ingredient in Recipe
		id: IntegerField(),
		recipe_id: ForeignKeyField()
		ingredient_id: ForeignKeyField()

### Recipe of User
		id: IntegerField(),
		user_id: ForeignKeyField()
		recipe_id: ForeignKeyField()

























