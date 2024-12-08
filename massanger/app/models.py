from django.db import models

class User(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='users_avatar')
    update_datetime = models.DateTimeField(auto_now=True)


class Chat(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    avatar = models.ImageField(upload_to='chats_avatar')
    users = models.ManyToManyField(User, related_name='chat_user')
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, default=None)
    text = models.TextField()
    file = models.FileField(upload_to='chats_files', default=None)
    image = models.ImageField(upload_to='chats_image', default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now=True)

class Tarif(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()