from Crypto.Hash import SHA256
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bulletins.models import Bulletin, BulletinSearch, File, Folder



#import Pycrypt_egg.Crypto.Cipher



import os, random, struct
from Crypto.Cipher import AES


def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()



def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))




def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)



def recent_bulletins(recent=100):
    latest_bulletins = Bulletin.objects.all().order_by('-Date')[:recent]
    return latest_bulletins

def delete_folder(folder):
    bulletins = Folder.objects.filter(folder=folder)
    for bulletin in bulletins:
        bulletin.delete()
    subfolders = Folder.objects.filter(root=folder).exclude(pk=folder.id)
    for subfolder in subfolders:
        delete_folder(subfolder)
    print 'deleting folder'
    print folder.name
    folder.delete()

def handle_upload(request, bulletin):
    if 'files' in request.FILES:
            for i in request.FILES.getlist('files'):
                upload = File()
                upload.bulletin = bulletin
                upload.File_Field = i

                upload.save()

                key = getKey("some password") #hash+pad key for 16,32,64?   TODO Do something else with KEY ! ! !
                fileToEncrypt = upload.File_Field.path
                encryptedOutput = upload.File_Field.name
                encrypt_file(key, fileToEncrypt, encryptedOutput)   #Moved this to after Save. . .

"""

            key = getKey("some password") #hash+pad key for 16,32,64?   TODO Do something else with KEY

            someFileName = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\2014\11\30\saint-heaven-map.jpg"
            encrypt_file(key, someFileName, "testPic.jpg")

            someFileName2 = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\testPic.jpg"
            decrypt_file(key,someFileName2,  "decryptedTestPic.jpg" )  #TODO match file name and type when uploading.
            #  TODO If encruption = true for this file.  Encyrpt before storing loccally? Do what with keys?
"""


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
            pass
            #delete_folder(folder)
            #return HttpResponseRedirect('/myBulletins/')
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
        if 'edit' in request.POST:
            return HttpResponseRedirect('/bulletin/'+bulletin_id+'/edit/')
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
        return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')
    docs = File.objects.filter(bulletin=bulletin)
    return render(request, 'edit_bulletin.html', {
        'bulletin': bulletin,
        'docs': docs
    })