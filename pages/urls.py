from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'dashboard/', views.index, name='dashboard'),
    url(r'chart-creation/', views.chartcreation, name='chart-creation'),
    url(r'data-selection/', views.dataselection, name='data-selection'),
    url(r'create-chartset-redirect/', views.createchartset, name='create-chartset-redirect'),
    url(r'confirm-chart-redirect/', views.confirmchartredirect, name='confirm-chart-redirect'), 
    url(r'delete-chart-redirect/', views.deletechartredirect, name='delete-chart-redirect'),
    url(r'save-chartset-redirect/', views.savechartset, name='save-chartset-redirect'),
    url(r'change-chartset-redirect/', views.changechartset, name='change-chartset-redirect'),
    url(r'change-selected-chart-redirect/', views.changeselectedchartredirect, name='change-selected-chart-redirect'),
    # url(r'edit-chart/', views.editchart, name='edit-chart'),
    url(r'edit-dataset/', views.editdataset, name='edit-dataset'), 
    url(r'select-dataset-redirect', views.selectdatasetredirect, name='select-dataset-redirect'),
]
