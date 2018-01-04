from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from .models import Game
from .forms import MoveForm


@login_required
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)  # Returns Game object or raises Http404 exception.
    context = {'game': game}  # dictionary that contains the game
    if game.is_users_move(request.user):
        context['form'] = MoveForm()
    return render(request, 'gameplay/game_detail.html', context)


@login_required
def make_move(request, id):
    game = get_object_or_404(Game, pk=id)
    if not game.is_users_move(request.user):
        raise PermissionError
    move = game.new_move()
    form = MoveForm(instance=move, data=request.POST)
    if form.is_valid():
        move.save()
        return redirect("gameplay_detail", id)
    else:
        return render(request,
                      "gameplay/game_detail.html",
                      {'game': game, 'form': form})


@login_required
def end_game(request, id):
    game = get_object_or_404(Game, pk=id)
    context = {'game': game}
    if game.is_users_move(request.user):
        game.quit_game()
        return render(request, "gameplay/end_game.html", context, id)


class AllGamesList(ListView):
    """
    With ListView module creating display list of games for particular user.
    """
    model = Game

