from typing import Union, Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .schema import Users, Quiz_Data, Transactions

ModelInstances = Union[Users, Quiz_Data, Transactions]
ModelTypes = Union[Type[Users], Type[Quiz_Data], Type[Transactions]]


def get_user_info(db: Session, user_id: int):
    """Возвразает информацию по пользователю по его user_id"""
    return db.query(Users).filter(Users.user_id == user_id).first()


def add_user_to_db(db: Session, user_id: int):
    """Добавляет Telegram id пользователя в базу"""
    if user_id == 441179051:
        new_entry = Users(user_id=user_id, is_admin=True)
    else:
        new_entry = Users(user_id=user_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


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
    """Добавляет имя пользователя, указанное в викторине с привязкой к индитификатору"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.quiz_name = user_name
    db.commit()
    db.refresh(user)
    return user

def set_user_admin_mode(db: Session, user_id: int, admin_id: int, is_admin: bool):
    """Делает user_id администратором"""
    admin = db.query(Users).filter(Users.user_id == admin_id).first()
    if admin is None or not admin.is_admin:
        return HTTPException(status_code=403, detail='Only admin users are allowed to do this.')
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return None
    user.is_admin = is_admin
    db.commit()
    db.refresh(user)
    return user


def set_finished_user(db: Session, user_id: int, is_finished: bool):
    """Добавляет имя пользователя Телеграм в привязке к индитификатору"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.is_finished = is_finished
    db.commit()
    db.refresh(user)
    return user



def set_account_name(db: Session, user_id: int, account_name: str):
    """Добавляет имя пользователя Телеграм в привязке к индитификатору"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.account_name = account_name
    db.commit()
    db.refresh(user)
    return user


def add_admin(db: Session, user_id: int, admin_id: int):
    """Добавляет запись в базу с 'админскими' правами"""
    admin = db.query(Users).filter(Users.user_id == admin_id).first()
    if admin is None or not admin.is_admin:
        return HTTPException(status_code=403, detail='Only admin users are allowed to do this.')
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return None
    user = add_user_to_db(db, user_id)
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return user


def set_user_position(db: Session, user_id: int, position: int):
    """Устанавливает текущую позицию пользователя в квесте"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    user.quest_num = position
    db.commit()
    db.refresh(user)
    return user


def get_user_position(db: Session, user_id: int):
    """Возвращает текущую позицию пользователя в квесте"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail='User not found')
    return user.quest_num


def show_users(db: Session):
    """Возвращает содержимое таблицы User"""
    users = db.query(Users).all()
    if users is None:
        return HTTPException(status_code=404, detail='No data to display.')
    return users


def show_user_ids_by_account(db: Session, account_name: str):
    """Возвращает все user_id соответствующие нику в Телеграм"""
    users = db.query(Users).filter(Users.account_name == account_name).all()
    if users is None:
        return HTTPException(status_code=404, detail=f'Account name: {account_name} - not found.')
    return users.user_id


def show_user_ids_by_quiz_name(db: Session, quiz_name: str):
    """Возвращает все user_id соответствующие выбранному имени в викторине"""
    users = db.query(Users).filter(Users.quiz_name == quiz_name).all()
    if users is None:
        return HTTPException(status_code=404, detail=f'Quiz name: {quiz_name} - not found.')
    return users.user_id


def user_delete(db: Session, user_id: int):
    """Удаление пользователя по user_id"""
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if user is None:
        return HTTPException(status_code=404, detail=f'User id: {user_id} - not found.')
    db.delete(user)
    db.commit()
    users = db.query(Users).all()
    if users is None or len(users) < 1:
        return HTTPException(status_code=204, detail=f'Users table is empty.')
    return users
