import email
from lib2to3.pgen2 import driver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import Trip, User


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    group = serializers.CharField()
    

    # validation_data
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    # create_user
    def create(self, validated_data):
        group_data = validated_data.pop('group')
        group, _ = Group.objects.get_or_create(name=group_data)
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        user = self.Meta.model.objects.create_user(**data)
        user.groups.add(group)
        user.save()
        return user


    class Meta:
        model = get_user_model()
        fields = (
            'id', 'username', 'password1', 'password2',
            'email', 'first_name', 'last_name', 'group',
            'photo',
        )
        
        read_only_fields = ('id',)


class LogInSerializer(TokenObtainPairSerializer):
    #display token and username and email
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['group'] = self.user.group
        data['id'] = self.user.id
        return data






class TripSerializer(serializers.ModelSerializer):


    class Meta:
        model = Trip
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'price', 'driver', 'passenger')

    #print trip
    



class NestedTripSerializer(serializers.ModelSerializer):
    driver = UserSerializer(read_only=True)
    passenger = UserSerializer(read_only=True)
    

    class Meta:
        model = Trip
        fields = '__all__'
        depth = 1

    #display passenger username and passenger email
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['passenger']:
            representation['passenger'] = {
            'id': instance.passenger.id,
            'username': instance.passenger.username,
            'email': instance.passenger.email,
            'first_name': instance.passenger.first_name,
            'last_name': instance.passenger.last_name,
        }
        elif representation['driver']:
            representation['driver'] = {
            'id': instance.driver.id,
            'username': instance.driver.username,
            'email': instance.driver.email,
            'first_name': instance.driver.first_name,
            'last_name': instance.driver.last_name,
        }
        else:
            representation
        
        return representation
        


    #filiter passenger and driver field


    

    

    

# class TripPassengerSerializer(serializers.ModelSerializer):
#     passenger = UserSerializer(read_only=True)

#     class Meta:
#         model = Trip
#         fields = '__all__'
#         depth = 1

    










