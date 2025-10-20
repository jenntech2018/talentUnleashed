from django.shortcuts import render, redirect
from .forms import ContestantForm
from django.http import HttpResponse
from django.core.mail import send_mail, EmailMessage, BadHeaderError
import logging
import os

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def partners(request):
    return render(request, 'landing/partners.html')

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect

from .forms import PartnerContactForm
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect

# views.py
@csrf_protect
def partner_contact(request):
    if request.method == 'POST':
        form = PartnerContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()

            try:
                # Admin notification
                admin_email = EmailMessage(
                    subject="New Partner/Sponsor Inquiry",
                    body=(
                        f"Partner Inquiry from {inquiry.name} ({inquiry.email}):\n\n{inquiry.message}"
                    ),
                    from_email='jenntech2018@gmail.com',
                    to=['jenntech2018@gmail.com'],
                    reply_to=[inquiry.email]
                )
                admin_email.send()

                # Confirmation to partner
                send_mail(
                    subject="Thanks for reaching out to Portland Brings Talent",
                    message=(
                        f"Hi {inquiry.name},\n\n"
                        "Thanks for your interest in partnering with Portland Brings Talent! "
                        "We’ve received your message and will be in touch soon.\n\n"
                        "Best,\nThe Portland Brings Talent Team"
                    ),
                    from_email='jenntech2018@gmail.com',
                    recipient_list=[inquiry.email],
                    fail_silently=False
                )

            except Exception as e:
                logger.exception("Partner contact email failed: %s", str(e))

            return render(request, 'landing/thank_you.html')
    else:
        form = PartnerContactForm()

    return render(request, 'landing/partner_contact.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import ContestantForm
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_protect
import logging
import os

logger = logging.getLogger(__name__)

@csrf_protect
def register(request):
    if request.method == 'POST':
        logger.info("Received POST to /register/")
        form = ContestantForm(request.POST, request.FILES)
        logger.info("Form is valid: %s", form.is_valid())

        if form.is_valid():
            is_group = form.cleaned_data.get('is_group')
            group_size = form.cleaned_data.get('group_size')

            if is_group and (not group_size or group_size < 2):
                form.add_error('group_size', 'Please specify a valid number of participants (minimum 2).')
            else:
                contestant = form.save()
                logger.info("Saved contestant: %s", contestant.name_or_group_name)

                try:
                    # Admin notification
                    admin_email = EmailMessage(
                        subject="New Portland Brings Talent Registration",
                        body=(
                            f"{contestant.name_or_group_name} just registered with a talent of {contestant.talent_description}!\n"
                            f"Email: {contestant.email}"
                        ),
                        from_email='jenntech2018@gmail.com',
                        to=['jenntech2018@gmail.com'],
                        reply_to=[contestant.email]
                    )

                    # Attach video if present
                    if contestant.video_submission:
                        try:
                            video_path = contestant.video_submission.path
                            logger.info("Video path: %s", video_path)
                            if os.path.exists(video_path):
                                admin_email.attach_file(video_path)
                            else:
                                logger.warning("Video file not found at: %s", video_path)
                        except Exception as e:
                            logger.exception("Failed to attach video file: %s", str(e))

                    admin_email.send()
                    logger.info("Admin email sent successfully.")

                    # Confirmation to contestant
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
                    logger.info("Confirmation email sent to contestant.")

                except Exception as e:
                    logger.exception("Email send failed: %s", str(e))

                return render(request, 'landing/thank_you.html')
    else:
        form = ContestantForm()

    return render(request, 'landing/register.html', {'form': form})

def thank_you(request):
    return render(request, 'landing/thank_you.html')
