from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bulletins.models import Bulletin
from bulletins.forms import BulletinForm

def recent_bulletins(recent = 100):
    latest_bulletins = Bulletin.objects.all().order_by('-Date')[:recent]
    return latest_bulletins

def index(request):
    bulletins = recent_bulletins(recent = 50)
    return render(request, 'index.html', {
        'bulletins': bulletins,
        'user': request.user
    })

def search(request):
    #unimplemented
    return HttpResponseRedirect('/')

def register(request):
    if request.method == 'POST':
        print "there was a POST request. . ."
        print request.POST ['username']
        print request.POST ['password']
        name = request.POST ['username']
        pw = request.POST ['password']
        user = User.objects.create_user(username=name, password=pw) # no email.
        user.save()
        return HttpResponseRedirect('/') #TODO maybe display a temp "success" page and redirect 5 sec
    else:
     user = request.user
    t = loader.get_template('register.html')
    rc = RequestContext(request, {  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(rc)) #do I also need to pass the csrf to the html for token?  Is a token being passed automatically?

@login_required()
def submit(request):
    if request.method == 'POST':
        form = BulletinForm(request.POST)
        if form.is_valid():
            bulletin = form.save(commit=False)
            bulletin.Author = request.user
            bulletin.save()
            return HttpResponseRedirect('/')
    else:
        form = BulletinForm()
    return render(request, 'submit.html', {'form': form})