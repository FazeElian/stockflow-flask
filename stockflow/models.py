from stockflow import db

class User(db.Model):
    # Table columns
    id = db.Column(db.Integer, primary_key = True) # Primary key
    email = db.Column(db.String(255), unique = True, nullable = False) # Max length and unique property and not null
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)

    # Create the object -> constructor
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    # Get user data -> representation
    def __repr__(self):
        return f"{self.username}"