from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Question, Answer
from django.contrib.auth.models import User

@receiver(post_save, sender=Question)
def created_question(sender, instance, created, **kwargs):
    if created:
        instance.asker.profile.questions_asked+=1
        instance.asker.profile.save()


@receiver(post_save, sender=Answer)
def created_answer(sender, instance, created, **kwargs):
    if created:
        instance.author.profile.questions_answered+=1
        instance.author.profile.save()


