from django.urls import path
from . import views
from .views import BadgeListView, BadgeDetailView
from .views import faculty_home
from stackbase.views import TaggedQuestionListView


app_name = 'stackbase'

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),

    # CRUD Function
    path('questions/', views.QuestionListView.as_view(), name="question-lists"),
    path('questions/new/', views.QuestionCreateView.as_view(), name="question-create"),
    path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name="question-detail"),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name="question-update"),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name="question-delete"),
    path('questions/<int:pk>/comment/', views.AddCommentView.as_view(), name="question-comment"),
    path('like/<int:pk>', views.like_view, name="like_post"),
    path('badges/', BadgeListView.as_view(), name='badge_list'),
    path('badges/<int:pk>/', BadgeDetailView.as_view(), name='badge_detail'),
    path('tags/', views.tags, name='tags'),
    path('tag/<str:tag>/', views.TaggedQuestionListView.as_view(), name='tagged-questions'),
    path('tag/', views.tags, name='tags'),
    path('faculty_home/', faculty_home, name='faculty_home'),
    

]