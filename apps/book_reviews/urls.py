from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_reviews),
    url(r'^add_review/(?P<book_id>\d+)$', views.add_review),
    url(r'^user/(?P<user_id>\d+)$', views.user),
    url(r'^new_review$', views.new_review),
    url(r'^create_review$', views.create_review),


]
