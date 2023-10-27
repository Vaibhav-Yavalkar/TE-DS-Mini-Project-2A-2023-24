from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from .models import UserProfile, Post, Post_tag, Recommendations, Interaction, Logs, Freelancer, Tag, TopCharts
from .forms import PostForm, TagSelectionForm
from django.utils.text import slugify

def landing(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'core/landing.html')


def index(request):
    if request.user.is_authenticated:
        users = UserProfile.objects.exclude(username=request.user.username)
        posts = Post.objects.all()
        user_profiles = UserProfile.objects.in_bulk([post.freelancer.user_id.id for post in posts])
        tags = Post_tag.objects.filter(post__in=posts, score=10)
        context = {
            'users': users,
            'posts' : posts,
            'user_profiles': user_profiles,
            'tags': tags,
        }
        return render(request, 'core/index.html', context)
    else:
        return redirect('landing')

def search(request, query):
    results = Post.objects.filter(Q(name__contains=query) | Q(description__contains=query))
    tags = Post_tag.objects.filter(post__in=results, score=10)
    context = {
        'query' : query,
        'posts' : results,
        'tags' : tags,
    }
    return render(request, 'core/search.html', context)

def recommendations_view(request):
    user = request.user
    if user.is_authenticated:
        recommendations = Recommendations.objects.filter(user=user, visited=False).order_by('-score')[:9]
        recommended_posts = [recommendation.post for recommendation in recommendations]

        return render(request, 'core/for_you.html', {'posts': recommended_posts})
    else:
        return redirect('index')

def top_posts_view(request):
    top_posts = Post.objects.filter(topcharts__type='Top')
    latest_posts = Post.objects.filter(topcharts__type='Latest')
    grossing_posts = Post.objects.filter(topcharts__type='Grossing')
    context = {
        'latest_posts': latest_posts,
        'top_posts': top_posts,
        'grossing_posts': grossing_posts,
    }

    return render(request, 'core/top_posts.html', context)


def create_post(request):
    error = None
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if not request.FILES.get('images'):
            error = "Image is a required field!"
        if form.is_valid():
            post = form.save(commit=False)
            freelancer = Freelancer.objects.get(user_id=request.user)
            post.freelancer = freelancer
            post.link = slugify(post.name.replace(" ", "-")) 
            post.save()
            populate_post_tags(post.link)
            
            return redirect('update_tag_scores', post.link)
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form, 'error':error})

def post_details(request, link):
    post = get_object_or_404(Post, link=link)    
    context={
        'post' : post
    }
    if request.user.is_authenticated:
        user = request.user
        interaction = Interaction(
            user=user,
            post=post,
            action="click",
        )
        interaction.save()
        log = Logs(
            user=user,
            post=post,
            action="click",
        )
        log.save()
    return render(request, 'core/details.html', context)

def update_tag_scores(request, link):
    post = get_object_or_404(Post, link=link)

    if request.method == 'POST':
        form = TagSelectionForm(request.POST)

        if form.is_valid():
            tag1 = form.cleaned_data['tag1']
            tag2 = form.cleaned_data['tag2']

            if tag1:
                Post_tag.objects.update_or_create(post=post, tag=tag1, defaults={'score': 10})
            if tag2:
                Post_tag.objects.update_or_create(post=post, tag=tag2, defaults={'score': 10})

            return redirect('details', post.link)

    else:
        form = TagSelectionForm()

    return render(request, 'core/update_tag_scores.html', {'form': form, 'post': post})

# Automated tasks

def populate_post_tags(link):
    # Get all posts and tags
    post = get_object_or_404(Post, link=link)
    tags = Tag.objects.all()

    # Loop through each tag, creating Post_tag instances with a score of 0
    for tag in tags:
        post_tag, created = Post_tag.objects.get_or_create(post=post, tag=tag)
