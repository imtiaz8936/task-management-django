from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.http import JsonResponse
from datetime import date
from django.http import HttpResponse
from tasks.forms import EventForm, ParticipantForm, CategoryForm
from tasks.models import Event, Participant, Category

# Create your views here.

def base(request):
    past_events_display = Event.objects.filter(date__lt=date.today()).order_by('-date')[:3]  
    return render(request, 'base.html' and 'home.html', {'past_events_display': past_events_display})

def event_list(request):
    events = Event.objects.all().order_by('-date', '-time').select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    search_term = request.GET.get('search')
    if search_term:
        events = events.filter(Q(name__icontains=search_term) | Q(location__icontains=search_term))
    return render(request, 'event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form, 'form_type': 'Create'})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form, 'form_type': 'Update'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})


def participant_list(request):
    participants = Participant.objects.all()
    return render(request, 'participant_list.html', {'participants': participants})


def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form, 'form_type': 'Create'})


def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list') 
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form, 'form_type': 'Update'})


def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})


def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'form_type': 'Create'})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'form_type': 'Update'})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

def dashboard(request):
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    today = date.today()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    today_events = Event.objects.filter(date=today).select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    events = Event.objects.all().order_by('-date', '-time').select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))

    selected_filter = request.GET.get('filter', 'today')

    if selected_filter == 'upcoming':
        events = Event.objects.filter(date__gte=today).order_by('date', 'time').select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    elif selected_filter == 'past':
        events = Event.objects.filter(date__lt=today).order_by('-date', '-time').select_related('category').prefetch_related('participants').annotate(participant_count=Count('participants'))
    elif selected_filter == 'today':
        events = today_events.order_by('date', 'time')

    return render(request, 'dashboard.html', {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'today_events': today_events,
        'today': today,
        'events': events,
        'selected_filter': selected_filter,
    })