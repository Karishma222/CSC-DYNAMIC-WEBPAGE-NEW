from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SatBooking
from .models import Review, Achievement, Workshop, Course,Career
from .forms import  DemoForm, ContactForm
from .utils import send_demo_email
from .forms import SatBookingForm, TN_DISTRICTS



def home(request):
    if request.method == 'POST' and 'demo_submit' in request.POST:
        form = DemoForm(request.POST)
        if form.is_valid():
            demo = form.save()
            try:
                send_demo_email(
                    name        = demo.name,
                    mobile      = demo.mobile,
                    email       = demo.email,
                    description = demo.description,
                )
            except Exception as e:
                print(f"Email error: {e}")

            messages.success(
                request,
                f'Thank you {demo.name}! Demo booked. We will contact you soon.'
            )
            return redirect('home')
    else:
        form = DemoForm()

    context = {
        'form'        : form,
        'reviews'     : Review.objects.order_by('-created_at')[:6],
        'achievements': Achievement.objects.all(),
        'workshops'   : Workshop.objects.order_by('-created_at')[:6],
        'courses'     : Course.objects.all(),
    }
    return render(request, 'main/home.html', context)

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SatBookingForm


def registration(request):
    if request.method == 'POST':
        form = SatBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!')
            return redirect('courses')  
    else:
        form = SatBookingForm()
    return render(request, 'main/registration.html', {
        'form': form,
        'districts': TN_DISTRICTS,
    })


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()  # saves to DB

            name    = contact_msg.name
            phone   = contact_msg.phone
            email   = contact_msg.email
            message = contact_msg.message

            # ── 1. Email to YOU (admin) ────────────────────────
            send_mail(
                subject    = f'[CSC Anna Nagar] New Enquiry from {name}',
                message    = f"""New contact form submission:

Name    : {name}
Phone   : {phone}
Email   : {email}

Message:
{message}
""",
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = ['annanagarcsc2024@gmail.com'],
                fail_silently  = False,
            )

            # ── 2. Auto-reply to CLIENT ────────────────────────
            send_mail(
                subject    = 'Thank you for contacting CSC Anna Nagar!',
                message    = f"""Dear {name},

Thank you for reaching out to CSC Anna Nagar. We have received your message and our team will get back to you within a few hours on working days.

Your message:
"{message}"

If you need immediate help:
📞 Call: +91 9940909056
💬 WhatsApp: https://wa.me/919940909056

Best regards,
CSC Anna Nagar Team
AP-814, "G" Block, 1st Street, Anna Nagar, Chennai
""",
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [email],
                fail_silently  = True,
            )

            messages.success(request, "Your message has been sent! We'll be in touch soon.")
            return redirect('contact')

        else:
            messages.error(request, 'Please fix the errors below and try again.')

    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


def achievements_view(request):
    achievements = Achievement.objects.all()
    return render(request, 'main/achievements.html', {'achievements': achievements})


def workshop_view(request):
     workshop = Workshop.objects.order_by('-created_at')
     return render(request, 'main/workshop.html', {'workshop': workshop})

def placement(request):
     return render(request, 'main/placement.html',)


def reviews_view(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews})



def career_list(request):
    careers = Career.objects.all().order_by('-posted_on')
    return render(request, 'career.html', {'careers': careers})
# ── Add to your existing views.py ─────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import Career, JobApplication
from .forms import JobApplicationForm


def career_list(request):
    """Show all active job openings."""
    careers = Career.objects.filter(is_active=True).order_by('-posted_on')
    return render(request, 'main/career.html', {'careers': careers})


def apply_job(request, career_id):
    """Handle job application form submission via POST (AJAX-friendly)."""
    career = get_object_or_404(Career, id=career_id, is_active=True)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application        = form.save(commit=False)
            application.career = career
            application.save()

            # ── Email to applicant ────────────────────────────────
            applicant_msg = f"""
Dear {application.name},

Thank you for applying to CSC Anna Nagar Institute! 🎉

We have received your application for the role of:
✅ {career.role} ({career.employment_type})

Your Application Details:
──────────────────────────────────────
Name                  : {application.name}
Email                 : {application.email}
Mobile                : {application.mobile}
Highest Qualification : {application.highest_qualification}
Passed Out Year       : {application.passed_out_year}
Applied For           : {career.role}
Applied On            : {timezone.now().strftime('%d %b %Y  %I:%M %p')}
──────────────────────────────────────

Our team will review your application and contact you soon.

We look forward to connecting with you!

Best Regards,
CSC Anna Nagar Institute
AP-814, "G" Block, 1st Street,
Near Anna Nagar Tower, Anna Nagar, Chennai.
Phone : 9940909056
Email : annanagarcsc2024@gmail.com

"""
            send_mail(
                subject        = f'Application Received — {career.role} | CSC Anna Nagar',
                message        = applicant_msg,
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [application.email],
                fail_silently  = True,
            )

            # ── Email to institute (with resume attached) ─────────
            institute_msg = f"""
New Job Application Received
──────────────────────────────────────
Role Applied          : {career.role} ({career.employment_type})
──────────────────────────────────────
Applicant Name        : {application.name}
Email                 : {application.email}
Mobile                : {application.mobile}
Highest Qualification : {application.highest_qualification}
Passed Out Year       : {application.passed_out_year}
Cover Letter          : {application.cover_letter if application.cover_letter else '(not provided)'}
Applied On            : {timezone.now().strftime('%d %b %Y  %I:%M %p')}
──────────────────────────────────────
Resume is attached to this email.
"""
            email_with_resume = EmailMessage(
                subject        = f'New Application — {career.role} from {application.name}',
                body           = institute_msg,
                from_email     = settings.DEFAULT_FROM_EMAIL,
                to             = ['annanagarcsc2024@gmail.com'],
            )
            # Attach resume file
            try:
                application.resume.open()
                email_with_resume.attach(
                    application.resume.name.split('/')[-1],
                    application.resume.read(),
                    'application/octet-stream'
                )
                application.resume.close()
            except Exception:
                pass

            try:
                email_with_resume.send(fail_silently=False)
            except Exception as e:
                print(f"Institute email error: {e}")

            messages.success(
                request,
                f'Thank you {application.name}! Your application for "{career.role}" has been submitted successfully. We will contact you soon.'
            )
            return redirect('career')

        else:
            # Form invalid — return errors
            messages.error(request, 'Please fix the errors below and try again.')
            careers = Career.objects.filter(is_active=True)
            return render(request, 'main/career.html', {
                'careers':    careers,
                'form':       form,
                'open_career': career_id,
            })

    return redirect('career')



