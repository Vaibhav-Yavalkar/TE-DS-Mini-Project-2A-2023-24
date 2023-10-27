from allauth.account.signals import user_signed_up
from .models import UserProfile, Tag, UserInterests, Freelancer
from django.dispatch import receiver

@receiver(user_signed_up)
def user_signed_up_handler(sender, request, user, **kwargs):
    user_profile = UserProfile.objects.get(username=user.username)
    create_freelancer_profile(user_profile)
    populate_user_interests(user_profile)

def create_freelancer_profile(user_profile):
    freelancer, created = Freelancer.objects.get_or_create(user_id=user_profile)

def populate_user_interests(user_profile):
    tags = Tag.objects.all()

    for tag in tags:
        user_interest, created = UserInterests.objects.get_or_create(user=user_profile, tag=tag)

