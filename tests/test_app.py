import pytest
from app import app, db, Expense
from datetime import datetime, date

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing forms if used (not used here but good practice)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_create_expense(client):
    """Test creating a new expense."""
    response = client.post('/add', data={
        'title': 'Test Expense',
        'amount': '50.00',
        'category': 'Food',
        'spent_on': '2023-10-27',
        'description': 'Lunch'
    }, follow_redirects=True)

    # Check if redirect to index occurred (status code 200 after following redirect)
    assert response.status_code == 200
    
    # Verify data in database
    with app.app_context():
        expense = db.session.execute(db.select(Expense).filter_by(title='Test Expense')).scalar_one()
        assert expense is not None
        assert expense.amount == 50.00
        assert expense.category == 'Food'
        assert expense.spent_on == date(2023, 10, 27)

def test_update_expense(client):
    """Test updating an existing expense."""
    # Create an initial expense
    with app.app_context():
        expense = Expense(
            title='Old Title', 
            amount=100.0, 
            category='Travel', 
            spent_on=date(2023, 1, 1),
            description='Old Desc'
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # Update the expense
    response = client.post(f'/edit/{expense_id}', data={
        'title': 'New Title',
        'amount': '150.00',
        'category': 'Utilities',
        'spent_on': '2023-12-31',
        'description': 'New Desc'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verify changes in database
    with app.app_context():
        updated_expense = db.session.get(Expense, expense_id)
        assert updated_expense.title == 'New Title'
        assert updated_expense.amount == 150.00
        assert updated_expense.category == 'Utilities'
        assert updated_expense.spent_on == date(2023, 12, 31)
        assert updated_expense.description == 'New Desc'

def test_delete_expense(client):
    """Test deleting an expense."""
    # Create an expense to delete
    with app.app_context():
        expense = Expense(
            title='To Delete', 
            amount=10.0, 
            category='Other', 
            spent_on=date.today()
        )
        db.session.add(expense)
        db.session.commit()
        expense_id = expense.id

    # Delete the expense
    response = client.post(f'/delete/{expense_id}', follow_redirects=True)
    assert response.status_code == 200

    # Verify it's gone from database
    with app.app_context():
        deleted_expense = db.session.get(Expense, expense_id)
        assert deleted_expense is None
