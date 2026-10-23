import re

from django import forms
from .models import (
    DemoRequest, ContactMessage, JobApplication,
    CourseBooking, WorkshopRegistration, SatBooking
)

# TN Districts list from RP
TN_DISTRICTS = [
    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore",
    "Dharmapuri", "Dindigul", "Erode", "Kallakurichi", "Kancheepuram",
    "Kanyakumari", "Karur", "Krishnagiri", "Madurai", "Mayiladuthurai",
    "Nagapattinam", "Namakkal", "Perambalur", "Pudukkottai",
    "Ramanathapuram", "Ranipet", "Salem", "Sivagangai", "Tenkasi",
    "Thanjavur", "The Nilgiris", "Theni", "Thiruvallur", "Thiruvarur",
    "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur",
    "Tiruppur", "Tiruvannamalai", "Vellore", "Viluppuram", "Virudhunagar",
]

# Allowed email endings (add more if needed)
ALLOWED_EMAIL_TLDS = (
    ".com", ".in", ".co.in", ".org", ".net", ".edu",
    ".edu.in", ".ac.in", ".org.in", ".net.in", ".gov.in",
    ".info", ".co", ".io", ".me",
)


# =========================================================
# SHARED VALIDATORS (used by SAT, Course Booking, Workshop)
# =========================================================

def validate_person_name(value):
    name = " ".join(value.split())
    if len(name) < 3:
        raise forms.ValidationError("Name must be at least 3 characters.")
    if len(name) > 40:
        raise forms.ValidationError("Name must be 40 characters or less.")
    if not re.fullmatch(r"[A-Za-z .]+", name):
        raise forms.ValidationError("Name can have only letters, spaces and dots.")
    return name


def validate_indian_mobile(value):
    mobile = value.strip().replace(" ", "").replace("-", "")
    if mobile.startswith("+91"):
        mobile = mobile[3:]
    if not re.fullmatch(r"[6-9]\d{9}", mobile):
        raise forms.ValidationError("Enter a valid 10-digit Indian mobile number.")
    return mobile


def validate_email_address(value):
    email = value.strip().lower()

    if not re.fullmatch(r"[a-z0-9._%+-]+@[a-z0-9-]+(\.[a-z0-9-]+)+", email):
        raise forms.ValidationError("Enter a valid email address.")

    if ".." in email or email.startswith(".") or email.split("@")[0].endswith("."):
        raise forms.ValidationError("Enter a valid email address.")

    if not email.endswith(ALLOWED_EMAIL_TLDS):
        raise forms.ValidationError(
            "Please use a valid email ending like .com, .in, .org or .edu."
        )
    return email


# =========================================================
# FORMS
# =========================================================

class DemoForm(forms.ModelForm):
    class Meta:
        model = DemoRequest
        fields = ['name', 'mobile', 'email', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Ravi Kumar',
                'id': 'id_name',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'e.g. +91 98765 43210',
                'id': 'id_phone',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'e.g. your@email.com',
                'id': 'id_email',
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your message here...',
                'id': 'id_message',
            }),
        }


class JobApplicationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Full Name',
            'class': 'form-input',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'form-input',
        })
    )
    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Mobile Number',
            'class': 'form-input',
        })
    )
    highest_qualification = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. B.E Computer Science',
            'class': 'form-input',
        })
    )
    passed_out_year = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 2023',
            'class': 'form-input',
        })
    )
    resume = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-file',
            'accept': '.pdf,.doc,.docx',
        })
    )
    cover_letter = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Write a brief cover letter (optional)...',
            'class': 'form-input',
            'rows': 4,
        })
    )

    class Meta:
        model = JobApplication
        fields = [
            'name', 'email', 'mobile',
            'highest_qualification', 'passed_out_year',
            'resume', 'cover_letter',
        ]


class CourseBookingForm(forms.ModelForm):
    student_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Full Name',
            'class': 'b-input',
            'data-validate': 'name',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'b-input',
            'data-validate': 'email',
        })
    )
    mobile = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': '10-digit mobile number',
            'class': 'b-input',
            'data-validate': 'mobile',
            'inputmode': 'numeric',
        })
    )

    class Meta:
        model = CourseBooking
        fields = ['student_name', 'email', 'mobile']

    def clean_student_name(self):
        return validate_person_name(self.cleaned_data['student_name'])

    def clean_mobile(self):
        return validate_indian_mobile(self.cleaned_data['mobile'])

    def clean_email(self):
        return validate_email_address(self.cleaned_data['email'])


class PaymentSubmissionForm(forms.ModelForm):
    transaction_id = forms.CharField(
        max_length=100,
        label="UPI Transaction ID",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter UPI transaction ID',
            'class': 'b-input',
            'required': True,
        })
    )

    payment_proof = forms.ImageField(
        required=False,
        label="Payment Screenshot (Optional)"
    )

    class Meta:
        model = CourseBooking
        fields = ['transaction_id', 'payment_proof']


class WorkshopRegistrationForm(forms.ModelForm):
    class Meta:
        model = WorkshopRegistration
        fields = ['name', 'email', 'mobile']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'data-validate': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'data-validate': 'email',
            }),
            'mobile': forms.TextInput(attrs={
                'placeholder': '10-digit mobile number',
                'data-validate': 'mobile',
                'inputmode': 'numeric',
            }),
        }

    def clean_name(self):
        return validate_person_name(self.cleaned_data['name'])

    def clean_mobile(self):
        return validate_indian_mobile(self.cleaned_data['mobile'])

    def clean_email(self):
        return validate_email_address(self.cleaned_data['email'])


class SatBookingForm(forms.ModelForm):
    district = forms.ChoiceField(
        choices=[("", "Select District")] + [(d, d) for d in TN_DISTRICTS],
        error_messages={
            "required": "Please select a district.",
            "invalid_choice": "Please select a valid Tamil Nadu district.",
        },
    )

    class Meta:
        model = SatBooking
        fields = [
            'name', 'address', 'gender', 'qualification',
            'district', 'area', 'timing', 'mobile', 'email'
        ]

    def clean_name(self):
        return validate_person_name(self.cleaned_data['name'])

    def clean_mobile(self):
        return validate_indian_mobile(self.cleaned_data['mobile'])

    def clean_email(self):
        return validate_email_address(self.cleaned_data['email'])