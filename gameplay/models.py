from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


"""
All Django models has to inherit from class models.Model,
this makes it official django model which will represent a table in the database that holds moves
"""


# Defining possible status for the games.
GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)

BOARD_SIZE = 3


class GamesQuerySet(models.QuerySet):
    """
    Custom QuerySet class which represent all game objects from database.
    Method games_for_user returns only games for specific user.
    Using Q function to filter for games in which specific use is first or second player.
    Method active returns only games that haven't finished yet.
    """
    def games_for_user(self, user):

        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):

        return self.filter(
            Q(status="F") | Q(status="S")
        )


@ python_2_unicode_compatible
class Game(models.Model):
    """
    Creating players for the game using User class model
    Status attribute allows to store games statuses with default value for first player's move.
    Objects attribute has assigned new custom manager with methods from custom QuerySet class to override
    the manager object from Model class"
    """
    first_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_first_player")
    second_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_second_player")
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default="F", choices=GAME_STATUS_CHOICES)
    objects = GamesQuerySet.as_manager()

    def board(self):
        """
        Setting board parameters. Method board return a list of Move objects and [y][x] positions.
        """
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        # retrieves all moves from database
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        """
        Method receive user object to check if its current user's move.
        """
        return (user == self.first_player and self.status == 'F') or (user == self.second_player and self.status == 'S')

    def new_move(self):
        """
        Returns a new move object and checks if the game is not finished yet.
        """
        if self.status not in 'FS':
            raise ValueError("Cannot make a move on finished game")

        return Move(
            game=self,
            by_first_player=self.status == 'F'
        )

    def update_after_move(self, move):
        """
        Update of the games status given last move.
        """
        self.status = self._get_game_status_after_move(move)

    def quit_game(self):
        if self.status not in 'FS':
            raise ValueError("Cannot quit on finished game")
        else:
            return self.status == 'L'

    def _get_game_status_after_move(self, move):
        x, y = move.x, move.y
        board = self.board()
        if (board[y][0] == board[y][1] == board[y][2]) or\
           (board[0][x] == board[1][x] == board[2][x]) or\
           (board[0][0] == board[1][1] == board[2][2]) or\
           (board[0][2] == board[1][1] == board[2][0]):
            return "W" if move.by_first_player else "L"
        if self.move_set.count() >= BOARD_SIZE**2:
            return 'D'
        return 'S' if self.status == 'F' else 'F'

    def get_absolute_url(self):
        """
        Method get_absolute_url constructs URLs for game objects for the mapping.
        """
        return reverse('gameplay_detail', args=[self.id])

    def __str__(self):
        """
        Str method displays games in user-friendly way with game's details.
        """
        return"{0} vs. {1}".format(self.first_player, self.second_player)


class Move(models.Model):
    """
    Creating model class with x and y properties with methods to save move instances in database as integers.
    Field comment allows users to place comments before making move, stored as characters.
    Adding relations from moves to games.
    Using built-in class validators that check on coordinates with x and y values.
    """
    x = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE-1)]
    )
    y = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(BOARD_SIZE-1)]
    )
    comment = models.CharField(max_length=300, blank=True)  # blank=Trues allows user to leave comment field empty
    game = models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)  # adding relation from moves to games
    by_first_player = models.BooleanField(editable=False)

    def __eq__(self, other):
        """
        Equal method compares two moves
        """
        if other is None:
            return False
        return other.by_first_player == self.by_first_player

    def save(self, *args, **kwargs):
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()
