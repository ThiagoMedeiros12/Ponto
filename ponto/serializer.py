from rest_framework import serializers
from django.contrib.auth.models import User
from . models import Profile



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =['cargo','datetime']



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    

    class Meta:
        model = User
        fields = ['id', 'username', 'password','email','profile']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        Profile.objects.create(
            user=user,
            cargo=profile_data('cargo')
        )
        return user
    