from django.contrib import admin

# Register your models here.

from .models import DemoRequest, Review, Achievement, Workshop, ContactMessage,Course,SatBooking


admin.site.register(DemoRequest)
admin.site.register(Review)
admin.site.register(Achievement)
admin.site.register(Workshop)
admin.site.register(ContactMessage)
admin.site.register(Course)


# ── Add to your admin.py ──────────────────────────────────────────────────

from django.contrib import admin
from .models import Career, JobApplication


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display  = ['role', 'employment_type', 'location', 'salary', 'is_active', 'posted_on']
    list_filter   = ['employment_type', 'is_active']
    search_fields = ['role', 'job_description']
    list_editable = ['is_active']
    ordering      = ['-posted_on']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'mobile', 'career', 'highest_qualification', 'passed_out_year', 'applied_on']
    list_filter   = ['career']
    search_fields = ['name', 'email', 'mobile']
    readonly_fields = ['applied_on']
    ordering      = ['-applied_on']
    
# ── Add to your existing admin.py ────────────────────────────────────────

from django.contrib import admin
from .models import BookCourse, CourseBooking


@admin.register(BookCourse)
class BookCourseAdmin(admin.ModelAdmin):
    list_display  = ['name', 'duration', 'original_fee', 'offer_fee', 'discount_percent', 'is_active']
    list_editable = ['is_active']
    list_filter   = ['is_active']
    search_fields = ['name']

    def discount_percent(self, obj):
        return f"{obj.discount_percent()}% OFF"
    discount_percent.short_description = 'Discount'


@admin.register(CourseBooking)
class CourseBookingAdmin(admin.ModelAdmin):
    list_display  = ['booking_ref', 'student_name', 'email', 'mobile', 'course', 'booked_on']
    list_filter   = ['course']
    search_fields = ['student_name', 'email', 'mobile', 'booking_ref']
    readonly_fields = ['booking_ref', 'booked_on']
    ordering      = ['-booked_on']


@admin.register(SatBooking)
class SatBookingAdmin(admin.ModelAdmin):
    list_display    = ['name', 'mobile', 'email', 'qualification', 'district', 'area', 'timing', 'gender', 'created_at']
    list_filter     = ['timing', 'gender', 'qualification', 'district']
    search_fields   = ['name', 'mobile', 'email', 'area']
    readonly_fields = ['created_at']
    ordering        = ['-created_at']

