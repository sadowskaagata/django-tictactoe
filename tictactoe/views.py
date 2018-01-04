from django.shortcuts import render, redirect


def welcome(request):

    """
    Main welcome page.

    After successful user authentication redirects player to player's home page

    """

    if request.user.is_authenticated:
        return redirect('player_home')
    else:
        return render(request, 'tictactoe/welcome.html')

