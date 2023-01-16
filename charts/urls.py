from django.urls import path
from . import views

app_name = 'charts'

urlpatterns = [
   path('<pk>/', views.dashboard, name='dashboard'),
   path('upload/<pk>', views.upload_view, name='upload'),
   path('htmx/create-chart/<pk>/<pk2>/', views.create_chart, name='create-chart'),  
   path('htmx/new-chart/<pk>', views.new_chart, name='new-chart'),
   path('htmx/update-title/<pk>', views.update_title, name='update-title'),
   path('htmx/pivot-table/<pk>', views.pivot_table, name='pivot-table'),
   path('htmx/dataframe/<pk>', views.show_dataframe, name='dataframe'),
   path('htmx/row-delete/<pk>', views.row_deleter, name='row-delete'),
   path('htmx/show-update/<pk>', views.show_update, name='show-update'),
   path('htmx/remover/', views.remover, name='remover')
]

