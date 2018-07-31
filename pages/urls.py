from django.conf.urls import url
from . import views
from wkhtmltopdf.views import PDFTemplateView
urlpatterns = [
    url(r'dashboard/', views.index, name='dashboard'),
    url(r'chart-creation/', views.chartcreation, name='chart-creation'),
    url(r'data-selection/', views.dataselection, name='data-selection'),
    url(r'create-chartset-redirect/', views.createchartset, name='create-chartset-redirect'),
    url(r'confirm-chart-redirect/', views.confirmchartredirect, name='confirm-chart-redirect'), 
    url(r'delete-chart-redirect/', views.deletechartredirect, name='delete-chart-redirect'),
    url(r'save-chartset-redirect/', views.savechartsetredirect, name='save-chartset-redirect'),
    url(r'change-chartset-redirect/', views.changechartset, name='change-chartset-redirect'),
    url(r'change-selected-chart-redirect/', views.changeselectedchartredirect, name='change-selected-chart-redirect'), 
    url(r'select-dataset-redirect/', views.selectdatasetredirect, name='select-dataset-redirect'),
    url(r'report/', views.reportview, name='report'),
    url(r'db-updater/', views.updatedb, name='db-updater'),
    url(r'db-updater-all-redirect/', views.updatedballredirect, name='db-updater-all-redirect'),
    url(r'db-updater-week-redirect/', views.updatedbweekredirect, name='db-updater-week-redirect'),
]
