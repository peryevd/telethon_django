from django.db import models

class ChannelInfo(models.Model):
    json = models.JSONField()

class UsersInfo(models.Model):
    json = models.JSONField()

class MessageChannel(models.Model):
    json = models.JSONField()

class MessageReply(models.Model):
    json = models.JSONField()