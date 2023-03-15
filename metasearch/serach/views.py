from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import URLdata
from .modules import mse


def mainp(request):
    if request.method == "POST":
        term = request.POST["query"]
        return search_term(request, term)
    else:
        term = ""
        URLdata.objects.all().delete()
    return render(request, "myfirst.html", {"term": term})


def search_term(request, query):
    king = mse.mse(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', query)
    sol = king.search_query()
    # sol[0]->url, sol[1]->rank
    for res in sol:
        q = URLdata(url=res[0], rank=res[1][0], title=res[1][2], se=res[1][1])
        q.save()
    print("db saved!")
    objs = URLdata.objects.all()
    stu = {"res_number": objs}
    return render(request, "results.html", stu)
    # return render(request,"show.html",{"list":str(sol)})


def serach(request):
    pass
