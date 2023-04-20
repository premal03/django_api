from rest_framework import serializers
from .models import Students, Singer, Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'singer', 'duration']


class SingerSerializer(serializers.ModelSerializer):
    # song = serializers.StringRelatedField(many=True, read_only=True)
    # song = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # song = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='songviewset-detail')
    # song = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # song = serializers.HyperlinkedIdentityField(view_name='songviewset-detail')
    song = SongSerializer(many=True, read_only=True)
    class Meta:
        model = Singer
        fields = ['id', 'name', 'gender', 'song']


def start_with_r(value):
    if value[0].lower() == 'r':
        raise serializers.ValidationError('Name should not start from R')
    return value


class StudentHyperLinkedSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='studentmodelhyperlink-detail')
    class Meta:
        model = Students
        fields = ['name', 'rollno', 'city', 'url']


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = ['name', 'rollno', 'city']
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


#
# class StudentSerializer(serializers.Serializer):
#
#     # id = serializers.IntegerField()
#     name = serializers.CharField(max_length=100, validators=[start_with_r])
#     rollno = serializers.IntegerField()
#     city = serializers.CharField(max_length=100)
#
#     def create(self, validated_data):
#         return Students.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#
#         #partial data update
#         instance.name = validated_data.get('name', instance.name)
#         instance.rollno = validated_data.get('rollno', instance.rollno)
#         instance.city = validated_data.get('city', instance.city)
#         instance.save()
#         return instance
#     #field level validation
#     def validate_rollno(self, value):
#         if value >= 200:
#             raise serializers.ValidationError('Seat full')
#         return value
#     #0bject level validation
#     def validate(self, data):
#         nm = data.get('name')
#         ct = data.get('city')
#         if nm.lower() == 'premal' and ct.lower() == "ahmedabad":
#             raise serializers.ValidationError('He is admin')
#         return data
