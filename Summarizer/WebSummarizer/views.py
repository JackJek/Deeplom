from django.shortcuts import render
from .algoritms import *
import time


def index(request):
    if request.POST:
        f = open(settings.MEDIA_ROOT + str(int(time.time())) + '.txt', 'w')  # infile
        f.write(request.POST.get('intext'))
        g = f.name
        f.close()
        tokenize(g)
        if request.POST.get('intext') and request.POST.get('theme'):
            theme(request.POST.get('theme'))
        if request.POST.get('intext') and not request.POST.get('theme'):
            summar(int(request.POST.get('id')))
        file = open(settings.MEDIA_ROOT + tm + 'Refing.txt', 'r')
        line = file.read()
        file.close()
        os.remove(settings.MEDIA_ROOT + tm + 'Refing.txt')
        return render(request, 'WebSummarizer/RSATUSummarizer.html', context={'name': line})
    else:
        return render(request, 'WebSummarizer/RSATUSummarizer.html')
