
def create_firm(name: str, head: User):
    # db = get_db()
    # db.connect()
    # with db.atomic():
    #     firm, _ = Firm.get_or_create(name=name, head_user_id=head.id)
    #     firm.save()
    # return firm
    pass

def create_user(name, role):
    user, _ = User.get_or_create(name=name, role=role)
    user.save()
    return user
    pass

def create_test_db():
    # db = get_db()
    #
    # db.connect()
    # with db.atomic():
    #
    #     db.commit()
    #     db.create_tables([City,Region, Firm, UserProfile, User, Question,  Petition], safe=True)
    #     db.commit()
    # # user = create_user("Димон", "firm")
    # # firm = create_firm("РПКБ", user)
    # # firm.save()
    # # user = create_user("Другой", "firm")
    # # firm = create_firm("РПЗ", user)
    # # firm.save()
    # from questions import questions_list
    # with db.atomic():
    #     for q in questions_list:
    #         qr, _ = Question.get_or_create(ask=q[0], answer=q[1])
    #         qr.save()
    # db.close()
    pass

def clear_database(db_name='bot.db'):
    # db =get_db()
    # db.connect()
    # with db:
    #     Question.delete().execute()
    #     db.commit()
    # db.close()
    pass