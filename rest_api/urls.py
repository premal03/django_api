
from django.contrib import admin
from django.urls import path, include
from api_demo import views
from rest_framework.routers import DefaultRouter
from api_demo.auth import CustomAuthToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

router = DefaultRouter()

router.register('studentviewset', views.StudentViewSets, basename='studentviewset')
router.register('studentmodelviewset', views.StudentModelViewSets, basename='studentmodelviewset')
router.register('studentmodelhyperlink', views.StudentHyperlinkedViewSet, basename='studentmodelhyperlink')
router.register('singers', views.SingerViewSet, basename='singerviewset')
router.register('songs', views.SongViewSet, basename='songviewset')

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
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('generatetoken/', CustomAuthToken.as_view()),
    #JWT
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
]
#http POST http://127.0.0.1:3000/generatetoken/ username="admin" password="admin"
#http POST http://127.0.0.1:3000/gettoken/ username="admin" password="admin"
#http POST http://127.0.0.1:3000/verifytoken/ token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxNzk4NzcyLCJpYXQiOjE2ODE3OTg0NzIsImp0aSI6ImMxNGIxMTFlZWUyODQ3ZjQ4NmU0M2UwMmQxYjIxYTYwIiwidXNlcl9pZCI6MX0.ssA6lLbF3mPVDG2H-vNdF9lLD4S9reuBGzHqJ3lvwa4"
#http POST http://127.0.0.1:3000/refreshtoken/ refresh="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTg4NDg3MiwiaWF0IjoxNjgxNzk4NDcyLCJqdGkiOiIwMGFiOTcyOTk1ZWE0YWI1YTJlOTIyYjg2ZGI1MTU4NyIsInVzZXJfaWQiOjF9.OV2g9hozrRKPFXObMOxaMfLEFQnBg2DBjnGDRXCykEY"
