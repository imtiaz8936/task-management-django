from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

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

def create_task(request):
    # employees = Employee.objects.all()
    form = TaskModelForm() # for GET

    # Saving the form into DB if method "POST"
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():

            """For Model Form Data"""
            form.save()
            return render(request, 'task_form.html',{"form":form, "message":"Task Added Successfully"})


            '''For Django Form Data'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to') # list['','',...]

            # task = Task.objects.create(
            #     title=title,description=description,due_date=due_date)

            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            
            # return HttpResponse("Task Added Successfully")

    context = {"form": form}
    return render(request, "task_form.html", context)

def view_task(request):
    #retrieve all data from Task Model
    tasks = Task.objects.all()
    return render(request, "show_task.html", {"tasks": tasks})
