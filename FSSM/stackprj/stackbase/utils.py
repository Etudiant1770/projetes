# utils.py

from .models import UserBadge, Badge, Question#, Answer, Tag
from django.contrib.auth.models import User

from .models import Answer, Question


def award_question_badge(user, question):
    # Exemple de badge pour poser une première question
    first_question_badge, created = Badge.objects.get_or_create(
        name="Premier Question",
        defaults={"description": "Première question posée", "type": "question"}
    )
    if not UserBadge.objects.filter(user=user, badge=first_question_badge).exists():
        UserBadge.objects.create(user=user, badge=first_question_badge)

def award_answer_badge(user, answer):
    # Exemple de badge pour répondre à une première question
    first_answer_badge, created = Badge.objects.get_or_create(
        name="Premier Réponse",
        defaults={"description": "Première réponse donnée", "type": "answer"}
    )
    if not UserBadge.objects.filter(user=user, badge=first_answer_badge).exists():
        UserBadge.objects.create(user=user, badge=first_answer_badge)

def award_participation_badge(user):
    # Exemple de badge pour la participation (par exemple, 10 questions/réponses)
    participation_badge, created = Badge.objects.get_or_create(
        name="Participant Actif",
        defaults={"description": "Pour avoir participé activement (10 questions/réponses)", "type": "participation"}
    )
    if (Question.objects.filter(user=user).count() + Answer.objects.filter(user=user).count()) >= 10:
        if not UserBadge.objects.filter(user=user, badge=participation_badge).exists():
            UserBadge.objects.create(user=user, badge=participation_badge)

def award_tag_badge(user, tag):
    # Exemple de badge pour utiliser un tag spécifique
    tag_badge, created = Badge.objects.get_or_create(
        name=f"Expert en {tag.name}",
        defaults={"description": f"Pour avoir utilisé le tag {tag.name}", "type": "tag"}
    )
    if not UserBadge.objects.filter(user=user, badge=tag_badge).exists():
        UserBadge.objects.create(user=user, badge=tag_badge)
