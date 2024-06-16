from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from stackbase.models import Question
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=1000)
    phone = models.IntegerField(null = True , blank= True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pic")
    
    def __str__(self):
        return f'{self.user.username} - Profile'

    def save(self, *args , **kwargs):
        super().save(*args , **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300 , 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


#class Answer(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
   # question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
   # content = models.TextField()
   # upvotes = models.ManyToManyField(User, related_name='answer_upvotes')
    #date_created = models.DateTimeField(default=timezone.now)

    #def __str__(self):
     #   return f'Answer by {self.user.username}'

    #def total_upvotes(self):
      #  return self.upvotes.count()

    #def is_good_answer(self):
      #  return self.total_upvotes() >= 5  # Exemple: une réponse est bonne si elle a au moins 5 votes positifs


#class Badge(models.Model):
 #    name = models.CharField(max_length=100)
 #    description = models.TextField()
#     image = models.ImageField(upload_to='badges/')
    
#     def __str__(self):
#         return self.name

# class UserBadge(models.Model):
 #    user = models.ForeignKey(User, on_delete=models.CASCADE)
#     badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
 #    date_awarded = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#        return f"{self.user.username} - {self.badge.name}"

#
