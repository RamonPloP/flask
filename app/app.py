from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('localhost',27017)
db = client.blog

# Declaracion para coleccion users
users_col = db.users
tags_col = db.tags

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

@app.route('/users/adduser', methods =['GET','POST'])
def addUser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = {
            "name": name,
            "email": email
        }
        users_col.insert_one(user)
        return redirect(url_for('addUser'))
    data = {
        "title": "Agregar usuario",
        "db": users
    }
    return render_template('/users/add.html',data=data)

@app.route('/users/listusers')
def listUsers():
    lista = list(users_col.find())
    data={
        "title": "Listar Usuario",
        "db": lista
    }
    return render_template('/users/list.html',data=data)

@app.route('/users/edituser', methods=['POST','GET'])
def editUser():
    if request.method == 'POST':
        user_id = request.form['id']
        new_name = request.form['name']
        new_email = request.form['email']
        users_col.update_one({"_id": ObjectId(user_id)}, {"$set": {"name": new_name, "email": new_email}})
        return redirect(url_for('editUser'))
    data = {
        "title": "Editar Usuario"
    }
    return render_template('/users/edit.html', data=data)


@app.route('/users/searchuser', methods=['POST','GET'])
def searchUser():
    if request.method == 'POST':
        id = request.form['id']
        user = users_col.find_one({"_id": ObjectId(id)})
        if user:
            return jsonify({'name': user['name'], 'email': user['email'], 'id': id})
        else:
            return jsonify({'error': 'Usuario no encontrado'})

@app.route('/users/deleteuser', methods=['GET','DELETE'])
def deleteUser():
    if request.method == 'DELETE':
        id = request.form['id']
        users_col.delete_one({"_id": ObjectId(id)})
        return redirect(url_for('deleteUser'))
    data={
        "title": "Eliminar Usuario",
        "db": users
    }
    return render_template('/users/delete.html', data=data)
#---------------------------------------


# Tags ---------------------------------------------

@app.route('/tags')
def tags():
    data = {
        "title": "Tags"
    }
    return render_template('/tags.html', data=data)

@app.route('/tags/addtag', methods =['GET','POST'])
def addTag():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        tag = {
            "name": name,
            "url": url
        }
        tags_col.insert_one(tag)
        return redirect(url_for('addTag'))
    data = {
        "title": "Agregar Tag",
        "db": users
    }
    return render_template('/tags/add.html',data=data)

@app.route('/tags/listtags')
def listTags():
    lista = list(tags_col.find())
    data={
        "title": "Listar Tag",
        "db": lista
    }
    return render_template('/tags/list.html',data=data)

@app.route('/tags/edittag', methods=['POST','GET'])
def editTag():
    if request.method == 'POST':
        tag_id = request.form['id']
        new_name = request.form['name']
        new_url = request.form['url']
        tags_col.update_one({"_id": ObjectId(tag_id)}, {"$set": {"name": new_name, "tag": new_url}})
        return redirect(url_for('editTag'))
    data = {
        "title": "Editar Tag"
    }
    return render_template('/tags/edit.html', data=data)


@app.route('/tags/searchtag', methods=['POST','GET'])
def searchTag():
    if request.method == 'POST':
        id = request.form['id']
        tag = tags_col.find_one({"_id": ObjectId(id)})
        if tag:
            return jsonify({'name': tag['name'], 'url': tag['url'], 'id': id})
        else:
            return jsonify({'error': 'Tag no encontrado'})

@app.route('/tags/deletetag', methods=['GET','DELETE'])
def deleteTag():
    if request.method == 'DELETE':
        id = request.form['id']
        tags_col.delete_one({"_id": ObjectId(id)})
        return redirect(url_for('deleteTag'))
    data={
        "title": "Eliminar Tag",
        "db": tags
    }
    return render_template('/tags/delete.html', data=data)

#----------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)