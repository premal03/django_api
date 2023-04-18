import io
from .models import Students
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# class based
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin

# concrete view class
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# viewset
from rest_framework import viewsets
# ROUTER


# Basic Auth
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly


class StudentViewSets(viewsets.ViewSet):
    def list(self, request):
        stu = Students.objects.all()
        serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)

    def create(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        id = pk
        stu = Students.objects.get(id=id)
        serializer = StudentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        id = pk
        stu = Students.objects.get(id=id)
        serializer = StudentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        id = pk
        stu = Students.objects.get(id=id)
        stu.delete()
        return Response({'success': True}, status=status.HTTP_201_CREATED)


# viewsets.ReadOnlyModelViewSet: It gives two methods list and retrieve

# customer Permission
from api_demo.custompermission import MyPermission


class StudentModelViewSets(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    # To give this globally we can add this in settings.py file
    authentication_classes = [TokenAuthentication]
    # TOKEN AUTH: There are multiple methods to generate token but before that add rest_framework.auth in installed_app
    # then, python manage.py migrate
    #   1. Admin Panel: You will find one token table there you can create API KEY for particular user
    #   2. CMD: python manage.py drf_create_token <username>
    #   3. DRF also provide in built view function which returns token when
    #   we pass username and password(obtain_auth_token)
    #   4. Using Signals: When we create user at that time only it generate token
    # authentication_classes = [SessionAuthentication]
    # authentication_classes = [BasicAuthentication]
    # permission_classes: IsAuthenticated, AllowAny, IsAdminUser
    # permission_classes = [MyPermission]
    permission_classes = [IsAuthenticated]
    # permission_classes = [DjangoModelPermissions]



class StudentConcreteList(ListCreateAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer


class StudentConcreteRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer


# Generic API View and Mixins
class StudentGenericList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# retrieve update and destroy - PK required
class StudentRetrieveUpdate(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class StudentAPI(APIView):
    def get(self, request, pk=None, format=None):
        id = pk
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu)
            return Response(serializer.data)
        stu = Students.objects.all()
        serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'data created'}, status=status.HTTP_201_CREATED)
        return Response(
            {
                'message': 'Invalid request',
                'error': serializer.errors
            },
            status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == "GET":
        return Response({'message': 'Hello world!!'})
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Data created'})

        return Response({'data': serializer.errors})
    elif request.method == "PUT":
        id = request.data.get('id')
        stu = Students.objects.get(pk=id)
        serializer = StudentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Data updated'})
        return Response({'data': serializer.errors})


@method_decorator(csrf_exempt, name='dispatch')
class Student(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        model_data = JSONParser().parse(stream)
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Students.objects.all()
        print(stu)
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        model_data = JSONParser().parse(stream)
        serializer = StudentSerializer(data=model_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'student created'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        model_data = JSONParser().parse(stream)
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu, data=model_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': f'student name: {stu.name} updated'
                }
                json_data = JSONRenderer().render(response)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        model_data = JSONParser().parse(stream)
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            stu.delete()
            response = {
                'message': f'student deleted'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')


def student_details(request, id):
    stu = Students.objects.get(id=id)
    print(stu)
    serializer = StudentSerializer(stu)
    # json_data = JSONRenderer().render(serializer.data)
    # return HttpResponse(json_data, content_type='application/json')
    return JsonResponse(serializer.data)


@csrf_exempt
def student_list(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    model_data = JSONParser().parse(stream)
    if request.method == 'POST':
        serializer = StudentSerializer(data=model_data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'student created'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')
    elif request.method == 'GET':
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type='application/json')
        stu = Students.objects.all()
        print(stu)
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'PUT':
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            serializer = StudentSerializer(stu, data=model_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    'message': f'student name: {stu.name} updated'
                }
                json_data = JSONRenderer().render(response)
                return HttpResponse(json_data, content_type='application/json')
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(json_data, content_type='application/json')

    elif request.method == 'DELETE':
        id = model_data.get('id', None)
        if id is not None:
            stu = Students.objects.get(id=id)
            stu.delete()
            response = {
                'message': f'student deleted'
            }
            json_data = JSONRenderer().render(response)
            return HttpResponse(json_data, content_type='application/json')
