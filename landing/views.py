from django.shortcuts import render, redirect
from .forms import ContestantForm
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage, BadHeaderError
import logging
import os
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def partners(request):
    return render(request, 'landing/partners.html')

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect


def partner_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        full_message = f"Partner Inquiry from {name} ({email}):\n\n{message}"

        send_mail(
            subject="New Partner/Sponsor Inquiry",
            message=full_message,
            from_email='jenntech2018@gmail.com',
            recipient_list=['jenntech2018@gmail.com'],
            fail_silently=False
        )

        return redirect('thank_you')

def register(request):
    if request.method == 'POST':
        form = ContestantForm(request.POST, request.FILES)
        if form.is_valid():
            is_group = form.cleaned_data.get('is_group')
            group_size = form.cleaned_data.get('group_size')

            if is_group and not group_size:
                form.add_error('group_size', 'Please specify the number of participants.')
            else:
                contestant = form.save()

                try:
                    # Prepare admin email
                    admin_email = EmailMessage(
                        subject="New Portland Brings Talent Registration",
                        body=(
                            f"{contestant.name_or_group_name} just registered with a talent of {contestant.talent_description}!\n"
                            f"Email: {contestant.email}"
                        ),
                        from_email='jenntech2018@gmail.com',
                        to=["jenntech2018@gmail.com"]
                    )

                    # Attach video if present
                    if contestant.video_submission:
                        try:
                            video_path = contestant.video_submission.path
                            if os.path.exists(video_path):
                                admin_email.attach_file(video_path)
                            else:
                                logger.warning("Video file not found at: %s", video_path)
                        except Exception as e:
                            logger.exception("Failed to attach video file: %s", str(e))

                    admin_email.send()

                    # Confirmation email to contestant
                    send_mail(
                        subject="Portland Brings Talent Registration Received",
                        message=(
                            f"Hi {contestant.name_or_group_name},\n\n"
                            "Thanks for registering for Portland Brings Talent! "
                            "We’ve received your submission and will be in touch soon.\n\n"
                            "Best,\nThe Portland Brings Talent Team"
                        ),
                        from_email='jenntech2018@gmail.com',
                        recipient_list=[contestant.email],
                        fail_silently=False
                    )

                except Exception as e:
                    logger.exception("Email send failed: %s", str(e))

                return redirect('thank_you')
    else:
        form = ContestantForm()

    return render(request, 'landing/register.html', {'form': form})

def thank_you(request):
    return render(request, 'landing/thank_you.html')