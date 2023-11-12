from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

client = MongoClient('localhost',27017)
db = client.blog

# Declaracion para coleccion users
users_col = db.users
tags_col = db.tags
cats_col = db.categories
coms_col = db.comments

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
            "email": email,
            "articles": []
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
        tag = {
            "name": name
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
        tags_col.update_one({"_id": ObjectId(tag_id)}, {"$set": {"name": new_name}})
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
            return jsonify({'name': tag['name'], 'id': id})
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

# Categories -----------------------------------------

@app.route('/categories')
def categories():
    data = {
        "title": "Tags"
    }
    return render_template('/categories.html', data=data)

@app.route('/categories/addcat', methods =['GET','POST'])
def addCat():
    if request.method == 'POST':
        name = request.form['name']
        cat = {
            "name": name
        }
        cats_col.insert_one(cat)
        return redirect(url_for('addCat'))
    data = {
        "title": "Agregar Categoria",
        "db": users
    }
    return render_template('/categories/add.html',data=data)

@app.route('/categories/listcats')
def listCats():
    lista = list(cats_col.find())
    data={
        "title": "Listar Categorias",
        "db": lista
    }
    return render_template('/categories/list.html',data=data)

@app.route('/categories/editcat', methods=['POST','GET'])
def editCat():
    if request.method == 'POST':
        cat_id = request.form['id']
        new_name = request.form['name']
        cats_col.update_one({"_id": ObjectId(cat_id)}, {"$set": {"name": new_name}})
        return redirect(url_for('editCat'))
    data = {
        "title": "Editar Categoria"
    }
    return render_template('/categories/edit.html', data=data)


@app.route('/categories/searchcat', methods=['POST','GET'])
def searchCat():
    if request.method == 'POST':
        id = request.form['id']
        cat = cats_col.find_one({"_id": ObjectId(id)})
        if cat:
            return jsonify({'name': cat['name'],'id': id})
        else:
            return jsonify({'error': 'Categoria no encontrada'})

@app.route('/categories/deletecat', methods=['GET','DELETE'])
def deleteCat():
    if request.method == 'DELETE':
        id = request.form['id']
        cats_col.delete_one({"_id": ObjectId(id)})
        return redirect(url_for('deleteCat'))
    data={
        "title": "Eliminar Categoria",
        "db": tags
    }
    return render_template('/categories/delete.html', data=data)

#----------------------------------------------------

# Coments -------------------------------------------

@app.route('/comments')
def comments():
    data = {
        "title": "Comentarios"
    }
    return render_template('/comentarios.html', data=data)

@app.route('/comments/addcom', methods =['GET','POST'])
def addCom():
    if request.method == 'POST':
        iduser = request.form['iduser']
        idart = request.form['idart']
        text = request.form['text']
        com = {
            "iduser": iduser,
            "idart": idart,
            "text": text
        }
        coms_col.insert_one(com)
        return redirect(url_for('addCom'))
        
    users_list = list(users_col.find())
    arts_list = []
    for user in users_list:
        user_articles = user.get('articles', [])  # Obtener la lista de artículos del usuario
        arts_list.extend(user_articles)

    data = {
        "title": "Agregar Comentario",
        "db": users,
        "arts_list": arts_list,
        "users_list": users_list
    }
    return render_template('/comments/add.html',data=data)

@app.route('/comments/listcoms')
def listComs():
    lista = list(coms_col.find())
    data={
        "title": "Listar Categorias",
        "db": lista
    }
    return render_template('/comments/list.html',data=data)

@app.route('/comments/editcom', methods=['POST','GET'])
def editCom():
    if request.method == 'POST':
        com_id = request.form['id']
        text = request.form['text']
        coms_col.update_one({"_id": ObjectId(com_id)}, {"$set": {"text": text}})
        return redirect(url_for('editCom'))
    data = {
        "title": "Editar Comentario"
    }
    return render_template('/comments/edit.html', data=data)

@app.route('/comments/searchcom', methods=['POST','GET'])
def searchCom():
    if request.method == 'POST':
        id = request.form['id']
        com = coms_col.find_one({"_id": ObjectId(id)})
        if com:
            return jsonify({'iduser': com['iduser'], 'idart': com['idart'], 'text': com['text'], 'id': id})
        else:
            return jsonify({'error': 'Comentario no encontrada'})

@app.route('/comments/deletecom', methods=['GET','DELETE'])
def deleteCom():
    if request.method == 'DELETE':
        id = request.form['id']
        coms_col.delete_one({"_id": ObjectId(id)})
        return redirect(url_for('deleteCom'))
    data={
        "title": "Eliminar Comentario",
        "db": tags
    }
    return render_template('/comments/delete.html', data=data)
#-------------------------------------------------------

# Articulos-----------------------------------------------

@app.route('/articles')
def articles():
    data = {
        "title": "Articulos"
    }
    return render_template('/articles.html', data=data)

@app.route('/articles/addart', methods =['GET','POST'])
def addArt():
    if request.method == 'POST':
        date = str(datetime.now())
        title = request.form['title']
        text = request.form['text']
        userid = request.form['iduser']
        tagid = request.form['idtag']
        catid = request.form['idcat']
        art = {
            "title": title,
            "text": text,
            "date": date,
            "tagid": tagid,
            "catid": catid
        }
        users_col.update_one({"_id": ObjectId(userid)}, {"$push": {"articles": art}})
        return redirect(url_for('addArt'))
    users_list = list(users_col.find())
    tags_list = list(tags_col.find())
    cats_list = list(cats_col.find())
    data = {
        "title": "Agregar Articulo",
        "db": users,
        "users_list": users_list,
        "tags_list": tags_list,
        "cats_list": cats_list
    }
    return render_template('/articles/add.html',data=data)

@app.route('/articles/listarts')
def listArts():
    # Obtener todos los usuarios
    users_list = list(users_col.find())

    # Inicializar una lista para almacenar todos los artículos
    all_articles = []

    # Recorrer cada usuario y obtener sus artículos
    for user in users_list:
        user_articles = user.get('articles', [])  # Obtener la lista de artículos del usuario
        all_articles.extend(user_articles)

    # Crear el objeto 'data' con la lista completa de artículos
    data = {
        "title": "Listar Articulos",
        "db": all_articles
    }

    return render_template('/articles/list.html', data=data)




@app.route('/articles/editart', methods=['POST','GET'])
def editArt():
    if request.method == 'POST':
        art_id = request.form['id']
        new_title = request.form['title']
        new_text = request.form['text']
        arts_col.update_one({"_id": ObjectId(art_id)}, {"$set": {"title": new_title, "text": new_text}})
        return redirect(url_for('editArt'))
    data = {
        "title": "Editar Articulo"
    }
    return render_template('/articles/edit.html', data=data)

@app.route('/articles/searchart', methods=['POST','GET'])
def searchArt():
    if request.method == 'POST':
        id = request.form['id']
        art = arts_col.find_one({"_id": ObjectId(id)})
        if art:
            return jsonify({'title': art['title'], 'text': art['text'], 'id': id})
        else:
            return jsonify({'error': 'Articulo no encontrada'})

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)