from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Question(models.Model):
    SUBJECT_CHOICES = [
        ('M', 'Mathematics'),
        ('P', 'Physics'),
        ('C', 'Chemistry'),
    ]
    # CHAPTER_CHOICES = [
    #     ('APE', 'Alcohol, Phenol And Ethers'),
    # ]
    # EXCERCISE_TYPE = [
    #     ('CPPSL1', 'CPP Subjective Level 1'),
    #     ('CPPSL2', 'CPP Subjective Level 2'),
    #     ('CPPOL2', 'CPP Objective Level 2'),
    #     ('CPPOL1', 'CPP Objective Level 2'),#TODO: Add more excercise types
    # ]
    asker= models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    title = models.CharField(max_length=100)
    text = models.TextField()
    subject=models.CharField(max_length=1, choices=SUBJECT_CHOICES, default='C')
    hardness_points= models.IntegerField(default = 0)
    date_asked=models.DateTimeField('Date Asked', auto_now_add=True)
    no_of_answers = models.IntegerField(default=0)
    upvotes_total = models.ManyToManyField(User, related_name="upvotes" ,)
    downvotes_total = models.ManyToManyField(User, related_name="downvotes" ,)
    def hasUserAnswered(self, u):
        for answer in self.answer_set.all():
            if u == answer.author:
                return True
        return False

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('doubts:details', kwargs={'pk':self.pk})


class Answer(models.Model):
    author= models.ForeignKey(get_user_model(), on_delete=models.SET(get_sentinel_user))
    question= models.ForeignKey(Question, on_delete=models.CASCADE)
    text=models.TextField()
    date_answered=models.DateTimeField('Date Answered', auto_now_add=True)
    upvotes = models.IntegerField(default = 0)
    updated_time = models.DateTimeField(auto_now=True)
    upvoters = models.ManyToManyField(User, related_name="upvoters" ,)
    downvoters = models.ManyToManyField(User, related_name="downvoters" ,)
    def get_absolute_url(self):
        return reverse('doubts:details', kwargs={'pk':self.question.id})


