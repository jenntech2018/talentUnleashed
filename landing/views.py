from django.shortcuts import render, redirect
from .forms import ContestantForm

def home(request):
    return render(request, 'landing/home.html')

from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)

from django.core.mail import send_mail, BadHeaderError
import logging

logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST)
        if form.is_valid():
            contestant = form.save()
            try:
                # Email to admin
                send_mail(
                    subject="New Portland Brings Talent Registration",
                    message=f"{contestant.name_or_group_name} just registered with a talent of {contestant.talent_description}!\nEmail: {contestant.email}",
                    from_email='jenntech2018@gmail.com',
                    recipient_list=["jenntech2018@gmail.com"],
                    fail_silently=False
                )

                # Email to contestant
                send_mail(
                    subject="Portland Brings Talent Registration Received",
                    message=(
                        f"Hi {contestant.name_or_group_name},\n\n"
                        "Thanks for registering for Talent Unleashed! "
                        "We’ve received your submission and will be in touch soon.\n\n"
                        "Best,\nThe Talent Unleashed Team"
                    ),
                    from_email='jenntech2018@gmail.com',
                    recipient_list=[contestant.email],
                    fail_silently=False
                )

            except BadHeaderError:
                logger.error("Invalid header found in registration email.")
            except Exception as e:
                logger.exception("Email send failed")
            return redirect('thank_you')
    else:
        form = ContestantForm()
    return render(request, 'landing/register.html', {'form': form})


def thank_you(request):
    return render(request, 'landing/thank_you.html')