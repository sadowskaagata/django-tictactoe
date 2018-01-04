from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Move


class MoveForm(ModelForm):
    """
    Creating a HTML form class with inner Meta class based on model Move class.
    """
    class Meta:
        model = Move
        exclude = []  # MoveForm always need exclude or include list

    def clean(self):
        """
        Checks for valid game board coordinates.
        Doesnt allow to pick previously used coordinates or outside of the board.
        """
        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        game = self.instance.game
        try:
            if game.board()[y][x] is not None:
                raise ValidationError("Square is not empty")
        except IndexError:
            raise ValidationError("Invalid coordinates")
        return self.cleaned_data
