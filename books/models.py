from django.db import models
from django.contrib.auth import get_user_model
# from django.utils import timezone


class Book(models.Model):
    isbn = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    creator = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)

    def __str__(self):
        return str(self.isbn) + self.title


class History(models.Model):
    table_id = models.AutoField(primary_key= True)
    table_name = models.CharField(max_length = 255)
    target_book = models.CharField(max_length=255)
    create_user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE, related_name='user')
    is_lending = models.BooleanField(default=True, help_text='貸し出し中ならTrue')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return str(self.target_book) + str(self.create_user) + str(self.updated_at)
