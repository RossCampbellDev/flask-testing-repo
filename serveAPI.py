import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
db.create_all()

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(250))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
        return 'hello!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    result = []

    for drink in drinks:
        drink_data = {'name': drink.name, 'desc': drink.description}
        result.append(drink_data)

    return {"drinks": result}


@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return {"name": drink.name, "description": drink.description}


@app.route('/drinks', methods=['POST'])
def add_drink():
    print(request.data.decode())
    req = json.loads(request.data.decode())
    drink = Drink(name=req['name'],
            description=req['description'])
    db.session.add(drink)
    db.session.commit()

    return {'id': drink.id}


@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get_or_404(id)
    if drink is None:
        return {"error": "not found"}
    db.session.delete(drink)
    db.session.commit()
    return f"{drink.name} deleted"
