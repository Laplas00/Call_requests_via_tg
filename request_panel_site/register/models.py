from django.db import models

class TelegramUser (models.Model):
    id = models.BigIntegerField(primary_key=True)  # Use BigIntegerField for Telegram user ID
    first_name = models.CharField(max_length=255)  # Store the user's first name
    username = models.CharField(max_length=255, unique=True, null=True)  # Store the username, allow null
    photo_url = models.URLField(max_length=2000, null=True)  # Store the photo URL, allow null

    def __str__(self):
        return f"{self.first_name} ({self.username})"