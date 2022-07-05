from sqlalchemy import Column, Integer, Boolean, DateTime, Text

from . import Base


class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=False)
    account_name = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
    quiz_name = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    is_admin = Column(Boolean, primary_key=False, unique=False, nullable=False, autoincrement=False)

    quest_num = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    balance = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    is_finished = Column(Boolean, primary_key=False, unique=False, nullable=False, autoincrement=False)


class Transactions(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    timestamp = Column(DateTime, primary_key=False, unique=False, nullable=False, autoincrement=False)

    user_id = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    admin_id = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)

    credit = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    debit = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)

    status = Column(Boolean, primary_key=False, unique=False, nullable=False, autoincrement=False)


class Quiz_Data(Base):
    __tablename__ = 'quiz_data'

    position = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)

    card_picture_path = Column(Text, primary_key=False, unique=False, nullable=True, autoincrement=False)
    card_text = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    question_text = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    is_chose_type = Column(Boolean, primary_key=False, unique=False, nullable=False, autoincrement=False)
    is_compare_type = Column(Boolean, primary_key=False, unique=False, nullable=False, autoincrement=False)

    answer_count = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)

    answer1 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
    prize1 = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    post_text1 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    answer2 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
    prize2 = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    post_text2 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    answer3 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
    prize3 = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    post_text3 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)

    answer4 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
    prize4 = Column(Integer, primary_key=False, unique=False, nullable=False, autoincrement=False)
    post_text4 = Column(Text, primary_key=False, unique=False, nullable=False, autoincrement=False)
