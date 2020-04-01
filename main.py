from flask import Flask, Response, json, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dhiyo:dhiyo007@localhost:3306/flask_api'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), unique=True)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.String(150))

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.bio = bio

    @staticmethod
    def get_all_users():
        return User.query.all()


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username', 'email', 'bio')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/users", methods=["GET"])
def get_user():
    all_users = User.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
