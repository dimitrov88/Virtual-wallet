from data.models import BaseUser
from data.database import read_query, insert_query, update_query, delete_query


def create_user(user: BaseUser):
    data = insert_query("INSERT INTO user (email, password, name) VALUES(?,?,?)",
                        (user.email, user.password, user.name))

    return data


def get_by_id(id):
    data = read_query("SELECT * FROM user WHERE id=?", (id,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def get_by_email(email):
    data = read_query("SELECT * FROM user WHERE email=?", (email,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def get_by_name(name):
    data = read_query("SELECT * FROM user WHERE name=?", (name,))

    return next((BaseUser.create_base_user(*row) for row in data), None)


def add_contact(user1_id, user2_id):
    data = insert_query("INSERT INTO contacts (user_id1, user_id2) VALUES(?,?)", (user1_id, user2_id))

    return data


def get_all_contacts_by_id(id):
    data = read_query("SELECT u.id, u.email, u.password, u.name FROM user u "
                      "JOIN contacts c  ON (c.user_id1 = u.id OR c.user_id2 = u.id) "
                      "WHERE c.user_id1 = ? and u.id != ?;", (id, id))

    return (BaseUser.create_base_user(*row) for row in data)



def remove_contact_by_id(id, current_user_id: int):
    data = update_query("DELETE FROM contacts WHERE user_id1 = ? and user_id2 = ? or user_id2 = ? and user_id1 = ?",
                        (id, current_user_id, id, current_user_id))

    return data