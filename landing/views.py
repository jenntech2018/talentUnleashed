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
        form = ContestantForm(request.POST, request.FILES)
        if form.is_valid():
            is_group = form.cleaned_data.get('is_group')
            group_size = form.cleaned_data.get('group_size')

            if is_group and not group_size:
                form.add_error('group_size', 'Please specify the number of participants.')
            else:
                contestant = form.save()

                # Prepare email with attachment
                try:
                    from django.core.mail import EmailMessage

                    admin_email = EmailMessage(
                        subject="New Portland Brings Talent Registration",
                        body=(
                            f"{contestant.name_or_group_name} just registered with a talent of {contestant.talent_description}!\n"
                            f"Email: {contestant.email}"
                        ),
                        from_email='jenntech2018@gmail.com',
                        to=["jenntech2018@gmail.com"]
                    )

                    if contestant.video_submission:
                        admin_email.attach_file(contestant.video_submission.path)

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
                    logger.exception("Email send failed")

                return redirect('thank_you')
    else:
        form = ContestantForm()

    return render(request, 'landing/register.html', {'form': form})

def thank_you(request):
    return render(request, 'landing/thank_you.html')