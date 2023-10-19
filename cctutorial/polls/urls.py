from django.urls import path, re_path

from polls import views

urlpatterns = [
    path('', views.index, name='index'),
    path('most-popular/', views.most_popular_choice, name='most-popular-choice'),
    re_path(r'choices/(?P<pk>\d+)/', views.choices, name='choices'),
    path('choices/', views.choices, name='choices'),
    re_path('question/(?P<pub_date>[0-9]{4}[-/][0-9]{2}[-/][0-9]{2})/', views.question, name='question'),
    re_path('question/', views.question, name='question'),
]
