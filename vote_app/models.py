from django.utils import timezone 
from django.db import models
from django.contrib.auth import  get_user_model
# Create your models here.
from django.urls import reverse

User = get_user_model()

class Election(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    rules = models.TextField()
    active = models.BooleanField(default=True)
    voters = models.ManyToManyField(User, related_name="eligible_elections")
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-active", '-start_date')

    def __str__(self) -> str:
        return self.name

    def get_total_votes(self) -> int:
        return self.votes.filter(is_completed=True).count()
    
    def get_total_positions (self) -> int:
        return self.positions.count()
    def end(self):
        self.end_date = timezone.now()
        self.active = True
        self.votes.filter(is_completed=False).update(is_completed=True)
        self.save()
        return True
            
    def get_end_url(self) -> str:
        return reverse('vote_app:end-election', kwargs={'election_id': self.pk})

    def get_results_url(self) -> str:
        return reverse('vote_app:election-results', kwargs={'election_id': self.pk})

    def get_vote_url(self) -> str:
        return reverse('vote_app:vote', kwargs={'election_id': self.pk})
    
    def get_review_votes_url(self) -> str:
        return reverse('vote_app:review-votes', kwargs={'election_id': self.pk})
    
    def is_started(self) -> bool:
        return self.start_date > timezone.now()
    
    def is_ended(self) -> bool:
        return self.end_date < timezone.now()
    
    def is_active(self) -> bool:
        return self.start_date <= timezone.now() <= self.end_date

    def yet_to_vote_users(self):
        return self.voters.exclude(
            id__in=[vote.user.pk for vote in self.votes.filter(is_completed=True)]
        )
class Position(models.Model):
    election = models.ForeignKey(Election, related_name="positions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_created',)
    
    def __str__(self) -> str:
        return self.name

    @property
    def is_yes_or_no(self):
        return self.aspirants.count() == 1

    def get_results_url(self) -> str:
        return reverse("vote_app:position-results", kwargs={'position_id': self.pk, 'election_id': self.election.pk})
    
    def get_vote_url(self) -> str:
        return reverse('vote_app:vote_position', kwargs={'position_id': self.pk})
    def get_votes_count(self) -> int:
        return self.aspirant_votes.filter(user_vote__is_completed=True).count()
    
    def winner(self):
        current_aspirant = None
        for aspirant in self.aspirants.all():
            
            if (current_aspirant == None) or (aspirant.total_votes > current_aspirant.total_votes):
                current_aspirant = aspirant
        return current_aspirant
class Aspirant(models.Model):
    name = models.CharField(max_length=255)
    position: Position = models.ForeignKey(Position, related_name="aspirants", on_delete=models.CASCADE)
    description = models.TextField()
    picture = models.ImageField(upload_to="aspirants/")

    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_created',)
    
    def __str__(self) -> str:
        return self.name

    def get_votes_count(self) -> int:
        return self.votes.filter(user_vote__is_completed=True).count()
    
    @property
    def total_votes(self) -> int:
        return self.get_votes_count()
    
    def get_vote_url(self) -> str:
        return reverse('vote_app:vote_position', kwargs={'position_id': self.position.pk, 'aspirant_id': self.pk})

    
    def get_percentage_votes(self):
        return self.total_votes / self.position.get_votes_count() * 100
    
    def get_percentage_votes_against(self):
        return 100 - self.get_percentage_votes()


class UserVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name="votes")
    is_completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"Vote by {self.user.username}"
    
    def get_save_url(self) -> str:
        return reverse('vote_app:save-vote', kwargs={'election_id': self.election.pk})
    
    def check_completed(self) -> bool:
        if self.is_completed:
            return True
        for position in self.election.positions.all():
            if not self.aspirant_votes.filter(position=position).exists():
                return False
        return True
    
    def get_uncompleted_votes(self):
        positions = []
        for position in self.election.positions.all():
            if not self.aspirant_votes.filter(position=position).exists():
                positions.append(position)
        return positions
    
class AspirantVote(models.Model):
    user_vote = models.ForeignKey(UserVote, related_name="aspirant_votes", on_delete=models.CASCADE)
    position = models.ForeignKey(Position, related_name="aspirant_votes", on_delete=models.CASCADE)
    aspirant = models.ForeignKey(Aspirant, related_name="votes", on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("position", "date_created",)
        unique_together = ('user_vote', 'position',)
    
    def __str__(self):
        if self.aspirant:
            return f"One vote for {self.aspirant.name} for position {self.position}"
        return f"Not Voted for position {self.position}"
    

    

