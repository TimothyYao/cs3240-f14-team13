import os
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Bulletin, BulletinSearch, File, Folder, Permission  #TODO WAS THIS, trying fix. . .
#from bulletins.models import Bulletin, BulletinSearch, File, Folder


#from bulletins.models import Bulletin, Folder, File, Permission


from Crypto.Hash import SHA256
import os, random, struct
from Crypto.Cipher import AES


import shutil
import os
#os.environ['PYTHON_EGG_CACHE'] = '/usr/local/pylons/python-eggs'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'   #TODO remove this if un-needed.  Only adding to match my other working project.



def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

MASTER_KEY = getKey("some password")    #TODO NOTE< this may break files when server restarts and it generates a new random key


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
                elif len(chunk) % 16 != 0:  #JOHN ADDD
                    chunk += ' ' * (16 - len(chunk) % 16)  #JOHN ADDED

                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)











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
    copy.save()
    docs = File.objects.filter(bulletin=bulletin)
    for doc in docs:
        file_copy = File()
        file_copy.bulletin = copy
        file_copy.File_Field = doc.File_Field
        file_copy.Is_Encrypted = doc.Is_Encrypted
        file_copy.save()
        permissions = Permission.objects.filter(FileID=doc)
        for permission in permissions:
            new_permission = Permission()
            new_permission.FileID = file_copy
            new_permission.UserID = permission.UserID
            new_permission.save()
    return copy

def handle_upload(request, bulletin):
    if 'files' in request.FILES:
            for i in request.FILES.getlist('files'):
                print "for i in requests.Files, where i = "
                print i
                upload = File()

                upload.bulletin = bulletin
                upload.File_Field = i
                #TODO encrypt here
                print "Path and name before save: "
                print upload.File_Field.path
                print upload.File_Field.name
                upload.save()

                print "Path and name AFTER save: "
                print upload.File_Field.path
                print upload.File_Field.name

                fileToEncrypt = upload.File_Field.path  #WAS THIS . . . temp hard coding . .

                encryptedOutput = upload.File_Field.name #TODO temp setting to  inMagic


                pathForTemp = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\TEMP"
                encrypt_file(MASTER_KEY, fileToEncrypt, "tempFile")
                os.remove(fileToEncrypt)
                shutil.copyfile("tempFile", fileToEncrypt)  #copy then rename . . .
                os.remove("tempFile")

                #TODO encrypt to a new temp, delete the old location, save the file to the old location.  Then delete the temp file!
                # upload.delete()
                #
                # upload = File()
                # upload.bulletin = bulletin
                # upload.File_Field = i



#---------------------------------now testing decrypt and replace!------------

                decrypt_file(MASTER_KEY, fileToEncrypt, "tempFile")
                os.remove(fileToEncrypt)
                shutil.copyfile("tempFile", fileToEncrypt)  #copy then rename . . .
                os.remove("tempFile")

            #TODO THEN TEST DECRYPTING< with thesame copy and replace technique.
