from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from .forms import ContestantForm, PartnerContactForm
import logging
import os

logger = logging.getLogger(__name__)

# Static pages
def home(request):
    return render(request, 'landing/home.html')

def about(request):
    return render(request, 'landing/about.html')

def partners(request):
    return render(request, 'landing/partners.html')

def thank_you(request):
    return render(request, 'landing/thank_you.html')

# Partner contact form
@csrf_protect
def partners(request):
    if request.method == 'POST':
        form = PartnerContactForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            logger.info("Partner inquiry saved: %s", inquiry.name)

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
                logger.info("Partner inquiry email sent to admin.")

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
                logger.info("Confirmation email sent to partner.")

            except Exception as e:
                logger.exception("Partner contact email failed: %s", str(e))

            return redirect('thank_you')
    else:
        form = PartnerContactForm()

    return render(request, 'landing/partners.html', {'form': form})

# Contestant registration form
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
                    if contestant.video_submission and contestant.video_submission.storage.exists(contestant.video_submission.name):
                        try:
                            video_path = contestant.video_submission.path
                            logger.info("Video path: %s", video_path)
                            admin_email.attach_file(video_path)
                        except Exception as e:
                            logger.exception("Failed to attach video file: %s", str(e))
                    else:
                        logger.info("No video submission found or file missing.")

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

                return redirect('thank_you')
    else:
        form = ContestantForm()

    return render(request, 'landing/register.html', {'form': form})