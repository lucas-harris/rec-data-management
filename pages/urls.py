from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'dashboard/', views.index, name='dashboard'),
    url(r'chart-creation/', views.chartcreation, name='chart-creation'),
    url(r'data-selection/', views.dataselection, name='data-selection'),
    url(r'create-chartset-redirect/', views.createchartset, name='create-chartset-redirect'),
    url(r'delete-chart-redirect/', views.deletechart, name='delete-chart-redirect'),
    url(r'save-chartset-redirect/', views.savechartset, name='save-chartset-redirect'),
    url(r'change-chartset-redirect/', views.changechartset, name='change-chartset-redirect'),
    # url(r'delete-chartset-redirect/', views.deletechartset, name='delete-chartset-redirect'),
]
