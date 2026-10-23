from django.db import models
import random
import string

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
    image = models.ImageField(upload_to="reviews/", blank=True, null=True)
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
    image = models.ImageField(upload_to="workshops/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Workshop {self.pk}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
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

class Career(models.Model):

    EMPLOYMENT_TYPES = (
        ("Full Time", "Full Time"),
        ("Part Time", "Part Time"),
        ("Internship", "Internship"),
        ("Contract", "Contract"),
    )

    role = models.CharField(max_length=200)
    job_description = models.TextField()
    employment_type = models.CharField(max_length=50, choices=EMPLOYMENT_TYPES)
    salary = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(
        max_length=200, blank=True, null=True,
        default="Anna Nagar, Chennai"
    )
    skills_required = models.TextField(
        blank=True, null=True, help_text="Comma separated skills"
    )
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="careers/", blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role

    class Meta:
        ordering = ["-posted_on"]

class JobApplication(models.Model):
    career = models.ForeignKey(
        Career, on_delete=models.CASCADE, related_name="applications"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    highest_qualification = models.CharField(max_length=200)
    passed_out_year = models.CharField(max_length=10)
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.career.role}"

    class Meta:
        ordering = ["-applied_on"]

class BookCourse(models.Model):

    CATEGORY_CHOICES = [
        ("Software Development", "Software Development"),
        ("Web Development", "Web Development"),
        ("Programming", "Programming"),
        ("UI / UX", "UI / UX"),
        ("Digital Marketing", "Digital Marketing"),
        ("Cloud Computing", "Cloud Computing"),
    ]
    MODE_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("Hybrid", "Hybrid"),
    ]
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default="Software Development"
    )
    mode = models.CharField(
        max_length=20, choices=MODE_CHOICES, default="Offline"
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="Beginner"
    )
    duration = models.CharField(max_length=100, help_text="e.g. 3 Months, 45 Days")
    original_fee = models.DecimalField(max_digits=8, decimal_places=2)
    offer_fee = models.DecimalField(max_digits=8, decimal_places=2)
    offer_label = models.CharField(max_length=80, blank=True, null=True)
    description = models.TextField()
    highlights = models.TextField(blank=True, null=True)
    roadmap = models.TextField(
        blank=True, null=True, help_text="Enter each roadmap step on a new line"
    )
    image = models.ImageField(upload_to="courses/booking/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def discount_percent(self):
        if self.original_fee and self.original_fee > 0:
            discount = ((self.original_fee - self.offer_fee) / self.original_fee) * 100
            return round(discount)
        return 0

    def get_roadmap_steps(self):
        if not self.roadmap:
            return []
        return [step.strip() for step in self.roadmap.splitlines() if step.strip()]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class CourseBooking(models.Model):

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Payment Pending"),
        ("submitted", "Verification Pending"),
        ("paid", "Paid"),
        ("rejected", "Payment Rejected"),
    ]

    course = models.ForeignKey(
        BookCourse, on_delete=models.CASCADE, related_name="bookings"
    )
    student_name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    booking_ref = models.CharField(max_length=20, unique=True, editable=False)
    booked_on = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_proof = models.ImageField(upload_to="payment_proofs/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.booking_ref:
            while True:
                reference = "CSC" + "".join(random.choices(string.digits, k=7))
                if not CourseBooking.objects.filter(booking_ref=reference).exists():
                    self.booking_ref = reference
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_name} — {self.course.name} ({self.booking_ref})"

    class Meta:
        ordering = ["-booked_on"]

class SatBooking(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    gender = models.CharField(max_length=25)
    qualification = models.CharField(max_length=200)
    district = models.CharField(max_length=50)
    area = models.CharField(max_length=50)
    timing = models.CharField(max_length=25)
    mobile = models.CharField(max_length=25)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.mobile}"

class PlacementStep(models.Model):
    order = models.PositiveSmallIntegerField(default=1)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]


class PlacementService(models.Model):
    order = models.PositiveSmallIntegerField(default=1)
    icon = models.CharField(max_length=10, default="📄")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]

class UpcomingWorkshop(models.Model):
    MODE_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("Hybrid", "Hybrid"),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="workshops/upcoming/", blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default="Offline")
    venue = models.CharField(max_length=200, blank=True)
    short_description = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    seats = models.PositiveIntegerField(
        null=True, blank=True, help_text="Leave empty for unlimited seats"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def seats_left(self):
        if self.seats is None:
            return None
        return max(self.seats - self.registrations.count(), 0)

    def __str__(self):
        return f"{self.title} ({self.date})"

    class Meta:
        ordering = ["date", "start_time"]


class WorkshopRegistration(models.Model):
    workshop = models.ForeignKey(
        UpcomingWorkshop, on_delete=models.CASCADE, related_name="registrations"
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.workshop.title}"

    class Meta:
        ordering = ["-registered_on"]