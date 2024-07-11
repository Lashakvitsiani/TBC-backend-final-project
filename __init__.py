from ext import app, db
from models import Product, User, Like

with app.app_context():
    db.create_all()

    admin_user = User("Lasha1", "lashakvitsiani5@gmail.com", "test1234", "admin")
    db.session.add(admin_user)
    db.session.commit()
  
