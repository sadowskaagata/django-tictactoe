from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class Invitation(models.Model):
    """
    Model Invitation class represents invitations to games from one user to another.

    """
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitations_sent")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="invitations_received",
                                verbose_name="User to invite",
                                help_text="Please select the user you want to play a game with.")
    message = models.CharField(max_length=300,
                               blank=True,
                               verbose_name="Optional Message",
                               help_text="It's always nice to add a friendly message!")
    timestamp = models.DateTimeField(auto_now_add=True)

