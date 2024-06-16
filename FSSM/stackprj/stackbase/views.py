# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import Question, Comment,Badge
from .forms import CommentForm
from .utils import award_question_badge, award_answer_badge, award_participation_badge, award_tag_badge
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from taggit.models import Tag


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def like_view(request, pk):
    post = get_object_or_404(Question, id=request.POST.get('question_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('stackbase:question-detail', args=[pk]))
class QuestionListView(ListView):
    model = Question
    context_object_name = 'questions'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ""
        tag_input = self.request.GET.get('tag') or ""

        if search_input:
            context['questions'] = context['questions'].filter(title__icontains = search_input)
            context['search_input'] = search_input
        return context

class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        something = get_object_or_404(Question, id=self.kwargs['pk'])
        total_likes = something.total_likes()
        liked = False
        if something.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['total_likes'] = total_likes
        context['liked'] = liked
        return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'content']
    context_object_name = 'question'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        award_question_badge(self.request.user, form.instance)
        award_participation_badge(self.request.user)
        # Assuming question has tags
        for tag in form.instance.tags.all():
            award_tag_badge(self.request.user, tag)
        return response

class QuestionUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Question
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user

class QuestionDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Question
    context_object_name = 'question'
    success_url = reverse_lazy('home')

    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user

class CommentDetailView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'question-detail.html'
    
    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        response = super().form_valid(form)
        award_answer_badge(self.request.user, form.instance)
        award_participation_badge(self.request.user)
        # Assuming comment is related to a question that has tags
        question = get_object_or_404(Question, pk=self.kwargs['pk'])
        for tag in question.tags.all():
            award_tag_badge(self.request.user, tag)
        return response

    success_url = reverse_lazy('question-detail')
    def get_success_url(self):
        return reverse_lazy('stackbase:question-detail', kwargs={'pk': self.kwargs['pk']})

    
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'question-answer.html'

    def form_valid(self, form):
        form.instance.question_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('question-lists')

        
    def get_success_url(self):
        return reverse_lazy('stackbase:question-detail', kwargs={'pk': self.kwargs['pk']})

class BadgeListView(ListView):
    model = Badge
    template_name = 'stackbase/badge_list.html'
    context_object_name = 'badges'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        badges = self.get_queryset()
        badge_data = []
        for badge in badges:

            badge_info = {
                'badge': badge,
                'users': badge.users.all(),
                'total_users': badge.users.count(),
                'total_questions': badge.questions.count(),
                'total_answers': badge.answers.count(),
                'total_likes': badge.likes_count,
                'gold_badges_count': badge.gold_badges_count,
                'silver_badges_count': badge.silver_badges_count,
                'bronze_badges_count': badge.bronze_badges_count
            }
            badge_data.append(badge_info)
        
        context['badge_data'] = badge_data

        return context

    

class BadgeDetailView(DetailView):
    model = Badge
    template_name = 'stackbase/badge_detail.html'
    context_object_name = 'badge'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        badge = self.object

        # Obtenir les utilisateurs avec leurs questions ou réponses associées
        users_with_content = []
        for user in badge.users.all():
            user_data = {
                'user': user,
                'profile': user.profile,  # Supposons que vous ayez un modèle de profil lié à l'utilisateur
                'questions': user.question_set.count(),
                'answers': user.answer_set.count(),
            }
            users_with_content.append(user_data)

        context['users_with_content'] = users_with_content
        context['total_users'] = badge.users.count()
        context['total_questions'] = badge.questions.count()
        context['total_answers'] = badge.answers.count()
        context['total_likes'] = badge.likes_count
        context['gold_badges_count'] = badge.gold_badges_count
        context['silver_badges_count'] = badge.silver_badges_count
        context['bronze_badges_count'] = badge.bronze_badges_count
        awarded_at = datetime.now()

        context['awarded_at'] = awarded_at
        return context



#tag
class TaggedQuestionListView(ListView):
    model = Question
    template_name = 'stackbase/tagged_questions.html'
    context_object_name = 'questions'

    def get_queryset(self):
        tag = get_object_or_404(Tag, name=self.kwargs.get('tag'))
        return Question.objects.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('tag')
        return context
def tags(request):
    tags = Tag.objects.all()  # Récupérer tous les objets Tag
    return render(request, 'tag_list.html', {'tags': tags})
 # Récupérer les questions
    tag_with_count = []
    for tag in tags:
        tag_data = {
            'name': tag,
            'count': Question.objects.filter(tags__icontains=tag).count()
        }
        tag_with_count.append(tag_data)
    return render(request, 'tags_list.html', {'tags': tag_with_count})

def tag_list_view(request):
    tags = Tag.objects.all()  # Récupérer tous les objets Tag
    return render(request, 'tag_list.html', {'tags': tags})
# acceuil

from django.shortcuts import render

def faculty_home(request):
    return render(request, 'faculty_home.html')

