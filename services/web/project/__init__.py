import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, 
            static_url_path='', 
            static_folder='media',
            template_folder='static')

app.config.from_object("project.config.Config")

db = SQLAlchemy(app)

class AddressBookModel(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    phone = db.Column(db.String())
    email = db.Column(db.String())
    address = db.Column(db.String())

    def __init__(self, first_name, last_name, phone, email, address):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address

    def __repr__(self):
        return f"{self.first_name}:{self.last_name}:{self.phone}:{self.email}:{self.address}"


@app.route('/', methods=['GET'])
def Index():
    if request.method == 'GET':
        contacts = AddressBookModel.query.all()
        results = [
            {
                "id": contact.id,
                "first_name": contact.first_name,
                "last_name": contact.last_name,
                "phone": contact.phone,
                "email": contact.email,
                "address": contact.address
            } for contact in contacts]
        # return {"count": len(results), "contacts": results}
        return render_template('index.html', contacts=results)

@app.route('/search', methods=['GET', 'POST'])
def search_filter():
    if request.method == 'POST':
        # filter_fname = AddressBookModel.query.filter(AddressBookModel.first_name.ilike())
        query = AddressBookModel.query
        filter_fname = request.form.get('filter_fname')
        query_result = query.filter(AddressBookModel.first_name == filter_fname)

        return render_template('index.html', contacts=query_result)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        data = request.form
        new_contact = AddressBookModel(first_name=data.get('first_name'), last_name=data.get('last_name'), phone=data.get('phone'), email=data.get('email'), address=data.get('address'))
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods=['GET', 'DELETE'])
def delete(id_data):
    contact = AddressBookModel.query.get_or_404(id_data)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('Index'))


@app.route('/update', methods=['POST', 'GET', 'PUT'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        update_contact = AddressBookModel.query.filter_by(id =id_data).first()
        update_contact.first_name=first_name
        update_contact.last_name=last_name
        update_contact.phone=phone
        update_contact.email=email
        update_contact.address=address

        # .update(dict(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address))
        db.session.commit()
        return redirect(url_for('Index'))


# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0')
