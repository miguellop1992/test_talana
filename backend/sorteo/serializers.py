import datetime

from rest_framework import serializers

from backend.sorteo.models import User, Lottery
from backend.sorteo.tasks import user_verify


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    date_verify = serializers.DateTimeField(read_only=True)
    link_password = serializers.CharField(read_only=True)

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()
        if user:
            msg = f"Error, el correo {value} ya se encuenta registrado"
            if not user.date_verify:
                msg = f"""El correo {value} ya se encuenta registrado, debe ser verificado se le enviara un correo para 
                la verificación"""
                user_verify.delay(value, self.context['request'].build_absolute_uri('/')[:-1])
                # user_verify(value, self.context['request'].build_absolute_uri('/')[:-1])
            raise serializers.ValidationError(msg)
        return value

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        request = self.context['request']
        localhost = request.build_absolute_uri('/')[:-1]
        user_verify.delay(user.email, localhost)
        # user_verify(user.email, localhost)
        user.link_password = user.get_link()
        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_verify', 'created_at', 'updated_at', 'link_password')


class VerifyUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmed = serializers.CharField(write_only=True)

    def validate_password_confirmed(self, value):
        if self.initial_data['password'] != value:
            raise serializers.ValidationError("Contraseña no coinciden")
        return value

    def update(self, instance: User, validated_data):
        password = validated_data['password']
        instance.set_password(password)
        instance.date_verify = datetime.datetime.today()
        instance.save(update_fields=['password', 'date_verify'])
        return instance

    class Meta:
        model = User
        fields = ('password', 'password_confirmed')


class LotterySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Lottery
        fields = ('user', 'created_at')
