from data.models import BaseUser
from data.database import read_query, insert_query, update_query, delete_query


def create_user(user: BaseUser):
    data = insert_query("INSERT INTO user (email, password, name), VALUES(?,?,?)",
                        (user.email, user.password, user.name))

    return data


def get_by_id(id):
    data = read_query("SELECT * FROM user WHERE id=?", (id,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def get_by_email(email):
    data = read_query("SELECT * FROM user WHERE email=?", (email,))

    return next((BaseUser.create_base_user(*row) for row in data), None)
