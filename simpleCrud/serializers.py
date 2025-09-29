# serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token payload
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['user_id'] = user.id        
        # If you have custom profile/vendor profile
        if hasattr(user, 'profile'):
            token['user_type'] = user.profile.user_type
        
        if hasattr(user, 'vendor_profile'):
            token['store_name'] = user.vendor_profile.store_name
            token['is_approved'] = user.vendor_profile.is_approved

        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra response data (not in token, just in response)
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['user_id'] = self.user.id
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer