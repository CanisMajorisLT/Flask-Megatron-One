__author__ = 'vyt'

from mainFlask import db, Queries,User
db.create_all()
usr = User('admin@admin.com', 'admin')
db.session.add(usr)
db.session.commit()

