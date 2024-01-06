from data.database import read_query, insert_query, update_query, delete_query
from data.models import Transactions, TransactionResponse


def get_by_id(id):
    data = read_query("SELECT * FROM transaction WHERE id=?"), (id,)

    return next((Transactions.from_query(*row) for row in data), None)


def get_by_username(name):
    data = read_query(f"SELECT t.id, s.name, r.name, t.amount, c.name, t.date FROM transaction t "
                      "JOIN user s on s.id = t.sender_id "
                      "JOIN user r on r.id = t.receiver_id "
                      "JOIN currency c on c.id = t.currency_id "
                      f"WHERE s.name = '{name}' or r.name='{name}'")

    return (TransactionResponse.from_query(*row) for row in data)


