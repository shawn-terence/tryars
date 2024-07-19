from rest_framework import serializers
from .models import User,Asset,Request


#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['first_name','last_name', 'phone_number', 'department', 'role','password','email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
#asset serializer
class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['name','description','category','serial_number','tag','status','asset_type' ]
    def create(self,validated_data):
        asset = Asset.objects.create(**validated_data)
        return asset
#request serializer
class RequestSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()
    employee = UserSerializer()
    class Meta:
        model = Request
        fields = ['id', 'asset', 'employee', 'status']
    def create(self,validated_data):
        request = Request.objects.create(**validated_data)
        return request