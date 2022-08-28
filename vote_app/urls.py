from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = "vote_app"

urlpatterns = [
    path('', views.elections, name="elections"),
    path('end-election/<int:election_id>/', views.end_election, name="end-election"),
    path('results/not-voted/<int:election_id>/', views.yet_to_vote, name="election-yet-to-vote"),
    path('results/<int:election_id>/percentage/', views.percentage_results, name="election-percentage-results"),
    path('results/<int:election_id>/', views.election_results, name="election-results"),
    path('results/<int:election_id>/position/<int:position_id>/', views.position_results, name="position-results"),
    path('review-votes/<int:election_id>/', views.review_votes, name="review-votes"),
    path('vote/<int:election_id>/', views.vote, name="vote"),
    path('vote/cast/<int:position_id>/', views.vote_position, name="vote_position"),
    path('vote/cast/<int:position_id>/<int:aspirant_id>/', views.vote_position, name="vote_position"),
    path('vote/save/<int:election_id>/', views.save_votes, name="save-vote")
]
