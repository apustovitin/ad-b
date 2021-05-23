from django.db import models
from accounts.models import Author
from ads.models import Ad


class Response(models.Model):
    """Модель Responses
    Пользователи могут отправлять отклики на объявления других пользователей,
    состоящие из простого текста. Также пользователю должна быть доступна приватная
    страница с откликами на его объявления, внутри которой он может фильтровать 
    отклики по объявлениям, удалять их и принимать.
    """
    accepted = 'ACP'
    new = 'NEW'
    STATUSES = [(accepted, 'принят'), (new, 'новый')]
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    status = models.CharField(max_length=3, choices=STATUSES, default=new)
    creation_datetime = models.DateTimeField(auto_now_add=True)

    def get_status(self):
        for status_label_list in self.STATUSES:
            if status_label_list[0] == self.status:
                return status_label_list[1]

    def get_absolute_url(self):
        return f'/ads/{self.ad.id}'