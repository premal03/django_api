import io

from django.shortcuts import render
from .models import Students
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
#class based
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# Create your views here.


#Generic API View and Mixins
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

    def put(self, request, *args, ** kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, ** kwargs):
        return self.destroy(request, *args, **kwargs)

class StudentAPI(APIView):
    def get(self, request, pk=None, format=None):
        id=pk
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




