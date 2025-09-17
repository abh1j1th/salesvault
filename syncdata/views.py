
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from syncdata.serializers import SyncedFileSerializer
from syncdata.tasks import sync_files_from_crm
from .models import SyncedFile
from .hubspot_service import HubSpotService
from salesvault import settings
from syncdata.filters import CustomeFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            if not username or not password:
                return Response({'status': 0, 'error': 'Please provide a username and password.'}, status=status.HTTP_400_BAD_REQUEST)

            # Do not lowercase username, Django is case-sensitive for superusers
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'status': 1,
                }, status=status.HTTP_200_OK)
            else:
                if not User.objects.filter(username__iexact=username).exists():
                    return Response({'reset': 0, 'username_error': 1, 'error': 'Email/Username you have entered is incorrect.'}, status=status.HTTP_409_CONFLICT)
                return Response({'reset': 0, 'username_error': 0, 'error': 'Password you have entered is incorrect.'}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print('ERROR', str(e))
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListCRMFiles(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        crm = HubSpotService()
        try:
            files = crm.get_deal_attachments()
            return Response(files)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SyncFilesFromCRM(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        syncdata_ids = request.data.get('syncdata_ids', [])
        sync_files_from_crm.delay(syncdata_ids)
        return Response({'data': "File sync initiated"}, status=status.HTTP_200_OK)


class SyncedFilesList(ListAPIView):
	permission_classes = [IsAuthenticated]
	queryset = SyncedFile.objects.all()
	serializer_class = SyncedFileSerializer
	filter_backends = [CustomeFilterBackend]