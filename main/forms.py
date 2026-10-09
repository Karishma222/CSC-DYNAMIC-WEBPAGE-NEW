from django import forms
from .models import DemoRequest, ContactMessage, SatBooking


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

class DemoForm(forms.ModelForm):
    class Meta:
        model = DemoRequest
        fields = ['name','mobile','email','description']
        widgets = {
        'description': forms.Textarea(attrs={'rows':3}),
        }


# class ContactForm(forms.ModelForm):
#     class Meta:
#         model = ContactMessage
#         fields = ['name','email','message']
#         widgets = {
#         'message': forms.Textarea(attrs={'rows':4}),
#         }


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
        
        
# ── Add to your existing forms.py ─────────────────────────────────────────

from django import forms
from .models import JobApplication


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
        model  = JobApplication
        fields = [
            'name', 'email', 'mobile',
            'highest_qualification', 'passed_out_year',
            'resume', 'cover_letter',
        ]
        
        
# ── Add to your existing forms.py ────────────────────────────────────────

from django import forms
from .models import CourseBooking


class CourseBookingForm(forms.ModelForm):
    student_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Full Name',
            'class': 'b-input',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'b-input',
        })
    )
    mobile = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': '+91 XXXXX XXXXX',
            'class': 'b-input',
        })
    )

    class Meta:
        model  = CourseBooking
        fields = ['student_name', 'email', 'mobile']


class SatBookingForm(forms.ModelForm):
    district = forms.ChoiceField(
        choices=[("", "Select District")] + [(d, d) for d in TN_DISTRICTS],
        error_messages={
            "required": "Please select a district.",
            "invalid_choice": "Please select a valid Tamil Nadu district.",
        },
    )
    class Meta:
        model  = SatBooking
        fields = ['name', 'address', 'gender', 'qualification',
                  'district', 'area', 'timing', 'mobile', 'email']
                  
