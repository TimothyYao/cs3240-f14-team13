from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
#from polls.models import Poll

from django.contrib.auth.decorators import login_required

from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf

from models import Bulletin


#todo uploading a file using forms example:
# http://stackoverflow.com/questions/5871730/need-a-minimal-django-file-upload-example

#http://www.djangobook.com/en/2.0/appendixA.html  'make sure directory is writable by the serb server's user account'

@login_required
def home (request):


    user = request.user


    t = loader.get_template('home.html')
    c = Context({
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))
    #return render_to_response('home.html')



@login_required
def bulletin_form (request):  #takes no arguements. . .


    user = request.user

    if request.method == 'POST':
        print "there was a POST request. . ."
        print request.POST ['authorID']
        print request.POST ['theDate']
        print request.POST ['postCode']
        print request.POST ['country']
        print request.POST ['address']
        print request.POST ['description']


        Author_ID =  request.POST ['authorID']
        Date =  request.POST ['theDate']
        Post_Code =request.POST ['postCode']
        Country = request.POST ['country']
        Description = request.POST ['description']
        Address = request.POST ['address']
        #file = request.POST['someFile']
        file= request.FILES['someFile']
        print "the file was: ", file

        b = Bulletin(Author_ID = Author_ID, Date = Date, Address = Address, Post_Code = Post_Code, Country = Country, Description = Description, File_Field = file)


        b.save()
        derp = b.Description
        print "The description in Database for this bulletin is saved as", derp



        return HttpResponseRedirect('/home/') #TODO maybe display a temp "success" page and redirect 5 sec


    else:

    # //TODO else what??
        print 'else what? . . .' #




    t = loader.get_template('bulletin_form.html')
    # c = Context({  #does context take in like a dictionary of random objects? ..
    #     'thing1': 'silly string', 'user': user,
    # })
    #return HttpResponse(t.render(c))

    rc = RequestContext(request, {  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(rc))  #Remember, must include the csrf token line in HTML of page getting requestContext



def secureWitness (request):
    user = request.user
    t = loader.get_template('secureWitness.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))





def register_account (request):

    if request.method == 'POST':
        print "there was a POST request. . ."
        print request.POST ['username']  #I can use this to pluck any id/name?'s value out of the post request on html page
        print request.POST ['password']
        name = request.POST ['username']
        pw = request.POST ['password']

        user = User.objects.create_user(username=name, password=pw) # no email.
        #    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        user.save()
        return HttpResponseRedirect('/home/') #TODO maybe display a temp "success" page and redirect 5 sec

    else:
    # //TODO else what??
        print 'else what? . . .' #

    user = request.user
    t = loader.get_template('register_account.html')
    rc = RequestContext(request, {  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(rc)) #do I also need to pass the csrf to the html for token?  Is a token being passed automatically?

#//TODO extend user with user profile.  http://www.youtube.com/watch?v=qLRxkStiaUg .  for reader/author types

#  secure registration form:   http://www.youtube.com/watch?v=Tam4IGrPESg&list=PLxxA5z-8B2xk4szCgFmgonNcCboyNneMD



#  https://github.com/tschellenbach/Django-facebook/issues/214
#  possible solution: " Finally I solved it by creating manually all the missing columns
#  in the "dbshell", using first the command "sqlall" to know which columns I had to create"


"""

BEGIN;
CREATE TABLE "Secure_Witness_App_bulletin" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "Author_ID" text NOT NULL,
    "Date" text NOT NULL,
    "Address" text NOT NULL,
    "Post_Code" text NOT NULL,
    "Country" text NOT NULL,
    "Description" text NOT NULL,
    "File_Field" varchar(100) NOT NULL
)
;

COMMIT;


"""