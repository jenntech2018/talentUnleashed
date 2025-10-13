from django.shortcuts import render, redirect
from .forms import ContestantForm

def home(request):
    return render(request, 'landing/home.html')
from django.core.mail import send_mail

from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST)
        if form.is_valid():
            contestant = form.save()
            send_mail(
                subject="New Talent Unleashed Registration",
                message=f"{contestant.name} just registered!\nEmail: {contestant.email}",
                from_email=None,  # uses DEFAULT_FROM_EMAIL
                recipient_list=["yourgmail@gmail.com"],
            )
            return redirect('thank_you')

def thank_you(request):
    return render(request, 'landing/thank_you.html')