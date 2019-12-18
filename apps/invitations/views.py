from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.invitations.models import Invitation
from apps.invitations.serializers import InvitationSerializer


class InvitationView(APIView):
    """
    List all invitations, or create a new invitation.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        invitations = request.user.created_invitations.all()
        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data['creator'] = request.user.pk
        serializer = InvitationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            from_email = request.user.email
            to_email = request.data.get('email')
            # Send notification from_email to to_email using
            # any of SMS tools like Mailchimp, Sandgrid, etc..
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvitationDetail(APIView):
    """
    Patch or delete an invitation instance.
    """

    def get_object(self, id):
        try:
            return Invitation.objects.get(pk=id)
        except Invitation.DoesNotExist:
            raise Http404

    def patch(self, request, id):
        invitation = self.get_object(id)
        # set partial=True to update a data partially
        serializer = InvitationSerializer(
            invitation, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            if invitation.email and invitation.email != request.data.get('email'):
                from_email = request.user.email
                to_email = request.data.get('email')
                # Send notification from_email to to_email using
                # any of SMS tools like Mailchimp, Sandgrid, etc..
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        invitation = self.get_object(id)
        invitation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
