from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(users_id):
    return users.query.get(users_id)

class users(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),index=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Name : {self.name} Username: {self.email} password : {self.password}"
