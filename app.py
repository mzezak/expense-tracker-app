from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Expense
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key_change_in_prod'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    expenses = db.session.execute(db.select(Expense).order_by(Expense.spent_on.desc())).scalars().all()
    # Calculate total
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=('GET', 'POST'))
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        spent_on_str = request.form['spent_on']
        description = request.form['description']
        
        try:
             spent_on = datetime.strptime(spent_on_str, '%Y-%m-%d').date()
        except ValueError:
             spent_on = datetime.today().date()

        expense = Expense(title=title, amount=amount, category=category, spent_on=spent_on, description=description)
        db.session.add(expense)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('form.html', action='Add')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_expense(id):
    expense = db.get_or_404(Expense, id)

    if request.method == 'POST':
        expense.title = request.form['title']
        expense.amount = float(request.form['amount'])
        expense.category = request.form['category']
        spent_on_str = request.form['spent_on']
        expense.description = request.form['description']
        
        try:
             expense.spent_on = datetime.strptime(spent_on_str, '%Y-%m-%d').date()
        except ValueError:
             pass # Keep original date if invalid

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('form.html', expense=expense, action='Edit')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id):
    expense = db.get_or_404(Expense, id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
