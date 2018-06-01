from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'dashboard/', views.index, name='dashboard'),
    url(r'chart-creation/', views.chartcreation, name='chart-creation'),
    url(r'data-selection/', views.dataselection, name='data-selection'),
    url(r'redirect/', views.create_chartset_index, name='redirect')
]
