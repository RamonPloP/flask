from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost',27017)
db = client.blog

# Declaracion para coleccion users
users_col = db.users

app = Flask(__name__)

@app.route('/')

def index():
    data = {
    "title": "Blog",
    "datos": [1,2,3,4,5]
}
    return render_template('index.html', data=data)

# Users ----------------------------
@app.route('/users')
def users():
    data = {
        "title": "Users"
    }
    return render_template('/users.html', data=data)

@app.route('/users/add', methods =['GET','POST'])
def add():
    if request.method == 'POST':
        print('dentro de if')
        name = request.form['name']
        email = request.form['email']
        user = {
            "name": name,
            "email": email
        }
        users_col.insert_one(user)
        print(user)
        return redirect(url_for('add'))
    data = {
        "title": "Agregar usuario",
        "db": users
    }
    return render_template('/users/add.html',data=data)

@app.route('/users/list')
def listUsers():
    lista = list(users_col.find())
    data={
        "title": "Listar Usuario",
        "db": lista
    }
    return render_template('/users/list.html',data=data)

@app.route('/users/edit', methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        user_id = request.form['id']
        new_name = request.form['name']
        new_email = request.form['email']
        users_col.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": new_name, "email": new_email}})
        return redirect(url_for('edit'))
    data = {
        "title": "Editar Usuario"
    }
    return render_template('/users/edit.html', data=data)


@app.route('/users/search', methods=['POST','GET'])
def search():
    if request.method == 'POST':
        id = request.form['id']
        user = users_col.find_one({"_id": ObjectId(id)})
        if user:
            return jsonify({'name': user['name'], 'email': user['email'], 'id': id})
        else:
            return jsonify({'error': 'Usuario no encontrado'})
            
@app.route('/users/delete', methods=['GET','DELETE'])
def delete():
    if request.method == 'DELETE':
        id = request.form['id']
        users_col.delete_one({"_id": ObjectId(id)})
        return redirect(url_for('delete'))
    data={
        "title": "Eliminar Usuario",
        "db": users
    }
    return render_template('/users/delete.html', data=data)
#---------------------------------------

if __name__ == '__main__':
    app.run(debug=True)