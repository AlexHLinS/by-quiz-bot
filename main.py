import logging
from typing import Dict

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import crud, schema, SessionLocal, engine

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%H:%M:%S')

schema.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return dict(message="use /docs to get documentation")


# user/add
@app.post("/user/add/{user_id}")
async def add_user(user_id: int, db: Session = Depends(get_db)) -> Dict[str, str | bool | int]:
    """
    Добавление id пользователя в систему
    :param db:
    :param user_id: идентификатор пользователя в Telegram \n
    :return: при успешном добавлении возвращает данные пользователя либо ошибку в случае отсутствия пользователя в базе
    """
    user = crud.get_user_info(db, user_id)
    if user:
        return HTTPException(status_code=409, detail='User already exists!')
    user = crud.add_user_to_db(db, user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='Current user does not exist.')


# /user/status
@app.get("/user/status/{user_id}")
async def get_user_status(user_id: int, db: Session = Depends(get_db)) -> Dict[str, str | bool | int]:
    """
    Получение статуса пользователя по id
    :param db:
    :param user_id: идентификатор пользователя в Telegram \n
    :return: возвращает данные пользователя либо ошибку в случае отсутствия пользователя в базе
    """
    user = crud.get_user_info(db, user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail='Current user does not exist.')


# balance/get
@app.get("/user/balance/{user_id}")
async def get_user_balance(user_id: int, db: Session = Depends(get_db)) -> Dict[str, str | int]:
    """
    Возвращает баланс пользователя
    :param user_id: идентификатор пользователя в Telegram \n
    :return: баланс пользователя либо ошибка если такого нет в базе
    """
    user = crud.get_user_info(db, user_id)
    if user:
        return user.balance
    else:
        raise HTTPException(status_code=404, detail='Current user does not exist.')


# balance up
@app.put("/user/balance/credit/{user_id}/{amount}")
async def credit_user_balance(user_id: int, amount: int, db: Session = Depends(get_db)):
    """
    Увеличивает баланс пользователя
    :param user_id: идентификатор пользователя в Telegram,
    :param amount: сумма на которую увеличивается баланс
    :param db:
    :return: результат операции
    """
    return crud.credit_user_balance(db, user_id, amount)


# balance down
@app.put("/user/balance/debit/{user_id}/{admin_id}/{amount}")
async def debit_user_balance(user_id: int, amount: int, admin_id: int, db: Session = Depends(get_db)):
    """
    Списывает монеты с баланса пользователя
    :param user_id: идентификатор пользователя в Telegram,
    :param amount: сумма списания
    :param admin_id: идентификатор админа производящего списание в Telegram,
    :param db:
    :return: результат операции
    """
    return crud.debit_user_balance(db, user_id, admin_id, amount)


@app.put("/user/name/{user_id}/{user_name}")
async def set_user_name(user_id: int, user_name: str, db: Session = Depends(get_db)):
    """
    Устанавливает имя пользователя из ответа в викторине
    :param user_id:
    :param user_name:
    :param db:
    :return:
    """
    return crud.set_user_name(db, user_id, user_name)


@app.put("/user/account/{user_id}/{account}")
async def set_account_name(user_id: int, account: str, db: Session = Depends(get_db)):
    """
    Устанавливает имя пользователя из карточки пользователя в Телеграм
    :param user_id:
    :param account:
    :param db:
    :return:
    """
    return crud.set_account_name(db, user_id, account)


@app.put("/admin/add/{user_id}/{admin_id}")
async def add_admin(user_id: int, admin_id: int, db: Session = Depends(get_db)):
    """
    Добавляет пользователя с правами администратора
    :param user_id:
    :param admin_id:
    :param db:
    :return:
    """
    return crud.add_admin(db, user_id, admin_id)


@app.put("/user/position/{user_id}/{position}")
async def set_position(user_id: int, position: int, db: Session = Depends(get_db)):
    """
    Устанавливает позицию пользователя в викторине
    :param user_id:
    :param position:
    :param db:
    :return:
    """
    return crud.set_user_position(db, user_id, position)


@app.get("/user/position/{user_id}")
async def set_position(user_id: int, db: Session = Depends(get_db)):
    """
    Возвращает текущую позицию пользователя в викторине
    :param user_id:
    :param db:
    :return:
    """
    return crud.get_user_position(db, user_id)


@app.get('/users/show_table/')
async def show_users_table(db: Session = Depends(get_db)):
    """Возвращает содержимое таблицы Users"""
    return crud.show_users(db)


@app.get('/users/user_ids/account/{account}')
async def user_ids_by_account(account: str, db: Session = Depends(get_db)):
    """Возвращает все user_id соответствующие имени пользователя в Телеграм"""
    return crud.user_ids_by_account(db, account)


@app.get('/users/user_ids/quiz_name/{user_name}')
async def show_user_ids_by_quiz_name(user_name: str, db: Session = Depends(get_db)):
    """Возвращает все user_id соответствующие имени указанному в викторине"""
    return crud.show_user_ids_by_quiz_name(db, user_name)

@app.delete('/user/{user_id}')
async def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Удаляет пользователя по его user_id"""
    return crud.user_delete(db, user_id)
