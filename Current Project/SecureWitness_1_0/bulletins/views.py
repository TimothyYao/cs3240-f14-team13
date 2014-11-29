from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bulletins.models import Bulletin, BulletinSearch, File
from bulletins.forms import BulletinForm

def recent_bulletins(recent=100):
    latest_bulletins = Bulletin.objects.all().order_by('-Date')[:recent]
    return latest_bulletins

def handle_upload(request, bulletin):
    if 'files' in request.FILES:
            for i in request.FILES.getlist('files'):
                upload = File()
                upload.bulletin = bulletin
                upload.File_Field = i
                upload.save()

def index(request):
    bulletins = recent_bulletins(recent=50)
    return render(request, 'index.html', {
        'bulletins': bulletins,
        'user': request.user
    })

@login_required()
def search(request):
    if len(request.GET) > 0:
        term = request.GET['search']
        category = request.GET['type']
        bulletins = Bulletin.objects.search(term, category)[:50]
        no_results = len(bulletins) == 0
        return render(request, 'search_results.html', {
            'bulletins': bulletins,
            'user': request.user,
            'no_results': no_results
        })
    return render(request, 'search.html')

@login_required()
def search_redirect(request, bulletin_id):
    return HttpResponseRedirect('/'+bulletin_id+'/')

@login_required()
def details(request, bulletin_id):
    if request.method == 'POST':
        if 'edit' in request.POST:
            return HttpResponseRedirect('/'+bulletin_id+'/edit/')
        elif 'delete' in request.POST:
            Bulletin.objects.get(pk=bulletin_id).delete()
            return HttpResponseRedirect('/')
        elif 'move' in request.POST:
            print 'move'
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    docs = File.objects.filter(bulletin=bulletin)
    has_docs = len(docs) > 0
    owner = request.user == bulletin.Author
    return render(request, 'details.html', {
        'bulletin': bulletin,
        'owner': owner,
        'docs': docs,
        'has_docs': has_docs
    })

def register(request):
    message = 'Create User'
    if request.method == 'POST':
        name = request.POST['username']
        pw = request.POST['password']
        pw2 = request.POST['password2']
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
        bulletin = Bulletin()
        bulletin.Title = request.POST["title"]
        bulletin.Pseudonym = request.POST["pseudonym"]
        bulletin.Location = request.POST["location"]
        bulletin.Description = request.POST["description"]
        bulletin.Author = request.user
        bulletin.save()
        handle_upload(request, bulletin)
        return HttpResponseRedirect('/'+str(bulletin.id)+'/')
    else:
        form = BulletinForm()
    return render(request, 'submit.html', {'form': form})

@login_required()
def edit_bulletin(request, bulletin_id):
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    if request.user != bulletin.Author:
        return HttpResponseRedirect('/'+bulletin_id+'/')
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/'+bulletin_id+'/')
        bulletin.Title = request.POST["title"]
        bulletin.Pseudonym = request.POST["pseudonym"]
        bulletin.Location = request.POST["location"]
        bulletin.Description = request.POST["description"]
        bulletin.save()
        return HttpResponseRedirect('/'+bulletin_id+'/')
    return render(request, 'edit_bulletin.html', {
        'bulletin': bulletin,
    })