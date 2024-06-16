from django.contrib import admin
from .models import Question,Comment,Badge, UserBadge

admin.site.register(Question)
admin.site.register(Comment)


admin.site.register(Badge)
admin.site.register(UserBadge)