#------------------------------end decrypt and replace.  -------------------------


                print "---------------------"

                # print "The path and name of the uploaded file to encrypt are: "
                # print fileToEncrypt
                # print encryptedOutput
                #
                # encrypt_file(MASTER_KEY, fileToEncrypt, encryptedOutput)   #Moved this to after Save. . .
                # print "After enrypted, path is. . ."
                # print upload.File_Field._get_path
                #
                #
                # decrypt_file(MASTER_KEY, fileToEncrypt,  encryptedOutput ) #Does it blend?
                # tempForceOutPath = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\Puff6_in.jpg"
                # tempForceOutPath2 = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\Puff6_DECRYPTED.jpg"
                #
                # encrypt_file(MASTER_KEY, fileToEncrypt, tempForceOutPath)
                # decrypt_file(MASTER_KEY, tempForceOutPath,  tempForceOutPath2 ) #### THIS ONE SHOULD WORK !!!!

                #TODO delete file that's stored in fileToEncrypt's path. . .


                # encrypt_file(MASTER_KEY, fileToEncrypt, "Puff3_in.jpg")
                # pathOut = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\Puff3_in.jpg"
                # pathOut2 = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\Puff3.jpg"
                # decrypt_file(MASTER_KEY, pathOut,  pathOut2 ) #### THIS ONE SHOULD WORK !!!!


                #
                # alternatePath = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\damnit.png"
                # alternatePathFolder = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads"
                # alternatePathFake = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\RAGEEEEEEE\damnit.png"
                # print "Printing exists of: made up path, then real path to file.  Then real path to folder it's in. ."
                #
                # print os.path.exists(alternatePath)
                # print os.path.exists(alternatePathFake)
                # print os.path.exists(alternatePathFolder)
                # decrypt_file(MASTER_KEY, alternatePath,  "TOMATO_X.png" ) #Does it blend?
                #
                # alternatePathX = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\damnit.png"
                #
                # print "Printing exists of: made up path, then real path to file.  Then real path to folder it's in. ."
                #
                #
                # decrypt_file(MASTER_KEY, alternatePathX,  "DAMNIT_OUT.png" ) #Does it blend?




                # """ THIS WORKS for hard code and filez. . . BELOW"""
                # fileToEncrypt = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\castle01.jpg"
                # encryptedOutput = "In_RAGE.jpg"
                # encrypt_file(MASTER_KEY, fileToEncrypt, encryptedOutput)
                # dec_in = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\In_RAGE.jpg"
                # tempOut = "Out_RAGE.jpg"
                # decrypt_file(MASTER_KEY, dec_in,  tempOut )








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
        elif 'rename' in request.POST:
            return HttpResponseRedirect('/folder/'+str(folder_id)+'/edit/')
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

@login_required()
def rename_folder(request, folder_id):
    cur = Folder.objects.get(pk=folder_id)
    if request.user != cur.owner:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        folder = Folder.objects.get(pk=folder_id)
        folder.name = request.POST['name']
        folder.save()
        return HttpResponseRedirect('/folder/'+str(folder_id)+'/')
    return render(request, 'rename_folder.html')

def create_subs(folder, copy):
    for folders in Folder.objects.filter(root=folder):
        if folders.id == copy.id:
            continue
        next = Folder()
        next.root = copy
        next.owner = folders.owner
        next.name = folders.name
        next.save()
        for bulletin in Bulletin.objects.filter(folder=folders):
            new_bulletin = copy_bulletin(bulletin)
            new_bulletin.folder = next
            new_bulletin.save()
        create_subs(folders, next)

@login_required()
def my_bulletins(request):

