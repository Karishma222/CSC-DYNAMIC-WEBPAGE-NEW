from django.db import models
from django.utils import timezone

# Create your models here.
# from django.db import models


class DemoRequest(models.Model):
    name = models.CharField(max_length=120)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
     return f"{self.name} - {self.mobile}"


class Review(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField()
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"Review by {self.name}"


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)

    image = models.ImageField(upload_to="achievements/", null=True, blank=True)

    def __str__(self):
        return self.title



class Workshop(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='workshops/')
    created_at = models.DateTimeField(auto_now_add=True)






# models.py — ContactMessage
class ContactMessage(models.Model):
    name    = models.CharField(max_length=100)
    phone   = models.CharField(max_length=15, blank=True)   # ← add this
    email   = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.email}"
 
 
class Course(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="courses/")
    url = models.URLField(blank=True, null=True)
    
    def __str__(self):
            return self.title
        
from django.db import models

class Career(models.Model):

    EMPLOYMENT_TYPES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    )

    role = models.CharField(max_length=200)
    job_description = models.TextField()
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    salary = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='careers/', blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role
    
# ── Add these to your existing models.py ──────────────────────────────────

from django.db import models


class Career(models.Model):
    EMPLOYMENT_TYPES = (
        ('Full Time',  'Full Time'),
        ('Part Time',  'Part Time'),
        ('Internship', 'Internship'),
        ('Contract',   'Contract'),
    )

    role            = models.CharField(max_length=200)
    job_description = models.TextField()
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    salary          = models.CharField(max_length=100, blank=True, null=True)
    location        = models.CharField(max_length=200, blank=True, null=True, default='Anna Nagar, Chennai')
    skills_required = models.TextField(blank=True, null=True, help_text="Comma separated skills")
    is_active       = models.BooleanField(default=True)
    image           = models.ImageField(upload_to='careers/', blank=True, null=True)
    posted_on       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role

    class Meta:
        ordering = ['-posted_on']


class JobApplication(models.Model):
    career              = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='applications')
    name                = models.CharField(max_length=150)
    email               = models.EmailField()
    mobile              = models.CharField(max_length=15)
    highest_qualification = models.CharField(max_length=200)
    passed_out_year     = models.CharField(max_length=10)
    resume              = models.FileField(upload_to='resumes/')
    cover_letter        = models.TextField(blank=True)
    applied_on          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.career.role}"

    class Meta:
        ordering = ['-applied_on']


# ── Add to your existing models.py ───────────────────────────────────────

from django.db import models


class BookCourse(models.Model):
    name            = models.CharField(max_length=200)
    duration        = models.CharField(max_length=100, help_text="e.g. 3 Months, 45 Days")
    original_fee    = models.DecimalField(max_digits=8, decimal_places=2, help_text="Original price (strike-through)")
    offer_fee       = models.DecimalField(max_digits=8, decimal_places=2, help_text="Discounted price shown to students")
    offer_label     = models.CharField(max_length=80, blank=True, null=True, help_text="e.g. 50% OFF, Limited Offer")
    description     = models.TextField(help_text="Course overview shown on the card")
    highlights      = models.TextField(blank=True, null=True, help_text="Comma separated points e.g. Live Projects,Certificate,Placement Support")
    image           = models.ImageField(upload_to='courses/booking/', blank=True, null=True)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def discount_percent(self):
        if self.original_fee > 0:
            return int(((self.original_fee - self.offer_fee) / self.original_fee) * 100)
        return 0

    class Meta:
        ordering = ['name']


class CourseBooking(models.Model):
    course          = models.ForeignKey(BookCourse, on_delete=models.CASCADE, related_name='bookings')
    student_name    = models.CharField(max_length=150)
    email           = models.EmailField()
    mobile          = models.CharField(max_length=15)
    booking_ref     = models.CharField(max_length=20, unique=True, editable=False)
    booked_on       = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            import random, string
            self.booking_ref = 'CSC' + ''.join(random.choices(string.digits, k=7))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} — {self.course.name} ({self.booking_ref})"

    class Meta:
        ordering = ['-booked_on']


class SatBooking(models.Model):
    name          = models.CharField(max_length=50)
    address       = models.CharField(max_length=150)
    gender        = models.CharField(max_length=25)
    qualification = models.CharField(max_length=200)
    district      = models.CharField(max_length=50)
    area          = models.CharField(max_length=50)
    timing        = models.CharField(max_length=25)
    mobile        = models.CharField(max_length=25)
    email         = models.EmailField()
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"