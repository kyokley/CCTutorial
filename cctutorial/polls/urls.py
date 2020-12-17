from django.urls import path

from polls import views

urlpatterns = [
    path('', views.index, name='index'),
    path('most-popular/', views.most_popular_choice, name='most-popular-choice'),
    path('choices/(?P<pk>[0-9]{4})/', views.choices, name='choices'),
    path('choices/', views.choices, name='choices'),
    path('question/(?P<pub_date>[0-9]{4}[-/][0-9]{2}[-/][0-9]{2})/', views.question, name='question'),
]
