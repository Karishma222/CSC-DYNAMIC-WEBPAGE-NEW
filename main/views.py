from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.utils import timezone

from .models import (
    Review, Achievement, Workshop, Course, Career, 
    JobApplication, BookCourse, CourseBooking, 
    PlacementStep, PlacementService, 
    UpcomingWorkshop, WorkshopRegistration, SatBooking
)
from .forms import (
    DemoForm, ContactForm, SatBookingForm, 
    JobApplicationForm, CourseBookingForm, 
    PaymentSubmissionForm, WorkshopRegistrationForm
)
from .utils import send_demo_email
from .forms import TN_DISTRICTS


# =========================================================
# HOME & STATIC VIEWS
# =========================================================

def home(request):
    if request.method == 'POST' and 'demo_submit' in request.POST:
        form = DemoForm(request.POST)
        if form.is_valid():
            demo = form.save()
            try:
                send_demo_email(
                    name=demo.name,
                    mobile=demo.mobile,
                    email=demo.email,
                    description=demo.description,
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
        'form': form,
        'reviews': Review.objects.order_by('-created_at')[:6],
        'achievements': Achievement.objects.all(),
        'workshops': Workshop.objects.order_by('-created_at')[:6],
        'courses': Course.objects.all(),
    }
    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html')


def achievements_view(request):
    achievements = Achievement.objects.all()
    return render(request, 'main/achievements.html', {'achievements': achievements})


def reviews_view(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'main/reviews.html', {'reviews': reviews})


def placement(request):
    return render(request, 'main/placement.html', {
        'steps': PlacementStep.objects.filter(is_active=True),
        'services': PlacementService.objects.filter(is_active=True),
    })


def inspiration(request):
    return render(request, 'main/inspiration.html')


# =========================================================
# REGISTRATION & SAT BOOKING (From RP)
# =========================================================

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


# =========================================================
# CONTACT VIEW
# =========================================================

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()

            name = contact_msg.name
            phone = contact_msg.phone
            email = contact_msg.email
            message = contact_msg.message

            # Email to Admin
            send_mail(
                subject=f'[CSC Anna Nagar] New Enquiry from {name}',
                message=f"""New contact form submission:

Name    : {name}
Phone   : {phone}
Email   : {email}

Message:
{message}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['annanagarcsc2024@gmail.com'],
                fail_silently=False,
            )

            # Auto-reply to Client
            send_mail(
                subject='Thank you for contacting CSC Anna Nagar!',
                message=f"""Dear {name},

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
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True,
            )

            messages.success(request, "Your message has been sent! We'll be in touch soon.")
            return redirect('contact')
        else:
            messages.error(request, 'Please fix the errors below and try again.')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})


# =========================================================
# WORKSHOPS & UPCOMING WORKSHOPS
# =========================================================

def workshop_view(request):
    workshop = Workshop.objects.order_by('-created_at')
    upcoming = UpcomingWorkshop.objects.filter(
        is_active=True,
        date__gte=timezone.localdate()
    )
    return render(request, 'main/workshop.html', {
        'workshop': workshop,
        'upcoming': upcoming,
    })


def workshop_detail(request, pk):
    w = get_object_or_404(UpcomingWorkshop, pk=pk, is_active=True)
    return render(request, 'main/workshop_detail.html', {'w': w})


