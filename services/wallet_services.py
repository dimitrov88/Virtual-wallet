from data.models import Wallet, BaseUser, Currency, WalletResponse
from data.database import read_query, insert_query, update_query, delete_query
from typing import Optional, Union


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


def create_wallet(wallet: Wallet, user):
    temp_currency = read_query("SELECT * FROM currency WHERE name=?", (wallet.name,))

    data = insert_query("INSERT INTO wallet (name, balance, currency_id, user_id) VALUES (?, ?, ?, ?)",
                        (wallet.name, wallet.balance, temp_currency, user))

    return data


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


def get_by_email(email):
    data = read_query("SELECT w.id, w.name, w.balance, w.currency_id, w.user_id FROM wallet w"
                      " JOIN user u on u.id = w.user_id "
                      " WHERE u.email=?", (email,))

    return next((Wallet.from_query(*row) for row in data), None)


def make_transaction(sender: Union[Wallet, WalletResponse], receiver: Union[Wallet, WalletResponse], amount):
    to_remove = sender.balance - amount
    to_add = receiver.balance + amount
    send = update_query("UPDATE wallet SET balance = ? WHERE id = ?", (to_remove, sender.id))
    add = update_query("UPDATE wallet SET balance = ? WHERE id = ?", (to_add, receiver.id))
    transaction = insert_query("INSERT INTO transaction (sender_id, receiver_id, amount, currency_id) VALUES(?,?,?,?)",
                               (sender.user_id, receiver.user_id, amount, sender.currency_id))

    wallet_action = insert_query("INSERT INTO wallet_transaction (wallet_id1, wallet_id2, transaction_id) VALUES(?,?,?)",
                                 (sender.id, receiver.id, transaction))

    return wallet_action


def add_from_card(wallet, amount):
    to_add = wallet.balance + amount

    data = update_query("UPDATE wallet SET balance = ? "
                        "WHERE id = ?", (to_add, wallet.id))

    return data
