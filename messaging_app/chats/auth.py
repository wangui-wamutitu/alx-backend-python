from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# frontend will not need to decode the JWT to get the user info — it’s right there, username and email or anything else that will be necessary
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        data["email"] = self.user.email
        return data
