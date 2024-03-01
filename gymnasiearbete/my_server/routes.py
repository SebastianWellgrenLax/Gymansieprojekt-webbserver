from sqlalchemy import null
from my_server import app, redirect, render_template, request, url_for, BeautifulSoup, urlopen, urlretrieve, json, requests, extension, db, flash, login_user, logout_user, current_user, login_required, uuid
from my_server.models import User, Product
from my_server.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/favorites')
def favorites():
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.get_id()).first()
        products = user.products
        return render_template('favorites.html', products=products)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.password == form.password.data:

            flash('Du är inloggad!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('index'))
        
        flash(f'Login unsuccessful!', 'warning')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)

        flash('Användaren är registrerad', 'success') 
        return redirect(url_for('index'))

    return render_template('register.html' , form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('Du är utloggad!', 'success')

    return redirect(url_for('index'))

@app.route('/product/add/<number>')
def product_add_int(number=''):
    url = "https://fakestoreapi.com/products/"
    page = requests.get(url+number)

    new_product = Product(
        unique_string = str(uuid.uuid4()),
        name = page.json()['title'],
        price = page.json()['price'],
        price_type = '$',
        rating = page.json()['rating']['rate'],
        image = page.json()['image'],
        description = page.json()['description'],
        link = url+number
    )
    db.session.add(new_product)
    db.session.commit()
    flash('Product succsesfully added!', 'success')

    return redirect(url_for('index'))

@app.route('/product/favorite', methods=['POST'])
def product_favorite():
    data = request.get_json()
    id = data['product']['id']

    product = Product.query.filter(Product.unique_string == id).first()

    if product == None:
        new_product = Product(
        unique_string = id,
        name = data['product']['name'],
        price = float(data['product']['price']),
        price_type = data['product']['price_type'],
        rating = data['product']['rating'],
        image = data['product']['image'],
        description = data['product']['description'],
        link = data['product']['link']
        )

        db.session.add(new_product)
        db.session.commit()

    if current_user.is_authenticated:
        
        product = Product.query.filter(Product.unique_string == id).first()
        user = User.query.filter(User.id == current_user.get_id()).first()

        product.users.append(user)

        db.session.add(product)
        db.session.commit()
    else:
        flash('Login to favorite products!', 'warning')
        return redirect(url_for('login'))

    return json.dumps("")


@app.route('/product/unfavorite', methods=['POST'])
def product_unfavorite():
    data = request.get_json()
    id = data['id']

    product = Product.query.filter(Product.unique_string == id).first()
    user = User.query.filter(User.id == current_user.get_id()).first()
    
    user.products.remove(product)
    #produkter finns kvar i databasen även om igen längre bevakar dem
    
    db.session.add(product)
    db.session.commit()

    return json.dumps("")

@app.route('/product/list/favorite', methods=['POST'])
def product_list():
    if current_user.is_authenticated:
        user = User.query.filter(User.id == current_user.get_id()).first()
        products = user.products
        list = []
        for product in products:
            list.append(product.unique_string)
        return json.dumps(list)
    return json.dumps("")