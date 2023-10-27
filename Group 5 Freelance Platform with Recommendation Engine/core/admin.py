from django.contrib import admin

from .models import UserProfile, Freelancer, Tag, Interaction, Post_tag, UserInterests, Post

admin.site.register(UserProfile)
admin.site.register(Freelancer)
admin.site.register(Tag)
admin.site.register(Post_tag)
admin.site.register(Interaction)
admin.site.register(UserInterests)
admin.site.register(Post)
