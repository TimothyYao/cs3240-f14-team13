from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bulletins.forms import BulletinForm
from bulletins.models import Bulletin


def recent_bulletins(recent=100):
    latest_bulletins = Bulletin.objects.all().order_by('-Date')[:recent]
    return latest_bulletins

def index(request):
    bulletins = recent_bulletins(recent=50)
    return render(request, 'index.html', {
        'bulletins': bulletins,
        'user': request.user
    })

def search(request):
    if len(request.GET) > 0:
        term = request.GET['search']
        category = request.GET['type']
        print "there was a GET request. . ."
        bulletins = Bulletin.objects.search(term, category)[:50]
        return render(request, 'search_results.html', {
            'bulletins': bulletins,
            'user': request.user
        })
    return render(request, 'search.html')

def details(request, bulletin_id):
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    return render(request, 'details.html', {'bulletin': bulletin})

def register(request):
    message = 'Create User'
    if request.method == 'POST':
        name = request.POST ['username']
        pw = request.POST ['password']
        pw2 = request.POST ['password2']
        #all_users = list(Users.objects);
        #print all_users;
        if pw == pw2:
            if len(pw) < 7:
                message = 'password must have at least 7 characters'
                return render(request, 'register.html', {"message": message})
            if not any(x.isupper() for x in pw):
                message = 'password must contain at least 1 capital'
                return render(request, 'register.html', {"message": message})
            if not any(x.isdigit() for x in pw):
                message = 'password must contain at least 1 digit'
                return render(request, 'register.html', {"message": message})
            user = User.objects.create_user(username=name, password=pw) # no email.
            user.save()
            return HttpResponseRedirect('/') #TODO maybe display a temp "success" page and redirect 5 sec
        else:
            message = 'passwords do not match'
    return render(request, 'register.html', {"message": message})

@login_required()
def submit(request):
    if request.method == 'POST':
        form = BulletinForm(request.POST, request.FILES)
        if form.is_valid():
            bulletin = form.save(commit=False)
            bulletin.Author = request.user
            bulletin.save()
            return HttpResponseRedirect('/')
    else:
        form = BulletinForm()
    return render(request, 'submit.html', {'form': form})