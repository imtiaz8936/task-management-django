from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")

def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")

def test(request):
    names = ["Imtiaz", "Mawa", "Imran", "Ridwan"]
    count = 0
    for name in names:
        count+=1
    context = {
        "names" : names,
        "age" : ["20", "26"],
        "count" : count
    }
    return render(request, "dashboard/test.html", context)

