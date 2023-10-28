from django.shortcuts import render
from django.http import HttpResponse

from django import forms
from . import recommender
from . import api

# Create your views here.
def index(request):
    return render(request, 'Movies/index.html')

def Login(request):
    return render(request, 'Movies/Login_Page.html')

#def Register(request):
   # return render(request, 'Movies/form.html',context={"form":form})

class Searchbar(forms.Form):
    movie_name = forms.CharField()

def search_movies(request):
    form = Searchbar()
    if request.method == 'POST':
        form = Searchbar(request.POST)
        if form.is_valid():
            movie_name = form.cleaned_data.get('movie_name')
            try:
                url_list=[]
                recommended_movies_id=recommender.hybrid_recommendation(movie_name)
                for id in recommended_movies_id:
                    url_list.append(api.get_movie_poster(id))
                return render(request, 'Movies/result.html', context={'show':url_list})
                
                #return render(request, 'Movies/result.html', context={'show':url_list})
            except:
                return render(request, 'Movies/result.html', context={'show':"Movie name not found"})
        else:
            return render(request, 'Movies/form.html', context={'form': form})
    else:
        return render(request, 'Movies/form.html', context={'form': form})
