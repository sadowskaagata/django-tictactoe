from django.forms import ModelForm
from .models import Invitation


class InvitationForm(ModelForm):
    """
    Creating a HTML input form based on a Invitations model.
    """
    class Meta:
        model = Invitation
        exclude = ('from_user', 'timestamp')  # No need for filling fields for from_user and timestamp.
