from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    environmental_impact = db.Column(db.String(100))

class AddToBasketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=10)])
    submit = SubmitField('Add to Basket')

class CheckoutForm(FlaskForm):
    credit_card_number = StringField('Credit Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiry_date = StringField('Expiry Date (MM/YY)', validators=[DataRequired(), Length(min=5, max=5)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Pay Now')

@app.route('/')
def galleryPage():
    sort_by = request.args.get('sort_by', 'name')
    if sort_by == 'price':
        books = Book.query.order_by(Book.price).all()
    elif sort_by == 'environmental_impact':
        books = Book.query.order_by(Book.environmental_impact).all()
    else:
        books = Book.query.order_by(Book.name).all()
    return render_template('index.html', books=books)

@app.route('/book/<int:bookId>', methods=['GET', 'POST'])
def singleBookPage(bookId):
    book = Book.query.get(bookId)
    form = AddToBasketForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        
        basket = session.get('basket', [])
        basket.append({'book_id': bookId, 'quantity': quantity})
        session['basket'] = basket
        return redirect(url_for('basketPage'))
    return render_template('singlebook.html', book=book, form=form)

@app.route('/basket')
def basketPage():
    basket = session.get('basket', [])
    total_price = 0
    for item in basket:
        book = Book.query.get(item['book_id'])
        item['name'] = book.name
        item['price'] = book.price
        total_price += book.price * item['quantity']
    return render_template('basket.html', basket=basket, total_price=total_price)

@app.route('/remove_from_basket/<int:bookId>')
def removeFromBasket(bookId):
    if 'basket' in session:
        basket = session['basket']
        updated_basket = [item for item in basket if item['book_id'] != bookId]
        session['basket'] = updated_basket
        return redirect(url_for('basketPage'))
    return "Item not found in basket"

@app.route('/checkout', methods=['GET', 'POST'])
def checkoutPage():
    form = CheckoutForm()
    if form.validate_on_submit():
        session.pop('basket', None)  
        return redirect(url_for('checkout_confirmation'))
    return render_template('checkout.html', form=form)

@app.route('/checkout_confirmation')
def checkout_confirmation():
    return render_template('checkout_confirmation.html')

if __name__ == '__main__':
    app.run(debug=True)
