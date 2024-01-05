from data.models import Wallet, BaseUser
from data.database import read_query, insert_query, update_query, delete_query


def create_first_wallet(wallet: Wallet, user_name):
    data = insert_query("INSERT INTO wallet (name, currency, balance), VALUES (?, ?, ?)",
                        (wallet.name, wallet.currency, wallet.balance))

    data2 = read_query("SELECT * FROM wallet WHERE id = ?"), (data,)
    temp_wallet = next((Wallet.from_query(*row) for row in data2), None)

    data3 = read_query("SELECT * FROM user WHERE name = ?"), (user_name,)
    temp_user = next((BaseUser.from_query(*row) for row in data3), None)

    result = insert_query("INSERT INTO wallet_access (wallet_id, user_id, spend_access, add_access) ,VALUES(?,?,?,?)"
                          , (temp_wallet.id, temp_user.id, True, True))
    return result


def create_wallet(wallet: Wallet):
    data = insert_query("INSERT INTO wallet (name, currency, balance), VALUES (?, ?, ?)",
                        (wallet.name, wallet.currency, wallet.balance))

    return data


def get_by_id(id):
    data = read_query("SELECT * FROM wallet WHERE id=?"), (id,)

    return next((Wallet.from_query(*row) for row in data), None)


def add_from_card(id, amount, user):
    wallet = read_query("SELECT * FROM wallet WHERE ")
    data = update_query("UPDATE wallet SET balance = ?")
    return
