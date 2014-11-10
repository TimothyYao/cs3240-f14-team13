from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import loader, Context
from polls.models import Poll


def index(request):
    poll_list = Poll.objects.all()
    t = loader.get_template('index.html')
    c = Context({
        'poll_list': poll_list,
    })


    return HttpResponse(t.render(c))
    #return render_to_response('index.html')


def details(request, poll_id):
    return render_to_response('details.html')


def results(request, poll_id):
    return render_to_response('results.html')


def vote(request, poll_id):
    return render_to_response('vote.html')