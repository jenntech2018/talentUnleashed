from django.shortcuts import render, redirect
from .forms import ContestantForm

def home(request):
    return render(request, 'landing/home.html')

from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST)
        if form.is_valid():
            contestant = form.save()
            try:
                send_mail(
                    subject="New Talent Unleashed Registration",
                    message=f"{contestant.name} just registered - Their talent is: {contestant.talent_description}!\nEmail: {contestant.email}",
                    from_email=None,  # uses DEFAULT_FROM_EMAIL from settings.py
                    recipient_list=["jenntech2018@gmail.com"],
                    fail_silently=False  # set to True if you want to suppress errors
                )
            except BadHeaderError:
                logger.error("Invalid header found in registration email.")
            except Exception as e:
                logger.error(f"Email send failed: {e}")
            return redirect('thank_you')
    else:
        form = ContestantForm()
    return render(request, 'landing/register.html', {'form': form})


def thank_you(request):
    return render(request, 'landing/thank_you.html')