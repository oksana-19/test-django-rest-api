
from django.utils import timezone
from rest_framework import serializers
from apps.invitations.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    createdTime = serializers.DateTimeField(
        source='created_time', default=timezone.now)
    seconds = serializers.SerializerMethodField()
    creatorEmail = serializers.SerializerMethodField()
    creatorFullname = serializers.SerializerMethodField()

    class Meta:
        model = Invitation
        fields = ('id', 'createdTime', 'seconds', 'email',
                  'used', 'creatorEmail', 'creatorFullname', 'creator')

    def get_seconds(self, obj):
        """
        Obtain interval time between now and created_time in seconds.
        """
        current_datetime = timezone.now()
        created_datetime = obj.created_time
        return int((current_datetime - created_datetime).total_seconds())

    def get_creatorFullname(self, obj):
        """
        Return current user full name.
        """
        return obj.creator.get_full_name()

    def get_creatorEmail(self, obj):
        """
        Return current user email address.
        """
        return obj.creator.email

    def to_representation(self, obj):
        """
        Remove creator field before returning result in data property.
        """
        ret = super(InvitationSerializer, self).to_representation(obj)
        ret.pop('creator')
        return ret
