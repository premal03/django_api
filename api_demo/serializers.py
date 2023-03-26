from rest_framework import serializers
from .models import Students


def start_with_r(value):
    if value[0].lower() == 'r':
        raise serializers.ValidationError('Name should not start from R')
    return value


class StudentSerializer(serializers.Serializer):

    # id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, validators=[start_with_r])
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
    #field level validation
    def validate_rollno(self, value):
        if value >= 200:
            raise serializers.ValidationError('Seat full')
        return value
    #0bject level validation
    def validate(self, data):
        nm = data.get('name')
        ct = data.get('city')
        if nm.lower() == 'premal' and ct.lower() == "ahmedabad":
            raise serializers.ValidationError('He is admin')
        return data
