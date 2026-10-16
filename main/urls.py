from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Common / General Pages ──────────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('placement/', views.placement, name='placement'),  
    path('inspiration/', views.inspiration, name='inspiration'),
    path('registration/', views.registration, name='registration'), # Reporting Person (RP) path

    # ── Workshops (Both singular & plural included so no links break) ──
    path('workshop/', views.workshop_view, name='workshop'),          # Mine
    path('workshops/', views.workshop_view, name='workshops'),        # RP path (plural)
    path('workshop/<int:pk>/', views.workshop_detail, name='workshop_detail'),       # Mine
    path('workshop/<int:pk>/register/', views.workshop_register, name='workshop_register'), # Mine

    # ── Careers ─────────────────────────────────────────────
    path('careers/', views.career_list, name='career'),
    path('careers/apply/<int:career_id>/', views.apply_job, name='apply_job'),

    # ── Courses (All booking, payment, detail, and success views) ──
    path('courses/', views.courses_page, name='courses'),
    path('courses/details/<int:course_id>/', views.course_detail, name='course_detail'), # Mine
    path('courses/book/<int:course_id>/', views.book_course, name='book_course'),
    path('courses/payment/<int:booking_id>/', views.course_payment, name='course_payment'), # Mine
    path('courses/success/<int:booking_id>/', views.booking_success, name='booking_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)