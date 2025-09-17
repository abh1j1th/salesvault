from django.urls import path
from syncdata.views import (
    ListCRMFiles,
    SyncFilesFromCRM,
    SyncedFilesList,
    UserLoginView
)

urlpatterns = [
    path('api/v1/auth/login/', UserLoginView.as_view()),
    path('api/v1/crm/deals_files/', ListCRMFiles.as_view()),
    path('api/v1/crm/sync-files/', SyncFilesFromCRM.as_view()),
    path('api/v1/crm/synced-files/', SyncedFilesList.as_view()),
]
