
from django.contrib import admin
from django.urls import path, include
from api_demo import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('studentviewset', views.StudentViewSets, basename='studentviewset')
router.register('studentmodelviewset', views.StudentModelViewSets, basename='studentmodelviewset')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('students/<int:id>', views.student_details),
    path('students/', views.student_list),
    path('studentgenericlist/', views.StudentGenericList.as_view()),
    path('studentgenericlist/<int:pk>', views.StudentRetrieveUpdate.as_view()),
    path('studentconcreteretrieveupdatedestroy/<int:pk>', views.StudentConcreteRetrieveUpdateDestroy.as_view()),
    path('studentconcretelist', views.StudentConcreteList.as_view()),
    path('helloworld/', views.hello_world),
    path('studviewset', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]

