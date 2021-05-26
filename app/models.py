from app import db
from app import login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(64), index=True, unique=True)
    mail = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(64), index=True)
    password_hash=db.Column(db.String(128))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'login': self.login,
            'mail': self.mail}

        return data


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

    
