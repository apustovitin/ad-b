from django.db import models
from tinymce import HTMLField
from accounts.models import Author
#from filebrowser.fields import FileBrowseField


class Category(models.Model):
    """Модель Category
    Кроме того пользователь должен определить объявление в одну из следующих 
    категорий: Танки, Хиллы, ДД, Торговцы, Гилдмастеры, Квестгиверы, Кузнецы,
    Кожевники, Зельевары, Мастера заклинаний
    """
    tanks = 'TNK'
    healers = 'HLR'
    damage_dealers = 'DDL'
    merchants = 'MRC'
    guild_masters = 'GMS'
    quest_givers = 'QGV'
    blacksmiths = 'BSM'
    tanners = 'TNR'
    potion_makers = 'PMK'
    spell_masters = 'SMS'
    CATEGORIES = [
        (tanks, 'Танки'),
        (healers, 'Хиллы'),
        (damage_dealers, 'ДД'),
        (merchants, 'Торговцы'),
        (guild_masters, 'Гилдмастеры'),
        (quest_givers, 'Квестгиверы'),
        (blacksmiths, 'Кузнецы'),
        (tanners, 'Кожевники'),
        (potion_makers, 'Зельевары'),
        (spell_masters, 'Мастера заклинаний'),
    ]
    category = models.CharField(max_length=3, choices=CATEGORIES, unique=True)

    def get_category_label_list(self):
        for category_label_list in self.CATEGORIES:
            if category_label_list[0] == self.category:
                return category_label_list

    def __str__(self):
        return self.get_category_label_list()[1]


class Ad(models.Model):
    """Модель Ads
    Объявления. Состоят из заголовка и текста, внутри которого могут быть картинки,
    встроенные видео и другой контентю. Обявления могут оставлять только 
    зарегистрированные пользователи. Один пользователь может быть автором нескольких
    объявлений. Кроме того пользователь должен определить объявление 
    в одну из следующих категорий.
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = HTMLField('Content')
    # image = FileBrowseField("Image", max_length=200, directory="images/", extensions=[".jpg"], blank=True)
    # document = FileBrowseField("PDF", max_length=200, directory="documents/", extensions=[".pdf", ".doc"], blank=True)

    def get_absolute_url(self):
        return f'/ads/{self.id}'
