from flask import render_template, redirect, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import RegisterForm, LoginForm, EditUserForm
from models import Product, User, db, Like
from ext import app
from decorators import admin_required


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register.html', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

    return render_template('register.html', form=form)


@app.route("/login.html", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", form=form)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm(username=user.username, email=user.email, password=user.password)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data

        db.session.commit()
        return redirect("/registered_users.html")

    return render_template("Edit_user.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/store.html')
@login_required
def store():
    products = Product.query.all()
    return render_template('store.html', products=products)


@app.route('/News.html')
@login_required
def news():
    return render_template('News.html')


@app.route('/Album-AM.html')
@login_required
def album():
    return render_template('Album-AM.html')


@app.route("/Album-TBHC.html")
@login_required
def album2():
    return render_template("Album-TBHC.html")


@app.route("/Album-FWN.html")
@login_required
def album1():
    return render_template("Album-FWN.html")


@app.route("/Album-The_Car.html")
@login_required
def album3():
    return render_template("Album-The_Car.html")


@app.route("/Album-Currents.html")
@login_required
def album4():
    return render_template("Album-Currents.html")


@app.route("/Album-Ok_Computer.html")
@login_required
def album5():
    return render_template("/Album-Ok_Computer.html")


@app.route("/Album-Rammstein.html")
@login_required
def album6():
    return render_template("/Album-Rammstein.html")


@app.route("/Albums.html")
@login_required
def album8():
    return render_template("/Albums.html")


@app.route("/Album-The Slow Rush.html")
@login_required
def album7():
    return render_template("/Album-The Slow Rush.html")


@app.route("/add_product")
@admin_required
@login_required
def add_product():
    return render_template("add_product.html")


@app.route("/delete_user/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/registered_users.html")


@app.route("/product/<int:product_id>")
def product(product_id):
    product = Product.query.get(product_id)
    return render_template("product.html", product=product)


@app.route("/registered_users.html")
@admin_required
def users():
    registered_users = User.query.all()
    return render_template("/registered_users.html", registered_users=registered_users)


@app.route('/like', methods=['POST'])
@login_required
def like_product():
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        user_id = current_user.id

        if not product_id:
            return jsonify({'error': 'Missing product_id'}), 400

        # Check if the user has already liked the product
        existing_like = Like.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_like:
            return jsonify({'error': 'You have already liked this product'}), 400

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Record the like
        new_like = Like(user_id=user_id, product_id=product_id)
        db.session.add(new_like)
        product.likes += 1
        db.session.commit()

        return jsonify({'message': 'Like recorded', 'likes': product.likes}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
