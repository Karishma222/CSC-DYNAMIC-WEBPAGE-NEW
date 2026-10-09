from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('workshops/', views.workshop_view, name='workshop'),  
    path('reviews/', views.reviews_view, name='reviews'),
     path('careers/',           views.career_list, name='career'),
    path('careers/apply/<int:career_id>/', views.apply_job,   name='apply_job'),
    path('courses/',                          views.courses_page,    name='courses'),
    path('courses/book/<int:course_id>/',     views.book_course,     name='book_course'),
    path('courses/success/<int:booking_id>/', views.booking_success, name='booking_success'),
    path('placement/', views.placement, name='placement'),  
    path('registration/', views.registration, name='registration'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
