# Imports 
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# My App
app = Flask(__name__)


# Configure database SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)




# Data Class - Row of data

class GroceryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, default=0)
    category = db.Column(db.String(20))
    shopper = db.Column(db.String(20))
    time = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"item {self.id}"
    




# Takes the information puts in database then sends it back 
@app.route("/", methods=["GET", "POST"])
def index():
    # Add a purchase
    if request.method == "POST":
        amount = request.form['amount']
        category = request.form['category']
        shopper = request.form['shopper']
        new_purchase = GroceryItem(
            amount=amount,
            category=category,
            shopper=shopper
        )
        try:
            db.session.add(new_purchase)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR:{e}")
            return f"ERROR:{e}"
        
    # see all purchases
    else:
        items = GroceryItem.query.order_by(GroceryItem.time).all()
        return render_template("index.html", items=items)
    
    
















if __name__ in "__main__":
    with app.app_context():
        db.create_all
    app.run(debug=True)