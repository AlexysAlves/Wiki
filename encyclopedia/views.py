from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={
        "class": "search",
        "type": "text",
        "name": "q",
        "placeholder": "Search Encyclopedia"}))

class CreateForm(forms.Form):
    title = forms.CharField(label= "Title")
    text = forms.CharField(widget=forms.Textarea(), label='')

class EditForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def page(request, title): 
    page_content = util.get_entry(title)
    if page_content == None:
        return render(request, "encyclopedia/not_found.html", {
            "title": title,
            "form": SearchForm()
        })
 
    html_content = Markdown().convert(page_content)
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": html_content,
        "form": SearchForm()
    })
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["search"]
            page_content = util.get_entry(title)
            if page_content == None:
                similar = []
                for entry in util.list_entries():
                    if title in entry:
                        similar.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "title": title,
                    "similar_titles": similar,
                    "form": SearchForm()
                })
        
            return HttpResponseRedirect(reverse('page', args=[title]))
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })
def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {"form": SearchForm(), "title": title})
  
            util.save_entry(title,text)
            page_content = util.get_entry(title)
            html_content = Markdown().convert(page_content)

            return render(request, "encyclopedia/page.html", {
                'form': SearchForm(),
                'content': html_content,
                'title': title
            })
    return render(request, "encyclopedia/new_page.html", {"form": SearchForm(), "create_form": CreateForm()})

def edit(request, title):
    page_content = util.get_entry(title)
    if request.method == 'POST':
        form = EditForm(request.POST) 
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title,text)
            content = util.get_entry(title)
            html_content = Markdown().convert(content)

            return render(request, "encyclopedia/page.html", {
                'form': SearchForm(),
                'content': html_content,
                'title': title
            })
    

    return render(request, "encyclopedia/edit.html", {
        'form': SearchForm(),
        'edit': EditForm(initial={'text': page_content}),
        'title': title
    })

def randomP(request):
    if request.method == "GET":
        entries = util.list_entries()
        page = random.choice(entries)
        page_content = util.get_entry(page)
        html_content = Markdown().convert(page_content)
        return render(request, "encyclopedia/page.html", {
            'form': SearchForm(),
            'content': html_content,
            'title': page
        })