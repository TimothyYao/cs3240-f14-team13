from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Bulletin, BulletinSearch, File, Folder, Permission
#from bulletins.models import Bulletin, BulletinSearch, File, Folder

def recent_bulletins(recent=100):
    latest_bulletins = Bulletin.objects.all().order_by('-Date')[:recent]
    return latest_bulletins

def delete_folder(folder):
    bulletins = Bulletin.objects.filter(folder=folder)
    for bulletin in bulletins:
        bulletin.delete()
    subfolders = Folder.objects.filter(root=folder)
    for subfolder in subfolders:
        delete_folder(subfolder)
    folder.delete()

def copy_bulletin(bulletin):
    copy = Bulletin()
    copy.Title = "" + bulletin.Title + " - copy"
    copy.Author = bulletin.Author
    copy.Pseudonym = bulletin.Pseudonym
    copy.Location = bulletin.Location
    copy.Description = bulletin.Description
    copy.folder = bulletin.folder
    docs = File.objects.filter(bulletin=bulletin)
    copy.save()
    for doc in docs:
        file_copy = File()
        file_copy.bulletin = copy
        file_copy.File_Field = doc.File_Field
        file_copy.save()
    return copy

def handle_upload(request, bulletin):
    if 'files' in request.FILES:
            for i in request.FILES.getlist('files'):
                upload = File()
                upload.bulletin = bulletin
                upload.File_Field = i
                #TODO encrypt here
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
def folder(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    if request.user != folder.owner:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if 'bulletin' in request.POST:
            return HttpResponseRedirect('submit')
        elif 'delete' in request.POST:
            delete_folder(folder)
            return HttpResponseRedirect('/myBulletins/')
        elif 'folder' in request.POST:
            return HttpResponseRedirect('createFolder')
    bulletins = Bulletin.objects.filter(folder=folder)
    folders = Folder.objects.filter(root=folder)
    is_root = folder.root is None
    return render(request, 'folder.html', {
        'folder': folder,
        'bulletins': bulletins,
        'folders': folders,
        'is_root': is_root
    })

@login_required()
def my_bulletins(request):
    folders = Folder.objects.filter(owner=request.user, name='root')
    if len(folders) == 0:
        folder = Folder()
        folder.owner = request.user
        folder.name = 'root'
        folder.save()
        folder_id = folder.id
    else:
        folder_id = folders[0].id
    return HttpResponseRedirect('/folder/'+str(folder_id)+'/')

@login_required()
def details(request, bulletin_id):
    if request.method == 'POST':
        if 'folder' in request.POST:
            folder_id = Bulletin.objects.get(pk=bulletin_id).folder.id
            return HttpResponseRedirect('/folder/'+str(folder_id)+'/')
        elif 'edit' in request.POST:
            return HttpResponseRedirect('/bulletin/'+bulletin_id+'/edit/')
        elif 'copy' in request.POST:
            original = Bulletin.objects.get(pk=bulletin_id)
            copy_bulletin(original)
            return HttpResponseRedirect('/folder/'+str(original.folder.id)+'/')
        elif 'delete' in request.POST:
            Bulletin.objects.get(pk=bulletin_id).delete()
            return HttpResponseRedirect('/')
        elif 'move' in request.POST:
            print 'move'
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    docs = File.objects.filter(bulletin=bulletin)
    has_docs = len(docs) > 0
    owner = request.user == bulletin.Author

    for doc in docs:
        doc.permission = (len(Permission.objects.filter(UserID=request.user.pk, FileID=doc.pk)) > 0 or owner)

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
def create_folder(request, folder_id):
    if request.method == 'POST':
        folder = Folder()
        folder.owner = request.user
        folder.root = Folder.objects.get(pk=folder_id)
        folder.name = request.POST['name']
        folder.save()
        return HttpResponseRedirect('/folder/'+str(folder_id)+'/')
    return render(request, 'create_folder.html')

@login_required()
def submit(request, folder_id):
    folder = Folder.objects.get(pk=folder_id)
    if request.user != folder.owner:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        bulletin = Bulletin()
        bulletin.Title = request.POST["title"]
        bulletin.Pseudonym = request.POST["pseudonym"]
        bulletin.Location = request.POST["location"]
        bulletin.Description = request.POST["description"]
        bulletin.Author = request.user
        bulletin.folder = folder
        bulletin.save()
        handle_upload(request, bulletin)
        return HttpResponseRedirect('/bulletin/'+str(bulletin.id)+'/')
    return render(request, 'submit.html')

@login_required()
def edit_bulletin(request, bulletin_id):
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    if request.user != bulletin.Author:
        return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')

    docs = File.objects.filter(bulletin=bulletin)

    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')
        bulletin.Title = request.POST["title"]
        bulletin.Pseudonym = request.POST["pseudonym"]
        bulletin.Location = request.POST["location"]
        bulletin.Description = request.POST["description"]
        bulletin.save()

        #updating input stuff

        for doc in docs:
            nameList = request.POST['text' + doc.File_Field.name].split(';')
            for name in nameList:
                if name == '': continue
                newName = name.strip()
                #create permission
                print 'about to query user: ' + newName
                newUser = User.objects.get(username=newName)
                newPermission = Permission(UserID=newUser, FileID=doc)
                check = Permission.objects.filter(UserID=newUser, FileID=doc)
                if newUser is request.user:
                    continue
                if (check is None):
                    newPermission.save()



        handle_upload(request, bulletin)
        return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')

    for doc in docs:
        doc.permissions = Permission.objects.filter(FileID=doc.pk)

    return render(request, 'edit_bulletin.html', {
        'bulletin': bulletin,
        'docs': docs
    })