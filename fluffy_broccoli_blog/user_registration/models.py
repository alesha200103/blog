from django.db import models

class User(models.Model): # модель пользователя
    username = models.CharField(max_length=20, unique=True) # уникальное имя пользователя
    user_password = models.TextField() # хеш пароля

