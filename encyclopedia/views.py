from django import forms
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown
import random
from . import util


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

        return render(request, 'encyclopedia/entry.html', {
            "title":create_title,
            'content':create_content
        })
    return render(request, "encyclopedia/create.html")


def randomPage(request):
    all_items = util.list_entries()
    num = random.randint(0, len(all_items)-1)
    title = all_items[num]
    return redirect('show_item', title = title)


def show_item(request, title):
    content = util.get_entry(title)

    if not content:
        return render(request, "encyclopedia/error.html",{
            "message": "Page was not found"
            })

    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
        })


def edit(request, title):
    content = util.get_entry(title.strip())

    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "Can't find this page.Please check again"
            })

    if request.method == "POST":
        new_title = request.POST.get("title").strip()
        new_content = request.POST.get("content").strip()
        if not new_content or not new_title:
            return render(request, "encyclopedia/edit.html", {
                "message": "Can't save with empty content",
                "title": new_title,
                "content": new_content
                })
        if new_title != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
        util.save_entry(new_title, new_content)
        return render(request, "encyclopedia/entry.html", {
            "title": new_title,
            "content": new_content
            })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
        })


def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("show_item", title=q)
    return render(request, "encyclopedia/search.html", {"searched": util.search(q), "q": q})
