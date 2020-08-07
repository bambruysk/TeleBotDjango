import datetime

from django.db import models


# Create your models here.

class BaseBotModel(models.Model):
    pass


class Region(BaseBotModel):
    name = models.CharField()
    head_user_id = models.IntegerField(null=False)

    def __str__(self):
        return str(self.name)


class City(BaseBotModel):
    name = models.CharField()
    head_user_id = models.IntegerField(null=False)

    def __str__(self):
        return str(self.name)


class Firm(BaseBotModel):
    name = models.CharField()
    head_user_id = models.IntegerField(null=False)
    city = models.ForeignKey(City, null=False, backref="firm", verbose_name="Город")

    #    region = ForeignKeyField(Region, null=False,  backref="firm",verbose_name="Область" )

    def __str__(self):
        return str(self.name)


class Center(BaseBotModel):
    head_user_id = models.IntegerField(null=False)


def nameSurnameValidate(value: str) -> bool:
    """
    Validate name must be cyrrllic
    TODO: must be releease
    :param value:
    :return:
    """
    return True


class UserProfile(BaseBotModel):
    work_place = models.ForeignKey(Firm, backref="user_profile", null=True, verbose_name="Место работы")
    first_name = models.CharField(default="", verbose_name="Имя")
    last_name = models.CharField(default="", verbose_name="Фамилия")
    father_name = models.CharField(default="", verbose_name="Отчество")
    department = models.CharField(default="", verbose_name="Отдел")
    position = models.CharField(default="", verbose_name="Должность")
    ticket_id = models.CharField(default="", verbose_name="Номер профсоюзного билета")

    # city = ForeignKeyField(City, backref="user_profile", null=True, verbose_name="Город")
    # region = ForeignKeyField(Region, backref="user_profile", null=True, verbose_name="Область")

    def get_profile(self):
        profile = [
            ("Имя", self.first_name),
            ("Фамилия", self.last_name),
            ("Отчество", self.father_name),
            ("Место работы", self.work_place),
        ]
        return profile

    @classmethod
    def get_field_names(cls):
        res = {"work_place": "Место работы",
               "first_name": "Имя",
               "last_name": "Фамилия",
               "father_name": "Отчество",
               "department": "Отдел",
               "position": "Должность",
               "ticket_id": "Номер профсоюзного билета",
               "city": "Город",
               "region": "Область", }
        # print(cls._meta.fields)
        # for k, v in cls._meta.fields:
        #     if v.verbose_name:
        #         res[k] = v.verbose_name
        return res

    def __str__(self):
        return f"ФИО {self.last_name} {self.first_name} {self.father_name}\n" \
               f"Мeсто работы: {self.work_place} \n" \
               f"Отдел {self.department} \n" \
               f"Должность {self.position} \n" \
               f"Номер профсоюзного билета {self.ticket_id} \n" \
               f"Город {self.city}\n" \
               f"Область  {self.region}\n"

    def set_field_by_name(self, fname, val: str):
        if fname == "work_place":
            # TODO:  Validate workplace
            firm = Firm.select().get(name=val)
            if firm:
                self.work_place = firm
            else:
                raise ValueError
            return
        if fname == "first_name":
            if nameSurnameValidate(val):
                val.lower()
                val.capitalize()
                self.first_name = val
        if fname == "last_name":
            if nameSurnameValidate(val):
                val.lower()
                val.capitalize()
                self.last_name = val
        if fname == "father_name":
            if nameSurnameValidate(val):
                val.lower()
                val.capitalize()
                self.father_name = val
        if fname == "department":
            self.department = str(val)
        if fname == "position":
            self.position = str(val)
        if fname == "region":
            # TODO:  Validate workplace
            region = Region.select().get(name=val)
            if region:
                self.work_place = region
            else:
                raise ValueError
            return


class User(BaseBotModel):
    # telegram username
    name = models.CharField(null=True)
    chat_id = models.IntegerField(null=True, index=True, unique=True)
    user_id = models.IntegerField(null=True)
    role = models.CharField(null=True)
    profile = models.ForeignKey(UserProfile, backref="user", null=True)


class Question(BaseBotModel):
    ask = models.TextField()
    answer = models.TextField()
    firm = models.ForeignKey(Firm, null=True, related_name="questions")
    parent_id = models.IntegerField(default=0)


class Petition(BaseBotModel):
    author = models.ForeignKeyField(User, backref="petitions", null=False)
    text = models.TextField()
    severity = models.IntegerField()
    status = models.IntegerField()
    answer = models.TextField()
    created_time = models.DateTimeField(default=datetime.datetime.now)

    def send_list(self):
        s_list = []
        firm_head = User.get(id=self.author.profile.work_place.head_user_id)
        s_list.append(firm_head)
        if self.severity > SEVERITY_FIRM:
            region_head = User.get(id=self.author.profile.region.head_user_id)
            s_list.append(region_head)
        if self.severity > SEVERITY_REGION:
            center_head = User.get(id=Center.get(id=1).head_user_id)
            s_list.append(center_head)
        return s_list
