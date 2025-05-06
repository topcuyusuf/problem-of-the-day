from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Create Flask app
app = Flask(__name__)

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///problems.db'
db = SQLAlchemy(app)

# Define the Problem model
class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today)

# Create the database and tables (run once)
with app.app_context():
    db.create_all()

# Route to add a new problem
@app.route('/add', methods=['POST'])
def add_problem():
    data = request.get_json()
    new_problem = Problem(title=data['title'], content=data['content'])
    db.session.add(new_problem)
    db.session.commit()
    return jsonify({'message': 'Problem added successfully'})

# Route to get today’s problem
@app.route('/today', methods=['GET'])
def get_today_problem():
    today = date.today()
    problem = Problem.query.filter_by(date=today).first()
    if problem:
        return jsonify({'title': problem.title, 'content': problem.content})
    else:
        return jsonify({'message': 'No problem found for today'})

if __name__ == '__main__':
    app.run(debug=True)
