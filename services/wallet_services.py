from data.models import Wallet, BaseUser, Currency, WalletResponse
from data.database import read_query, insert_query, update_query, delete_query
from typing import Optional, Union
from flask_login import LoginManager, current_user


def create_first_wallet(wallet: Wallet, user_name):
    data3 = read_query("SELECT * FROM user WHERE name = ?", (user_name,))
    temp_user = next((BaseUser.create_base_user(*row) for row in data3), None)

    new_wallet = insert_query("INSERT INTO wallet (name, balance, currency_id, user_id) VALUES (?, ?, ?, ?)",
                              (wallet.name, wallet.balance, 1, temp_user.id))

    data2 = read_query("SELECT * FROM wallet WHERE id = ?", (new_wallet,))

    temp_wallet = next((Wallet.from_query(*row) for row in data2), None)

    result = insert_query("INSERT INTO wallet_access (wallet_id, user_id, spend_access, add_access) VALUES(?,?,?,?)"
                          , (temp_wallet.id, temp_user.id, True, True))
    return result


# def create_wallet(wallet: Wallet, user):
#     temp_currency = read_query("SELECT * FROM currency WHERE name=?", (wallet.name,))
#
#     data = insert_query("INSERT INTO wallet (name, balance, currency_id, user_id) VALUES (?, ?, ?, ?)",
#                         (wallet.name, wallet.balance, temp_currency, user))
#
#     return data


def get_by_id(id):
    data = read_query("SELECT * FROM wallet WHERE id=?", (id,))

    return next((Wallet.from_query(*row) for row in data), None)


def get_by_user_name(name):
    data = read_query("SELECT w.id, w.name, w.balance, c.name, u.name FROM wallet w "
                      "JOIN user u on w.user_id = u.id "
                      "JOIN currency c on c.id = w.currency_id "
                      "WHERE u.name=?", (name,))

    return next((WalletResponse.from_query(*row) for row in data), None)


def get_by_user_id(id):
    data = read_query("SELECT * FROM wallet WHERE user_id=?", (id,))

    return next((Wallet.from_query(*row) for row in data), None)


def get_all_by_user_id(id):
    data = read_query("SELECT * FROM wallet WHERE user_id=?", (id,))

    return (Wallet.from_query(*row) for row in data)


def get_all_by_access(user_id):
    wallet_ids = read_query(f"SELECT id FROM wallet WHERE user_id = {user_id}")
    wallet_ids = [row[0] for row in wallet_ids]

    if not wallet_ids:
        # Return an empty list or handle the case where there are no wallet IDs
        return []

    data = read_query(f"SELECT w.id, w.name, w.balance, c.name, u.name FROM wallet w "
                      "JOIN wallet_access wa on wa.wallet_id = w.id "
                      "JOIN user u on wa.user_id = u.id "
                      "JOIN currency c on c.id = w.currency_id "
                      f"WHERE wa.wallet_id IN ({','.join(map(str, wallet_ids))}) "
                      "AND wa.spend_access = ? AND wa.add_access = ? "
                      "AND wa.user_id != ?", (True, True, user_id))

    return [WalletResponse.from_query(*row) for row in data]


def add_access(wallet_id, user_id):
    data = insert_query("INSERT INTO wallet_access (wallet_id, user_id, spend_access, add_access) VALUES(?, ?, ?, ?)",
                        (wallet_id, user_id, True, True))


def remove_access(wallet_id, user_name):
    data = update_query("DELETE FROM wallet_access "
                        "WHERE wallet_id = ? AND user_id IN (SELECT id FROM user WHERE name = ?)",
                        (wallet_id, user_name))

    return data


def get_by_email(email):
    data = read_query("SELECT w.id, w.name, w.balance, w.currency_id, w.user_id FROM wallet w"
                      " JOIN user u on u.id = w.user_id "
                      " WHERE u.email=?", (email,))

    return next((Wallet.from_query(*row) for row in data), None)


def get_by_wallet_name(name):
    data = read_query("SELECT * FROM wallet "
                      "WHERE name=?", (name,))

    return next((Wallet.from_query(*row) for row in data), None)


def make_transaction(sender: Union[Wallet, WalletResponse], receiver: Union[Wallet, WalletResponse], amount,
                     receiver_amount):
    to_remove = sender.balance - amount
    to_add = receiver.balance + receiver_amount
    send = update_query("UPDATE wallet SET balance = ? WHERE id = ?", (to_remove, sender.id))
    add = update_query("UPDATE wallet SET balance = ? WHERE id = ?", (to_add, receiver.id))
    transaction = insert_query("INSERT INTO transaction (sender_id, receiver_id, amount, currency_id) VALUES(?,?,?,?)",
                               (sender.user_id, receiver.user_id, receiver_amount, receiver.currency_id))
    if sender.user_id != current_user.id:
        transaction2 = insert_query(
            "INSERT INTO transaction (sender_id, receiver_id, amount, currency_id) VALUES(?,?,?,?)",
            (current_user.id, receiver.user_id, receiver_amount, receiver.currency_id))

    wallet_action = insert_query(
        "INSERT INTO wallet_transaction (wallet_id1, wallet_id2, transaction_id) VALUES(?,?,?)",
        (sender.id, receiver.id, transaction))

    return wallet_action


def get_all_wallets(user_id):
    data = read_query("SELECT w.id, w.name, w.balance, w.currency_id, w.user_id FROM wallet w "
                      "JOIN wallet_access wa on w.id = wa.wallet_id "
                      "WHERE wa.user_id = ? AND wa.spend_access = ? AND wa.add_access = ?", (user_id, True, True))
    return (Wallet.from_query(*row) for row in data)


def get_all_wallets_response(user_id):
    data = read_query("SELECT w.id, w.name, w.balance, c.name, u.name FROM wallet w "
                      "JOIN wallet_access wa on w.id = wa.wallet_id "
                      "JOIN user u on u.id = w.user_id "
                      "JOIN currency c on c.id = w.currency_id "
                      "WHERE wa.user_id = ? AND wa.spend_access = ? AND wa.add_access = ?", (user_id, True, True))
    return (WalletResponse.from_query(*row) for row in data)


def add_from_card(wallet, amount):
    to_add = wallet.balance + amount

    data = update_query("UPDATE wallet SET balance = ? "
                        "WHERE id = ?", (to_add, wallet.id))

    return data


def create_wallet(wallet: Wallet):
    data = insert_query("INSERT INTO wallet (name, balance, currency_id, user_id) VALUES(?,?,?, ?)",
                        (wallet.name, wallet.balance, wallet.currency_id, wallet.user_id))

    access = insert_query("INSERT INTO wallet_access (wallet_id, user_id, spend_access, add_access) VALUES(?,?,?,?)",
                          (data, wallet.user_id, True, True))

    return data
