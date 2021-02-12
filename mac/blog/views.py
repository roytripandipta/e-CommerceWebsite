from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost


# Create your views here.

def index(request):
    mypost = Blogpost.objects.all()
    return render(request, 'blog/index.html', {'mypost': mypost})


def blogpost(request, id):
    blog = Blogpost.objects.filter(post_id = id)[0]
    print(blog)
    return render(request, 'blog/blogpost.html', {"blog":blog})
