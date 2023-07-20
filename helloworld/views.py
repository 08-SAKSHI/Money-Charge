from django.shortcuts import render
from helloworld.models import User
# Create your views here.
def index(request): # < here
    users = User.objects.all()
    return render(request, 'helloworld/index.html',{'users':users})

def hello(request):
    return render(request,'helloworld/hello.html')