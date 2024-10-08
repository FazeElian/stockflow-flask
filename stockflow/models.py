from stockflow import db

class User(db.Model):
    # Table columns
    id = db.Column(db.Integer, primary_key = True) # Primary key
    email = db.Column(db.String(255), unique = True, nullable = False)
    username = db.Column(db.String(20), unique = True, nullable = False)
    names = db.Column(db.String(50), nullable = True, default="")
    last_names = db.Column(db.String(50), nullable = True, default="")
    password = db.Column(db.Text, nullable = False)
    profile_photo = db.Column(db.String(255), nullable=True, default="")

    # Create the object -> constructor
    def __init__(self, email, username, password, names = "", last_names = "", profile_photo = ""):
        self.email = email
        self.names = names
        self.last_names = last_names
        self.profile_photo = profile_photo
        self.username = username
        self.password = password

    # Get user data -> representation
    def __repr__(self):
        return f"{self.username}"
    
class Category(db.Model):
    # Table columns
    id = db.Column(db.Integer, primary_key = True) # Primary key
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) # Foreign key
    name = db.Column(db.String(50), unique = True, nullable = False)
    description = db.Column(db.String(255), default='Sin descripción')

    # Create the object -> constructor
    def __init__(self, created_by, name, description = "Sin descripción"):
        self.created_by = created_by
        self.name = name
        self.description = description

    # Get user data -> representation
    def __repr__(self):
        return f"{self.id}"
    
class Product(db.Model):
    # Table columns
    id = db.Column(db.Integer, primary_key = True) # Primary key
    name = db.Column(db.String(100), nullable = False)
    category = db.Column(db.Integer, db.ForeignKey("category.name"), nullable = False) # Foreign key
    description = db.Column(db.String(255), default='Sin descripción')
    price = db.Column(db.Integer, nullable = False)
    image = db.Column(db.String(255), nullable=True, default="")

    # Create the object -> constructor
    def __init__(self, name, category, price, description = "Sin descripción", image = ""):
        self.name = name
        self.category = category
        self.price = price
        self.description = description
        self.image = image

    # Get user data -> representation
    def __repr__(self):
        return f"{self.name}"