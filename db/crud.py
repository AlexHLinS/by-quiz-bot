from typing import Union, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .schema import Users, Quiz_Data, Transactions

ModelInstances = Union[Users, Quiz_Data, Transactions]
ModelTypes = Union[Type[Users], Type[Quiz_Data], Type[Transactions]]


def get_user_info(db: Session, user_id: int):
    return db.query(Users).filter(Users.user_id == user_id).first()


def add_user_to_db(db: Session, user_id: int):
    new_entry = Users(user_id=user_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


'''
def update_user_balance(db: Session, user_id: int, sender_id: int, debit: int, credit: int):
    sender = db.query(Users).filter(Users.user_id == sender_id).first()
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return None
    elif sender.is_admin and debit > 0 and user.balance >= debit:
        user.balance -= debit
    user.balance += credit
    db.commit()
    db.refresh(user)
    return user
'''


def credit_user_balance(db: Session, user_id: int, amount: int):
    """
    Увеличивает баланс
    :param db:
    :param user_id:
    :param amount:
    :return:
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    try:
        if user.balance:
            user.balance = int(user.balance) + abs(int(amount))
        else:
            user.balance = abs(int(amount))
        db.commit()
        db.refresh(user)
        return user
    except ValueError:
        return HTTPException(status_code=400, detail='Invalid amount')


def debit_user_balance(db: Session, user_id: int, admin_id: int, amount: int):
    """
    Списывает деньги у пользователям
    :param db:
    :param user_id:
    :param admin_id:
    :param amount:
    :return:
    """
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    admin = db.query(Users).filter(Users.user_id == admin_id).first()
    if admin is None:
        return HTTPException(status_code=403, detail='Only admin can debit user\'s balance.')
    try:
        if user.balance:
            user.balance = int(user.balance) - abs(int(amount))
        else:
            raise ValueError
        db.commit()
        db.refresh(user)
        return user
    except ValueError:
        return HTTPException(status_code=400, detail='Invalid amount')


def set_user_name(db: Session, user_id: int, user_name: str):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.quiz_name = user_name
    db.commit()
    db.refresh(user)
    return user


def set_account_name(db: Session, user_id: int, account_name: str):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.account_name = account_name
    db.commit()
    db.refresh(user)
    return user


def add_admin(db: Session, user_id: int, admin_id: int):
    admin = db.query(Users).filter(Users.user_id == admin_id).first()
    if admin is None or not admin.is_admin:
        return HTTPException(status_code=403, detail='Only admin users are allowed to do this.')
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        user = add_user_to_db(db, user_id)
        user.is_admin = True
        db.commit()
        db.refresh(user)
        return user
    return None


def set_user_position(db: Session, user_id: int, position: int):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.quest_num = position
    db.commit()
    db.refresh(user)
    return user


def get_user_position(db: Session, user_id: int):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    return user.quest_num
