from my_server import db, UserMixin, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_list = db.Table('user_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), nullable=False, primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    unique_string = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    price_type = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.String(100))
    description = db.Column(db.String(100))
    image = db.Column(db.String(100))
    link = db.Column(db.String(100))
    users = db.relationship('User', secondary=user_list, back_populates="products")

    def __repr__(self):
        return f'Name: {self.name}'

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    products = db.relationship('Product', secondary=user_list, back_populates="users")

    def __repr__(self):
        return f'Username: {self.username}'
