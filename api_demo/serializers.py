from rest_framework import serializers
from .models import Students


class StudentSerializer(serializers.Serializer):
    # id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    rollno = serializers.IntegerField()
    city = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Students.objects.create(**validated_data)

    def update(self, instance, validated_data):

        #partial data update
        instance.name = validated_data.get('name', instance.name)
        instance.rollno = validated_data.get('rollno', instance.rollno)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        return instance

