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
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) # Foreign key
    name = db.Column(db.String(100), nullable = False)
    code = db.Column(db.String(10), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable = False) # Foreign key
    price = db.Column(db.Integer, nullable = False)
    image = db.Column(db.String(255), nullable = True)

    # Relationship with Category
    category = db.relationship('Category', backref='products', lazy=True)

    # Create the object -> constructor
    def __init__(self, created_by, name, code, category_id, price, image):
        self.created_by = created_by
        self.code = code
        self.name = name
        self.category_id = category_id
        self.price = price
        self.image = image

    # Get user data -> representation
    def __repr__(self):
        return f"{self.name}"
    
class Inventory(db.Model):
    # Table columns
    id = db.Column(db.Integer, primary_key = True) # Primary key
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False) # Foreign key
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False) # Foreign key
    inflows = db.Column(db.Integer, nullable = False)
    outflows = db.Column(db.Integer, nullable = True, default = 0)
    stock = db.Column(db.Integer, nullable = False, default = 0)

    # Relationship with Product
    product = db.relationship('Product', backref='inventory', lazy=True)

    # Create the object -> constructor
    def __init__(self, created_by, product_id, inflows, outflows = 0):
        self.created_by = created_by
        self.product_id = product_id
        self.inflows = int(inflows)
        self.outflows = int(outflows)
        self.stock = self.inflows - self.outflows

    # Get user data -> representation
    def __repr__(self):
        return f"{self.name}"
class Customer(db.Model):
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