#     #JOHN TEMP DERPING!!!
#     fileToEncrypt = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\castle01.jpg"
#     encryptedOutput = "In.jpg"
#     encrypt_file(MASTER_KEY, fileToEncrypt, encryptedOutput)
#     pathToIn = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\In.jpg"
#     decrypt_file(MASTER_KEY, pathToIn,  "Out.jpg" )
#
#
#     #Now doing a file inside the Uploads folder.. .
#
#     START = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\castle01.jpg"
#     MIDDLE = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\castle_IN.jpg"
#     encrypt_file(MASTER_KEY, START, MIDDLE)
#     END = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\castle_OUT.jpg"
#     decrypt_file(MASTER_KEY, MIDDLE,  END )  #Does this have access to and see files in here?
#                                             #How about files created by .save and not just dropped in?
#     #TODO  ^^ TEST THAT NEXT TO RULE OUT .SAVE BEING ISSUE>
#
#
#    #  NOW TESTING A FILE THAT WAS CREATED BY THE SAVE METHOD.  #TODO Then how about one being made at runtime?
# #TODO THIS ONE FAILED!!!  trying one created encryped by my other program and dropped in.  . next
#     #START = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\PuffGod.jpg"
#     MIDDLE = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\PuffGod.jpg"
#     #encrypt_file(MASTER_KEY, START, MIDDLE)
#     END = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\PuffGod_OUT.jpg"
#     decrypt_file(MASTER_KEY, MIDDLE,  END )  #Does this have access to and see files in here?
#                                             #How about files created by .save and not just dropped in?
#
#
#     MIDDLE = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\in_X.png"
#     #encrypt_file(MASTER_KEY, START, MIDDLE)
#     END = r"C:\Users\64\Documents\GitHub\cs3240-f14-team13\uploads\out_X.png"
#     decrypt_file(MASTER_KEY, MIDDLE,  END )  #Does this have access to and see files
#
#     #TODO SEE IF YOU CAN EVER DECRYPT A FILE CREATED WITH .SAVE() .  . ENCRYPTION (SEEMS) TO WORK tough which is odd.
#     #TODO TEST UPLOAD_ME.txt to see if same result in plzWork and here.



    #END JOHN TEMP DERPING!!!
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
            if 'folder_select' in request.POST:
                move_folder_id = request.POST['folder_select']
                bulletin = Bulletin.objects.get(pk=bulletin_id)
                bulletin.folder = Folder.objects.get(pk=move_folder_id)
                bulletin.save()
                HttpResponseRedirect('/bulletin/'+str(bulletin_id)+'/')
    bulletin = Bulletin.objects.get(pk=bulletin_id)
    docs = File.objects.filter(bulletin=bulletin)
    for doc in docs:
        print doc.File_Field.path
        doc.relative = os.path.basename(doc.File_Field.name)
    has_docs = len(docs) > 0
    owner = request.user == bulletin.Author

    for doc in docs:
        doc.permission = (len(Permission.objects.filter(UserID=request.user, FileID=doc)) > 0 or owner)

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

    docs = File.objects.filter(bulletin=bulletin)
    for doc in docs:
        doc.permissions = Permission.objects.filter(FileID=doc.pk)

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
            #name permission
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
                if (len(check) == 0):
                    newPermission.save()

            #encrypt check
            encryptDictKey = 'encrypt' + doc.File_Field.name
            encrypted = False

            key = getKey("some password")  # TODO is this hash always the same?..
            print "The hashed key for edit bulletin is:"
            print key


            if encryptDictKey in request.POST.keys():
                encrypted = True
                print "POST WAS TRUE"

                # #TODO if file is not encrypted, then ENCRYPT.
                # if doc.Is_Encrypted == True:
                #     encrypt_file()

                # fileToEncrypt = doc.File_Field.path
                # encryptedOutput = doc.File_Field.name
                # encrypt_file(key, fileToEncrypt, encryptedOutput)

            else:
                encrypted = False  #Then decrypt if it's not already*
                #todo if file is ...?
                print "POST WAS FALSE"
                print "WAS FILE object's isEncrypted field true?"
                if doc.Is_Encrypted == True:
                    print "model was encrypted"
                    fileToDecrypt = doc.File_Field.path
                    decryptedOutput = doc.File_Field.name
                    print "file to decrypt's path is . . ."
                    print fileToDecrypt
                    print "file to decrypt's name is . . ."
                    print decryptedOutput
                    #####decrypt_file(MASTER_KEY,fileToDecrypt,  decryptedOutput )
                    decrypt_file(MASTER_KEY, fileToDecrypt,  "MAGICK.png" )
                    print "File should be decrypted now. . ."


            encryptObject = File.objects.get(pk=doc.pk)
            encryptObject.Is_Encrypted = encrypted
            encryptObject.save()  #TODO move this inside ifs or leave?
            print "encrpyObject.save has been called"

            #permission delete
            for permission in doc.permissions:
                pDeleteKey = 'deletep' + permission.UserID.username + permission.FileID.File_Field.name
                willDelete = False
                if pDeleteKey in request.POST.keys():
                    willDelete = True
                else:
                    willDelete = False

                if willDelete:
                    print 'willdelete: ' + 'deletep' + permission.UserID.username + permission.FileID.File_Field.name
                    permission.delete()

            #delete the file
            deleteKey = 'delete' + doc.File_Field.name
            deleteFile = False
            if deleteKey in request.POST.keys():
                deleteFile = True
            else:
                deleteFile = False

            if deleteFile:
                print 'deleting file!!!'
                for permission in doc.permissions:
                    permission.delete()

                #TODO delete from hard disk!!
                doc.delete()


        handle_upload(request, bulletin)
        return HttpResponseRedirect('/bulletin/'+bulletin_id+'/')

    return render(request, 'edit_bulletin.html', {
        'bulletin': bulletin,
        'docs': docs
    })