# ── Add to your existing views.py ────────────────────────────────────────

from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone
from .models import BookCourse, CourseBooking
from .forms import CourseBookingForm
from .models import SatBooking


def courses_page(request):
    """Show all active bookable courses."""
    courses = BookCourse.objects.filter(is_active=True)
    return render(request, 'main/courses.html', {'courses': courses})


def book_course(request, course_id):
    """Handle booking form POST → save → send emails → redirect to thank-you."""
    course = get_object_or_404(BookCourse, id=course_id, is_active=True)

    if request.method == 'POST':
        form = CourseBookingForm(request.POST)
        if form.is_valid():
            booking          = form.save(commit=False)
            booking.course   = course
            booking.save()

            booked_on_str = timezone.now().strftime('%d %b %Y  %I:%M %p')

            # ── Email to STUDENT ──────────────────────────────────
            student_msg = f"""
Dear {booking.student_name},

Thank you for booking with CSC Anna Nagar Institute! 🎉

Your booking has been received successfully.

╔══════════════════════════════════════════╗
   BOOKING CONFIRMATION
╚══════════════════════════════════════════╝

Booking Reference : {booking.booking_ref}
Course Name       : {course.name}
Duration          : {course.duration}
Amount to Pay     : ₹{course.offer_fee}
Booked On         : {booked_on_str}

Student Details:
  Name   : {booking.student_name}
  Email  : {booking.email}
  Mobile : {booking.mobile}

══════════════════════════════════════════
⚠️  IMPORTANT — PAYMENT INSTRUCTIONS
══════════════════════════════════════════

To CONFIRM your registration, please complete the payment of
₹{course.offer_fee} using our QR code on the booking page.

After payment:
  ✅ Take a screenshot of the payment confirmation
  ✅ Send it to our WhatsApp: 9940909056
     OR email to: annanagarcsc2024@gmail.com

  ✅ Screenshot is MANDATORY for registration

Without payment screenshot, your seat will NOT be confirmed.

══════════════════════════════════════════

We look forward to seeing you!

Best Regards,
CSC Anna Nagar Institute
AP-814, "G" Block, 1st Street,
Near Anna Nagar Tower, Anna Nagar, Chennai.
📞 9940909056
✉️  annanagarcsc2024@gmail.com

"""
            send_mail(
                subject        = f'Booking Confirmed — {course.name} | CSC Anna Nagar [{booking.booking_ref}]',
                message        = student_msg,
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = [booking.email],
                fail_silently  = True,
            )

            # ── Email to INSTITUTE ────────────────────────────────
            institute_msg = f"""
New Course Booking Received!
══════════════════════════════════════════

Booking Reference : {booking.booking_ref}
Course Name       : {course.name}
Duration          : {course.duration}
Amount            : ₹{course.offer_fee}
Booked On         : {booked_on_str}

Student Details:
  Name   : {booking.student_name}
  Email  : {booking.email}
  Mobile : {booking.mobile}

══════════════════════════════════════════
Action Required: Verify payment screenshot from student.
"""
            send_mail(
                subject        = f'New Booking — {course.name} from {booking.student_name} [{booking.booking_ref}]',
                message        = institute_msg,
                from_email     = settings.DEFAULT_FROM_EMAIL,
                recipient_list = ['annanagarcsc2024@gmail.com'],
                fail_silently  = False,
            )

            # Redirect to thank-you page with booking id
            return redirect('booking_success', booking_id=booking.id)

        else:
            # form errors — re-show courses page with errors
            courses = BookCourse.objects.filter(is_active=True)
            return render(request, 'main/courses.html', {
                'courses':     courses,
                'form_errors': form.errors,
                'open_course': course_id,
            })

    return redirect('courses')


def booking_success(request, booking_id):
    """Thank-you page shown after successful booking."""
    booking = get_object_or_404(CourseBooking, id=booking_id)
    return render(request, 'main/booking_success.html', {'booking': booking})

