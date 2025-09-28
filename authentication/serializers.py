from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, attrs):
        logger.info(f"UserRegistrationSerializer.validate called with attrs: {attrs}")
        
        try:
            # Check if required fields are present
            if 'password' not in attrs:
                logger.error("Password field missing from validation data")
                raise serializers.ValidationError("Password is required")
            
            if 'password_confirm' not in attrs:
                logger.error("Password confirmation field missing from validation data")
                raise serializers.ValidationError("Password confirmation is required")
            
            if 'username' not in attrs:
                logger.error("Username field missing from validation data")
                raise serializers.ValidationError("Username is required")
            
            # Check password match
            if attrs['password'] != attrs['password_confirm']:
                logger.error("Password confirmation does not match password")
                raise serializers.ValidationError("Passwords don't match")
            
            # Check if username already exists
            username = attrs.get('username')
            if User.objects.filter(username=username).exists():
                logger.error(f"Username '{username}' already exists")
                raise serializers.ValidationError("Username already exists")
            
            logger.info("UserRegistrationSerializer validation successful")
            return attrs
            
        except serializers.ValidationError as e:
            logger.error(f"Validation error in UserRegistrationSerializer: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in UserRegistrationSerializer.validate: {str(e)}")
            raise serializers.ValidationError(f"Validation error: {str(e)}")

    def create(self, validated_data):
        logger.info(f"UserRegistrationSerializer.create called with validated_data: {validated_data}")
        
        try:
            # Remove password_confirm before creating user
            validated_data.pop('password_confirm', None)
            logger.info(f"Creating user with data: {validated_data}")
            
            user = User.objects.create_user(**validated_data)
            logger.info(f"User created successfully: {user.username} (ID: {user.id})")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user in UserRegistrationSerializer: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            raise serializers.ValidationError(f"Error creating user: {str(e)}")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')

        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active')
        read_only_fields = ('id', 'date_joined', 'is_active')
