from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from gameplay.models import Game
from .forms import InvitationForm
from .models import Invitation
# Create your views here.

@login_required
def home(request):
    """
    Template view: Home method retrieves user's games, active and finished ones and received invitation for logged user.
    """
    my_games = Game.objects.games_for_user(request.user)  # Game.objects.filter selects from the Game table
    active_games = my_games.active()
    finished_games = my_games.difference(active_games)
    invitations = request.user.invitations_received.all()
    return render(request, 'player/home.html',
                  {'games': active_games,
                   'finished_games': finished_games,
                   'invitations': invitations})  # passing list of invitations to the template

@login_required
def new_invitation(request):
    """
    Method new_invitation creates new InvitationForm object.
    Invitation object takes an instance of Invitation where from_user is logged user.
    Form object is an instance of InvitationForm where the fields hold user's input.
    Checking form - is valid if all fields were filled correctly.
    """
    if request.method == "POST":
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form': form})

@login_required
def accept_invitation(request, id):
    """
    Checking if currently logged user is a user who was invited.
    Create method for a model Game class creates a model instance
    of new game in database.
    If invitation was not accepted it will be removed.
    """
    global game
    invitation = get_object_or_404(Invitation, pk=id)  # either retrieves an object or displays 404 error
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user
            )
        invitation.delete()
        return redirect(game)
    else:
        return render(request,
                      "player/accept_invitation_form.html",
                      {'invitation': invitation})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')  # reverse_lazy
