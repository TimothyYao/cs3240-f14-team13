from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import loader, Context
#from polls.models import Poll

from django.contrib.auth.decorators import login_required

""" looks like index is the main page and somehow branches down to others.
 It sets up the loaded template T and passes some data in context C to the html page it renders.  """

""" looks like poll list data from the database being turned into an obect and passed through the context into render so html can grab it on the other side and loop through the items or wahtever.  okay."""
# def index(request):
#     poll_list = Poll.objects.all()
#     t = loader.get_template('index.html')
#     c = Context({
#         'poll_list': poll_list,
#     })
#     return HttpResponse(t.render(c))
#     #return render_to_response('index.html')
#
#
# def details(request, poll_id):
#     return render_to_response('details.html')
#
#
# def results(request, poll_id):
#     return render_to_response('results.html')
#
#
# def vote(request, poll_id):
#     return render_to_response('vote.html')

@login_required
def home (request):  #takes no arguements. . .


    user = request.user


    t = loader.get_template('home.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))
    #return render_to_response('home.html')

## //todo so what is a context here and what's it doing with those squigilies?

""" This works to load a page, trying the method with loader.get_templates above now.  And why would you use which when?"""
"""Maybe one is to pass values and data to the HTML page and the other is just for pure HTML? (with no params, can still have embeded python)"""
#http://stackoverflow.com/questions/11873084/typeerror-render-page-takes-exactly-2-arguments-1-given
#https://www.google.com/search?q=django+render%28%29+takes+exactly+2+arguments+%281+given%29&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:en-US:official&client=firefox-a&channel=sb

# def home (request):  #takes no arguements. . .
#     #t = loader.get_template('home.html')
#     #return HttpResponse(t.render())
#     return render_to_response('home.html')


#"  if a call to a method does any sort of state change to the backend (from template) you dont want to do that there
#calls to methods in templates should be basically equal to checking hte property of an object.


# TODO If the user type is an Author, then also display a link to submit a 'bulletin' form.
# TODO create registration page where users can choose to be a reader or author. . .
#todo allow users to change account type later on?  Or what.  hows that gonna work?

@login_required
def bulletin_form (request):  #takes no arguements. . .

#Do I still have the username from request here?  Or is it lost. . .
    user = request.user


    t = loader.get_template('bulletin_form.html')
    c = Context({  #does context take in like a dictionary of random objects? ..
        'thing1': 'silly string', 'user': user,
    })
    return HttpResponse(t.render(c))