from django.contrib import admin
from django.urls import path
from analysis.views import analyze_query

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/analyze/', analyze_query, name='analyze'),
]
