from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bulletins.models import Bulletin, BulletinSearch, File, Folder

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
    docs = File.objects.filter(bulletin=bulletin)
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
    cur = Folder.objects.get(pk=folder_id)
    if request.user != cur.owner:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if 'bulletin' in request.POST:
            return HttpResponseRedirect('submit')
        elif 'delete' in request.POST:
            delete_folder(cur)
            return HttpResponseRedirect('/myBulletins/')
        elif 'folder' in request.POST:
            return HttpResponseRedirect('createFolder')
        elif 'copy' in request.POST:
            next = Folder()
            next.root = cur
            next.owner = cur.owner
            next.name = cur.name
            next.save()
            for bulletin in Bulletin.objects.filter(folder=cur):
                copy = copy_bulletin(bulletin)
                copy.folder = next
                copy.save()
            create_subs(cur, next)
            return HttpResponseRedirect('/folder/'+str(cur.id)+'/')
        elif 'move' in request.POST:
            if 'folder_select' in request.POST:
                move_folder_id = request.POST['folder_select']
                cur.root = Folder.objects.get(pk=move_folder_id)
                cur.save()
                return HttpResponseRedirect('/folder/'+str(folder_id)+'/')
    bulletins = Bulletin.objects.filter(folder=cur)
    folders = Folder.objects.filter(root=cur)
    folders_to_remove = []
    subfolders = Folder.objects.filter(root=cur)
    while len(subfolders) != 0:
        subfolders_temp = []
        for folder in subfolders:
            folders_to_remove.append(folder)
            for sub in Folder.objects.filter(root=folder):
                subfolders_temp.append(sub)
        subfolders = subfolders_temp
    all_folders = Folder.objects.filter(owner=request.user)
    for removed in folders_to_remove:
        all_folders = all_folders.exclude(pk=removed.id)
    all_folders = all_folders.exclude(pk=cur.id)
    if cur.root != None:
        all_folders = all_folders.exclude(pk=cur.root.id)
    is_root = cur.root is None
    return render(request, 'folder.html', {
        'folder': cur,
        'bulletins': bulletins,
        'folders': folders,
        'is_root': is_root,
        'all_folders': all_folders
    })

def create_subs(folder, copy):
    for folders in Folder.objects.filter(root=folder)
        next = Folder()
        next.root = copy
        next.owner = folder.owner
        next.name = folder.name
        next.save()
        for bulletin in Bulletin.objects.filter(folder=folder):
            copy = copy_bulletin(bulletin)
            copy.folder = next
            copy.save()
        create_subs(folders, next)

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
            copy = copy_bulletin(original)
            copy.folder = original.folder
            copy.save()
            return HttpResponseRedirect('/folder/'+str(original.folder.id)+'/')
        elif 'delete' in request.POST:
            Bulletin.objects.get(pk=bulletin_id).delete()
            return HttpResponseRedirect('/')
        elif 'move' in request.POST:
            if 'folder_select' in request.POST:
                move_folder_id = request.POST['folder_select']
                bulletin = Bulletin.objects.get(pk=bulletin_id)
                bulletin.folder = Folder.objects.get(pk=move_folder_id)
                bulletin.save()
                HttpResponseRedirect('/bulletin/'+str(bulletin_id)+'/')
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    docs = File.objects.filter(bulletin=bulletin)
    has_docs = len(docs) > 0
    owner = request.user == bulletin.Author
    folders = Folder.objects.filter(owner=bulletin.Author)
    return render(request, 'details.html', {
        'bulletin': bulletin,
        'owner': owner,
        'docs': docs,
        'has_docs': has_docs,
        'folders': folders
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
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')
        bulletin.Title = request.POST["title"]
        bulletin.Pseudonym = request.POST["pseudonym"]
        bulletin.Location = request.POST["location"]
        bulletin.Description = request.POST["description"]
        bulletin.save()
        handle_upload(request, bulletin)
        return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')
    docs = File.objects.filter(bulletin=bulletin)
    return render(request, 'edit_bulletin.html', {
        'bulletin': bulletin,
        'docs': docs
    })