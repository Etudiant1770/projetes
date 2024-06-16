from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=10000)
    content = models.TextField(null=True, blank=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='question_post')
    date_created = models.DateTimeField(default=timezone.now)
    level_image = models.ImageField(upload_to='level_images/')
                                 
    def __str__(self):
        return f'{self.user.username} - Question'
    
    def get_absolute_url(self):
        return reverse('stackbase:question-detail', kwargs={'pk':self.pk})
    
    def total_likes(self):
        return self.likes.count()
    
    def is_good_question(self):
        # Logique pour déterminer si c'est une bonne question
        return self.total_likes() >= 10  # Modifié pour utiliser total_likes()

class Comment(models.Model):
    question = models.ForeignKey(Question, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=10000)
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return '%s - %s' % (self.question.title, self.question.user)

    def get_success_url(self):
        return reverse('stackbase:question-detail', kwargs={'pk': self.question.pk})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Badge(models.Model):
    BADGE_TYPES = [
        ('question', 'Question Badge'),
        ('answer', 'Answer Badge'),
        ('participation', 'Participation Badge'),
        ('tag', 'Tag Badge'),
    ]
    GOLD = 'Gold'
    SILVER = 'Silver'
    BRONZE = 'Bronze'
    BADGE_TYPE_CHOICES = [
        (GOLD, 'Gold'),
        (SILVER, 'Silver'),
        (BRONZE, 'Bronze'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=BADGE_TYPES)
    badge_type = models.CharField(max_length=6, choices=BADGE_TYPE_CHOICES)  # Modifié la longueur maximale
    users = models.ManyToManyField(User, related_name='badges')
    questions = models.ManyToManyField('Question', related_name='badge_questions')
    answers = models.ManyToManyField('Answer', related_name='badge_answers')
    likes_count = models.IntegerField(default=0)
    gold_badges_count = models.IntegerField(default=0)
    silver_badges_count = models.IntegerField(default=0)
    bronze_badges_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.badge.name}'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    content = models.TextField()
    upvotes = models.ManyToManyField(User, related_name='answer_upvotes')
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Answer by {self.user.username}'

    def total_upvotes(self):
        return self.upvotes.count()

    def is_good_answer(self):
        return self.total_upvotes() >= 5  # Exemple: une réponse est bonne si elle a au moins 5 votes positifs
