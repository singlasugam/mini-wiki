from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from . import util
import markdown2
import random

html = []

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, entry_title):
    global html 
    entries = list(util.list_entries())
    print(html)
    found = False
    for entry in entries:
        if entry == entry_title or entry.lower() == entry_title:
            html = markdown2.markdown(util.get_entry(entry_title))
            print(html)
            found = True
            print(found)
    if found:
        return render(request, 'encyclopedia/title.html', {'content' : html, 'title': entry_title})
    else:
        return render(request, 'encyclopedia/fail.html')
        
def search(request):
    if request.method ==  'POST':
        search = request.POST['search']
        entries = util.list_entries()
        print(entries)
        found = False
        for entry in entries:
            print(entry)
            if entry.lower() == search.lower():
                found = True
                return HttpResponseRedirect(f'wiki/{entry.lower()}')
        if found == False:
            pr = []
            for entry in entries:
                text = util.get_entry(entry)
                if search in text:
                    pr.append(entry)
                    found = True
                    print(found)
        return render(request, 'encyclopedia/search.html', {
                    'final' : pr, 'search':search
                })
            
def newentry(request): 
        return render(request, 'encyclopedia/newentry.html')

def check(request):
     if request.method == 'POST':
        newheading = request.POST['heading']
        content =  request.POST['content']
        entries = util.list_entries()
        if newheading not in entries:
            html = markdown2.markdown(content)
            util.save_entry(newheading,html)
            return HttpResponseRedirect(f'wiki/{newheading.lower()}')
        else:
            return render(request, 'encyclopedia/newentry.html', {
                'message': 'Same heading exists'
            })

def edit(request, title):
    content = util.get_entry(title)
    return render(request, 'encyclopedia/edit.html', {
        'heading': title, 'content': content
    })

def update(request, heading):
    if request.method == 'POST':
        up_head = request.POST['up_head']
        up_content = request.POST['up_content']
        util.delete(heading.lower())
        util.save_entry(up_head.lower(),up_content)
        print('save and delete done')
        return HttpResponseRedirect(reverse('title', kwargs={"entry_title": up_head.lower()})) 

def random_view(request):
    list = util.list_entries()
    view = random.choice(list)
    print(view)
    return HttpResponseRedirect(f'wiki/{view.lower()}')