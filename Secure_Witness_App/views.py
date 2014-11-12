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


@login_required
def home (request):  #takes no arguements. . .


    user = request.user


    t = loader.get_template('home.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))
    #return render_to_response('home.html')



@login_required
def bulletin_form (request):  #takes no arguements. . .

#Do I still have the username from request here?  Or is it lost. . .
    user = request.user


    t = loader.get_template('bulletin_form.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))



def secureWitness (request):  #takes no arguements. . .

#Do I still have the username from request here?  Or is it lost. . .
    user = request.user


    t = loader.get_template('secureWitness.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))





def register_account (request):  #takes no arguements. . .

#Do I still have the username from request here?  Or is it lost. . .

    # c = {}
    # c.update(csrf(request))

    if request.method == 'POST':
        print "there was a POST request. . ."
        print request.POST ['username']  #I can use this to pluck any id/name?'s value out of the post request on html page
        print request.POST ['password']
        name = request.POST ['username']
        pw = request.POST ['password']

        user = User.objects.create_user(username=name, password=pw) # no email.
        #    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')




        user.save()



        # create a form instance and populate it with data from the request:
            #form = NewAccountForm(request.POST)
        # check whether it's valid:
            #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
                #print "testing print"
                #print form.cleaned_data['register']  # lets see what we got here?



        return HttpResponseRedirect('/home/') #TODO maybe display a temp "success" page and redirect 5 sec

    # if a GET (or any other method) we'll create a blank form
    else:
    # form = NameForm()
    # //TODO else what??
        print 'else what? . . .' #
        #NewAccountForm()
    user = request.user


    t = loader.get_template('register_account.html')
    rc = RequestContext(request, {  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(rc)) #do I also need to pass the csrf to the html for token?  Is a token being passed automatically?

#//TODO extend user with user profile.  http://www.youtube.com/watch?v=qLRxkStiaUg .  for reader/author types

#  secure registration form:   http://www.youtube.com/watch?v=Tam4IGrPESg&list=PLxxA5z-8B2xk4szCgFmgonNcCboyNneMD
