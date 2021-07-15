from django.contrib.auth import get_user_model, password_validation as password_validator
from django.core import exceptions
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def validate(self, data):
        UserModel = self.Meta.model
        password = data["password"]

        user = UserModel(**data)
        errors = dict()

        try:
            password_validator.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = e.messages
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        UserModel = self.Meta.model
        user = UserModel.objects.create(**validated_data)
        return user
