from django.shortcuts import render
from core.models import UserProfile
from .models import ChatModel

def chatPage(request, username):
    user_obj = UserProfile.objects.get(username=username)
    users = UserProfile.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'
    message_objs = ChatModel.objects.filter(thread_name=thread_name)
    return render(request, 'Messaging/chatRoom.html', context={'user': user_obj, 'users': users, 'messages': message_objs})
# Create your views here.
