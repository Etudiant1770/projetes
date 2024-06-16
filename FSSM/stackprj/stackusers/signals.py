from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile#,Answer 
from stackbase.models import Question
#from .logic import award_badge_for_good_question, award_badge_for_good_answer

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()




 # @receiver(post_save, sender='stackbase.Question')
 # def check_good_question(sender, instance, created, **kwargs):
 #     if created and instance.is_good_question():
  #        award_badge_for_good_question(instance.user)

 # @receiver(post_save, sender='stackusers.Answer')
 # def check_good_answer(sender, instance, created, **kwargs):
 #     if created and instance.is_good_answer():
#        award_badge_for_good_answer(instance.user)