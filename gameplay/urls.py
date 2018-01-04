from django.conf.urls import url
from .views import game_detail, make_move, AllGamesList, end_game


urlpatterns = [
    url(r'detail/(?P<id>\d+)/$', game_detail, name="gameplay_detail"),
    url(r'make_move/(?P<id>\d+)/$', make_move, name="gameplay_make_move"),
    url('all$', AllGamesList.as_view()),
    url(r'end/(?P<id>\d+)/$', end_game, name="gameplay_end_game")
]
