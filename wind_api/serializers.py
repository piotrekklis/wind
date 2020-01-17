from django.contrib.auth.models import User, Group
from wind_api.models import Observation
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class ObservationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Observation
        fields = ('observation_time', 'country_code', 'city_name', 'latitude', 'longitude', 'wind_speed', 'wind_direction_short', 'wind_direction_full', 'wind_direction_degrees')
