from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def send_demo_email(name, mobile, email, description):

    # ── Email to YOU (institute) ──────────────────────────────
    institute_message = f"""
New Demo Booking Received
─────────────────────────────────────
Name        : {name}
Mobile      : {mobile}
Email       : {email}
Description : {description if description else '(not provided)'}
Submitted   : {timezone.now().strftime('%d %b %Y  %I:%M %p')}
─────────────────────────────────────
CSC Anna Nagar Institute
"""
    send_mail(
        subject        = f"New Demo Booking — {name}",
        message        = institute_message,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = ['cscannanagar@gmail.com'],
        fail_silently  = False,
    )

    # ── Confirmation email to STUDENT ────────────────────────
    student_message = f"""
Dear {name},

Thank you for booking a demo at CSC Anna Nagar Institute!

Our team will contact you shortly on {mobile}.

Your Booking Details:
──────────────────────────────
Name        : {name}
Mobile      : {mobile}
Email       : {email}
Description : {description if description else '—'}
──────────────────────────────

We look forward to seeing you!

Best Regards,
CSC Anna Nagar Institute
AP-814, "G" Block, 1st Street,
Near Anna Nagar Tower, Anna Nagar, Chennai.
Phone : 9940909056
"""
    send_mail(
        subject        = 'Demo Booking Confirmed — CSC Anna Nagar',
        message        = student_message,
        from_email     = settings.DEFAULT_FROM_EMAIL,
        recipient_list = [email],
        fail_silently  = True,
    )