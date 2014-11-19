from django.shortcuts import render
from django.template import loader, Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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