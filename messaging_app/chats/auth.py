from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # override the default field(username)
    username_field = "email"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Replace username field with 'email' in field definitions
        self.fields["email"] = serializers.EmailField()
        self.fields["password"] = serializers.CharField(write_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        data["user_id"] = str(self.user.user_id)
        data["email"] = self.user.email
        data["username"] = self.user.username  # optional
        data["role"] = self.user.role  # optional

        return data