def workshop_register(request, pk):
    w = get_object_or_404(UpcomingWorkshop, pk=pk, is_active=True)

    if w.seats_left() == 0:
        messages.error(request, "Sorry, this workshop is full.")
        return redirect('workshop_detail', pk=w.pk)

    if request.method == 'POST':
        form = WorkshopRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if WorkshopRegistration.objects.filter(workshop=w, email=email).exists():
                messages.error(request, "You have already registered for this workshop.")
                return redirect('workshop_detail', pk=w.pk)

            reg = form.save(commit=False)
            reg.workshop = w
            reg.save()

            send_mail(
                subject=f'Workshop Registration - {w.title}',
                message=(
                    f"Dear {reg.name},\n\n"
                    f"Thank you for registering for {w.title} on {w.date:%d %b %Y}.\n"
                    f"Our team will contact you to confirm your seat.\n\n"
                    f"CSC Anna Nagar\nPhone: +91 9940909056"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reg.email],
                fail_silently=True,
            )
            send_mail(
                subject=f'New Workshop Registration - {w.title}',
                message=(
                    f"Name: {reg.name}\nEmail: {reg.email}\nMobile: {reg.mobile}\n"
                    f"Workshop: {w.title} ({w.date:%d %b %Y})"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['annanagarcsc2024@gmail.com'],
                fail_silently=True,
            )

            messages.success(
                request,
                f"Thank you {reg.name}! You are registered for {w.title}. We will contact you soon."
            )
            return redirect('workshop_detail', pk=w.pk)
    else:
        form = WorkshopRegistrationForm()

    return render(request, 'main/workshop_register.html', {'w': w, 'form': form})


# =========================================================
# CAREERS & JOB APPLICATIONS
# =========================================================

def career_list(request):
    """Show all active job openings."""
    careers = Career.objects.filter(is_active=True).order_by('-posted_on')
    return render(request, 'main/career.html', {'careers': careers})


def apply_job(request, career_id):
    """Handle job application form submission via POST."""
    career = get_object_or_404(Career, id=career_id, is_active=True)

    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.career = career
            application.save()

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

Best Regards,
CSC Anna Nagar Institute
AP-814, "G" Block, 1st Street, Anna Nagar, Chennai.
Phone : 9940909056
Email : annanagarcsc2024@gmail.com
"""
            send_mail(
                subject=f'Application Received — {career.role} | CSC Anna Nagar',
                message=applicant_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[application.email],
                fail_silently=True,
            )

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
                subject=f'New Application — {career.role} from {application.name}',
                body=institute_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['annanagarcsc2024@gmail.com'],
            )
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
                f'Thank you {application.name}! Your application for "{career.role}" has been submitted successfully.'
            )
            return redirect('career')
        else:
            messages.error(request, 'Please fix the errors below and try again.')
            careers = Career.objects.filter(is_active=True)
            return render(request, 'main/career.html', {
                'careers': careers,
                'form': form,
                'open_career': career_id,
            })

    return redirect('career')


# =========================================================
# COURSES, BOOKINGS & PAYMENTS
# =========================================================

def courses_page(request):
    """Show all active bookable courses."""
    courses = BookCourse.objects.filter(is_active=True)
    return render(request, 'main/courses.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(
        BookCourse,
        id=course_id,
        is_active=True,
    )
    return render(
        request,
        'main/course_details.html',
        {'course': course},
    )


def book_course(request, course_id):
    course = get_object_or_404(
        BookCourse,
        id=course_id,
        is_active=True
    )

    if request.method == 'POST':
        form = CourseBookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)
            booking.course = course
            booking.save()

            booked_on_str = timezone.now().strftime('%d %b %Y  %I:%M %p')

            # Email to Student
            student_msg = f"""
Dear {booking.student_name},

Thank you for booking with CSC Anna Nagar Institute! 🎉

Booking Reference : {booking.booking_ref}
Course Name       : {course.name}
Duration          : {course.duration}
Amount to Pay     : ₹{course.offer_fee}
Booked On         : {booked_on_str}

Please complete your payment to confirm your seat.
"""
            send_mail(
                subject=f'Booking Confirmed — {course.name} | CSC Anna Nagar [{booking.booking_ref}]',
                message=student_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[booking.email],
                fail_silently=True,
            )

            return redirect(
                'course_payment',
                booking_id=booking.id
            )
    else:
        form = CourseBookingForm()

    return render(
        request,
        'main/course_register.html',
        {
            'course': course,
            'form': form,
        }
    )


def course_payment(request, booking_id):
    booking = get_object_or_404(
        CourseBooking,
        id=booking_id
    )

    if booking.payment_status == 'paid':
        return redirect(
            'booking_success',
            booking_id=booking.id
        )

    if request.method == 'POST':
        form = PaymentSubmissionForm(
            request.POST,
            request.FILES,
            instance=booking
        )

        if form.is_valid():
            payment = form.save(commit=False)
            payment.payment_status = 'submitted'
            payment.save()

            return redirect(
                'booking_success',
                booking_id=booking.id
            )
    else:
        form = PaymentSubmissionForm(instance=booking)

    return render(
        request,
        'main/course_payment.html',
        {
            'booking': booking,
            'form': form,
        }
    )


def booking_success(request, booking_id):
    """Thank-you page shown after successful booking."""
    booking = get_object_or_404(CourseBooking, id=booking_id)
    return render(request, 'main/booking_success.html', {'booking': booking})