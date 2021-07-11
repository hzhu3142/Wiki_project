from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
from markdown2 import Markdown


markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == 'POST':
        #create a new wiki item
        create_title = request.POST.get("title").strip()
        create_content = request.POST.get("content").strip()
        all_items = util.list_entries()
        if create_title in all_items:
            return render(request, "encyclopedia/create.html", {"message": "Error: this entry already exist."})

        if not create_title or not create_content:
            return render(request, "encyclopedia/create.html", {
                "message": "Error: this entry must have both title and content.",
                "title": create_title,
                "content": create_content
                })

        util.save_entry(create_title, create_content)
        item = util.get_entry(create_title)
        item_html = markdowner.convert(item)
        return render(request, 'encyclopedia/entry.html', {
            "title":create_title,
            'content':create_content
        })
    return render(request, "encyclopedia/create.html")


def randomPage(request):
    pass


def show_item(request):
    pass


def search(request):
    pass
