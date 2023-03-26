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
# Create your views here.


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




