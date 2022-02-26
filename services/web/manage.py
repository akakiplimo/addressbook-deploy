from flask.cli import FlaskGroup

from project import app, db, AddressBookModel


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    db.session.add(AddressBookModel(first_name="Joy", last_name="Chemu", phone="716-729-930", email="jc@daktaribora.com", address="10 Miotoni Rd"))
    db.session.commit()

if __name__ == "__main__":
    cli()