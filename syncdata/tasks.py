from celery import shared_task
from syncdata.utils import get_response
from syncdata.models import SyncedFile


@shared_task
def sync_files_from_crm(syncdata_ids):
    metadata = []
    try:
        for syncdata in syncdata_ids:
            deal_id = syncdata.get('deal_id', '')
            deal_url = f"/crm/v3/objects/deals/{deal_id}"
            deal_resp = get_response(deal_url).json()
            files = syncdata.get('files', [])
            for file_id in files:
                url = f"/files/v3/files/{file_id}"
                response = get_response(url)
                responseJson = response.json()
                syncDataObjects = SyncedFile(
                    name=deal_resp.get("properties", {}).get("dealname", ""),
                    size=responseJson.get("size", 0),
                    file_type=responseJson.get("extension", ""),
                    deal_id=deal_id,
                    crm_source="hubspot",
                    file_id=file_id,
                    file_name=responseJson.get("name", ""),
                    properties=deal_resp.get("properties", {}),
                    file_url=responseJson.get("url", "")
                )
                # attachments.append(response.json())
                metadata.append(syncDataObjects)
    except Exception as e:
        print(f"Error syncing files: {e}")
        return
    SyncedFile.objects.bulk_create(metadata, ignore_conflicts=True)
    print("Synced files from CRM")