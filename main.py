from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:krask0swes1@localhost:5432/store2'

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


class BookModel(db.Model):
    __tablename__ = 'books'
    pk = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<{self.pk}> {self.title} from {self.author}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Books(Resource):
    def post(self):
        data = request.get_json()
        new_book = BookModel(**data)
        db.session.add(new_book)
        db.session.commit()
        return new_book.as_dict()


if __name__ == "__main__":
    app.run(debug=True)