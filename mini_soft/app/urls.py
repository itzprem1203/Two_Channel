from django.conf import settings
from django.urls import path,include
from django.conf.urls.static import static
from .views import measurement,master,parameter,measurenew_data,spc,backup,changed_name,shutdown,report_xlsx,report_pdf,report,measurement_count,comport,login,data,delete_measure_data


urlpatterns = [
    path('',login,name="login"),
    path('measurement/',measurement,name="measurement"),
    path('master/',master,name="master"),
    path('parameter/',parameter,name="parameter"),
    path('report/',report,name="report"),
    path('comport/',comport,name="comport"),
    path('data/',data,name="data"),
    path('delete_measure_data/',delete_measure_data,name="delete_measure_data"),
    path('measurement_count/',measurement_count,name="measurement_count"),
    path('report_xlsx/',report_xlsx,name="report_xlsx"),
    path('report_pdf/',report_pdf,name="report_pdf"),
    path('spc/',spc,name="spc"),
    path('shutdown/',shutdown,name="shutdown"),
    path('changed_name/',changed_name,name="changed_name"),
    path('backup/',backup,name="backup"),
    path('measurenew_data/',measurenew_data,name="measurenew_data")
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)