from vars_libs import db


class Words(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    words_group = db.Column('words_group', db.String)
    pl = db.Column('pl', db.String)
    foreign = db.Column('foreign', db.String)
    label_1 = db.Column('label_1', db.String)
    label_2 = db.Column('label_2', db.String)
    date = db.Column('date', db.Date)
    owner = db.Column('owner', db.String)

    def __init__(self, words_group, pl, foreign, label_1, label_2, date, owner):
        self.words_group = words_group
        self.pl = pl
        self.foreign = foreign
        self.label_1 = label_1
        self.label_2 = label_2
        self.date = date
        self.owner = owner


class Verbs(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    verbs_group = db.Column('verbs_group', db.String)
    pl = db.Column('pl', db.String)
    form1 = db.Column('form1', db.String)
    form2 = db.Column('form2', db.String)
    form3 = db.Column('form3', db.String)

    def __init__(self, verbs_group, pl, form1, form2, form3):
        self.verbs_group = verbs_group
        self.pl = pl
        self.form1 = form1
        self.form2 = form2
        self.form3 = form3


class Users(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String)
    password = db.Column('password', db.String)
    email = db.Column('email', db.String)
    user_type = db.Column('user_type', db.String)

    def __init__(self, username, password, email, user_type):
        self.username = username
        self.password = password
        self.email = email
        self.user_type = user_type


class ResultsVerbs(db.Model):
    id = db.Column('ID', db.Integer(), primary_key=True)
    username = db.Column('username', db.String(20))
    verbs_group = db.Column('verbs_group', db.String(20))
    result = db.Column('result', db.String(10))
    date = db.Column('date', db.String(20))

    def __init__(self, username, verbs_group, result, date):
        self.username = username
        self.verbs_group = verbs_group
        self.result = result
        self.date = date