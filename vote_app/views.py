from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
# Create your views here.
from django.http.request import HttpRequest
from django.http.response import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Aspirant, AspirantVote, Election, Position, UserVote


def dashboard(request: HttpRequest) -> HttpResponse:
    user = request.user
    election = user.eligible_elections.first()

    return render(request, 'accounts/dashboard.html', {'election': election})

@login_required
def elections(request: HttpRequest) -> HttpResponse:
    user = request.user
    election = user.eligible_elections.first()

    return render(request, 'accounts/dashboard.html', {'election': election})

@login_required
def vote(request: HttpRequest, election_id: int = None) -> HttpResponse:
    election: Election = get_object_or_404(Election, active=True, voters=request.user, pk=election_id)
    if election.start_date > timezone.now():
        messages.error(request, "Sorry the Election has not begun.")
        return redirect('/elections/')
    elif election.end_date < timezone.now():
        messages.error(request, "Sorry The election has ended. If your vote remains, it will be automatically saved when the election is ended by the Commisioner")
        return redirect('/elections/')
    if not election:
        raise Http404("Not Allowed")
    if not request.user in election.voters.all():
        raise Http404("Not Allowed")
    uservote, created = UserVote.objects.get_or_create(user=request.user, election=election)
    
    return render(request, "vote_app/vote.html", {'election': election})

@login_required
def vote_position(request: HttpRequest, position_id: int, aspirant_id: int=None) -> HttpResponse:
    position: Position = get_object_or_404(Position, pk=position_id, election__voters=request.user)
    aspirant = None
    success = False
    election: Election = position.election
    if election.start_date > timezone.now():
        messages.error(request, "Sorry the Election has not begun.")
        return redirect('/elections/')
    elif election.end_date < timezone.now():
        messages.error(request, "Sorry The election has ended. If your vote remains, it will be automatically saved when the election is ended by the Commisioner")
        return redirect('/elections/')
    uservote:UserVote
    uservote, _ = UserVote.objects.get_or_create(user=request.user, election=position.election)
    if uservote.is_completed:
        messages.error(request, "You cannot vote again.")
        return redirect('/elections/')
    vote, _ = AspirantVote.objects.get_or_create(user_vote = uservote, position=position)
    
    if aspirant_id:
        aspirant: Aspirant = get_object_or_404(Aspirant, pk=aspirant_id)
        
    
        if position.is_yes_or_no:
            selection = request.GET.get('vote')
            
            if selection is not None:
                if selection == "yes":
                    vote.aspirant = aspirant
                    vote.save()
                    success = True
                elif selection == 'no':
                    vote.aspirant = None
                    vote.save()
                    success = True
                else:
                    success = False
                    messages.error(request, "Your vote was not saved")
        else:
            vote.aspirant = aspirant
            vote.save()
            messages.success(request,"Your vote has been save.")
            success = True
    if success:
        messages.success(request, "Everything was successful")
        try:
            new_position = position
            no_match = 0 
            while (new_position.id == position.id) or (new_position.election != position.election):
                new_position: Position = position.get_next_by_date_created()
                if new_position.election == election:
                    no_match = 0
                if no_match > 3:
                    raise Exception()
                no_match += 1
            return redirect(new_position.get_vote_url())
        except:
            uncompleted_votes = uservote.get_uncompleted_votes()
            if uncompleted_votes:
                return redirect(uncompleted_votes[0].get_vote_url())
            return redirect(position.election.get_review_votes_url())
    return render(request, 'vote_app/vote_position.html', {'position': position, 'vote': vote})

@login_required
def review_votes(request: HttpRequest, election_id: int):
    election: Election = get_object_or_404(Election, active=True, pk=election_id, voters=request.user)
    if election.start_date > timezone.now():
        messages.error(request, "Sorry the Election has not begun.")
        return redirect('/elections/')
    elif election.end_date < timezone.now():
        messages.error(request, "Sorry The election has ended. If your vote remains, it will be automatically saved when the election is ended by the Commisioner")
        return redirect('/elections/')
    user_vote: UserVote = get_object_or_404(UserVote, user=request.user, election=election)
    
    
    return render(request, 'vote_app/review_votes.html', {'election': election, 'user_vote': user_vote, 'uncompleted_positions': user_vote.get_uncompleted_votes()})

@login_required
def save_votes(request: HttpRequest, election_id: int):
    election: Election = get_object_or_404(Election, active=True, pk=election_id, voters=request.user)
    if election.start_date > timezone.now():
        messages.error(request, "Sorry the Election has not begun.")
        return redirect('/elections/')
    elif election.end_date < timezone.now():
        messages.error(request, "Sorry The election has ended. If your vote remains, it will be automatically saved when the election is ended by the Commisioner")
        return redirect('/elections/')
    user_vote: UserVote = get_object_or_404(UserVote, user=request.user, election=election)
    
    if user_vote.check_completed():
        user_vote.is_completed = True
        user_vote.save()
        messages.success(request, "Your Vote has been recorded. Thank you.")
    else:
        messages.error(request, "You have not completed your election. Kindly finish it up.")
        return redirect(election.get_vote_url())

    return redirect('/elections/')


@login_required
def election_results(request: HttpRequest, election_id: int) -> HttpResponse:
    if not request.user.is_superuser:
        raise Http404("Only the electoral commissioner is allowed here.")

    election = get_object_or_404(Election, pk=election_id)

    return render(request, "vote_app/election_results.html", {'election': election})


@login_required
def position_results(request: HttpRequest, election_id: int, position_id: int) -> HttpResponse:
    election = get_object_or_404(Election, pk=election_id,)
    position = get_object_or_404(Position, pk=position_id,)
    total_votes = position.get_votes_count()
    if position.is_yes_or_no:
        aspirant = position.aspirants.first()
        labels = [f"{aspirant.name}(YES)", f"{aspirant.name}(NO)"]
        values = [aspirant.get_votes_count(), total_votes - aspirant.get_votes_count()]
    else:
        labels = [aspirant.name for aspirant in position.aspirants.all()]
        values = [aspirant.get_votes_count() for aspirant in position.aspirants.all()]
    
    data={'labels': labels, 'values': values, 'total_votes': total_votes}
    return JsonResponse(data, safe=True)

@login_required
def end_election(request: HttpRequest, election_id: int) -> HttpResponse:
    if not request.user.is_superuser:
        return Http404("You do not have permission to view this page.")
    election = get_object_or_404(Election, pk=election_id)
    election.end()
    messages.success(request, "Election ended Successfully.")
    messages.success(request, "All unsaved votes have been saved.")
    return redirect(election.get_results_url())

@login_required
def yet_to_vote(request: HttpRequest, election_id: int) -> HttpResponse:
    if not request.user.is_superuser:
        return Http404("Only the electoral commissioner is allowed")
    election = get_object_or_404(Election, pk=election_id)
    return render(request, "vote_app/yet_to_vote.html", {"election": election})

@login_required
def percentage_results(request: HttpRequest, election_id: int) -> HttpResponse:
    if not request.user.is_superuser:
        return Http404("Only the electoral commissioner is allowed")
    election = get_object_or_404(Election, pk=election_id)
    return render(request, "vote_app/percentage_results.html", {"election": election})