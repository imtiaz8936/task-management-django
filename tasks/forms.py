from django import forms
from django.forms import ModelForm
from tasks.models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Events for Participant"
    )

    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
