from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    """Модель Author
    Модель, содержащая объекты всех авторов.
    Имеет следующие поля:
        cвязь «один к одному» с встроенной моделью пользователей User;
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
