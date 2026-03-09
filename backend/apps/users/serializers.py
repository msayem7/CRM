from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Business


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class BusinessSerializer(serializers.ModelSerializer):
    """Serializer for Business model"""
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Business
        fields = ['id', 'owner', 'name', 'description', 'email', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at']


class SignupSerializer(serializers.Serializer):
    """Serializer for user registration with improved error handling"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(max_length=30, required=False, default='')
    last_name = serializers.CharField(max_length=150, required=False, default='')
    business_name = serializers.CharField(max_length=255, required=False, default='')

    def validate_email(self, value):
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        
        # Validate password strength
        try:
            validate_password(attrs['password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        business_name = validated_data.pop('business_name', None)
        
        # Generate username from email (part before @)
        base_username = validated_data['email'].split('@')[0].lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )

        # Create business
        if business_name:
            business_name = business_name
        else:
            business_name = f"{user.username}'s Business"
        
        business = Business.objects.create(
            owner=user,
            name=business_name,
            email=user.email,
        )

        return {'user': user, 'business': business}


class LoginSerializer(serializers.Serializer):
    """Serializer for user login with improved error handling"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email', '').lower().strip()
        password = attrs.get('password', '')
        
        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
            attrs['user'] = user
        except User.DoesNotExist:
            pass
        
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, min_length=8, required=True)
    new_password_confirm = serializers.CharField(write_only=True, min_length=8, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Passwords do not match."})
        
        # Validate password strength
        try:
            validate_password(attrs['new_password'])
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        
        return attrs
