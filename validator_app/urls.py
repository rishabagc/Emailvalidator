from django.contrib import admin
from django.conf.urls import url
from validator_app import views

urlpatterns = [
    url(r'^$', views.DashBoardView.as_view(), name='home_page'),
    url(r'^dashboard/single_validator/$', views.SinglemailValidator.as_view(), name='single_mail_validator'),
    url(r'^dashboard/bulk_validator/$', views.BulkmailValidator.as_view(), name='bulk_mail_validator'),
    url(r'^dashboard/download_csv/$', views.DownloadCSV.as_view(), name='download_sample_csv'),
]