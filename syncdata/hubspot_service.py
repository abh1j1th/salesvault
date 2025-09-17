import requests
from salesvault import settings
from syncdata.utils import get_response


class HubSpotService:
    def __init__(self):
        self.access_token = settings.API_KEY

    def get_deal_attachments(self):
        url = "/crm/v3/objects/deals"
        response = get_response(url)
        response.raise_for_status()
        deals = response.json().get('results', [])
        for deal in deals:
            attachments = []
            deal_id = deal['id']
            note_url = f"/crm/v3/objects/deals/{deal_id}/associations/notes"
            note_resp = get_response(note_url)
            if note_resp.status_code != 200:
                continue
            results = note_resp.json().get('results', [])
            for result in results:
                note_id = result['id']
                att_url = f"/crm/v3/objects/notes/{note_id}?properties=hs_attachment_ids"
                att_resp = get_response(att_url)
                if att_resp.status_code != 200:
                    continue
                hs_attachment_ids = att_resp.json().get('properties', {}).get('hs_attachment_ids', '')
                if not hs_attachment_ids:
                    continue
                file_url = f"/files/v3/files/{hs_attachment_ids}"
                file_resp = get_response(file_url)
                if file_resp.status_code != 200:
                    continue
                file_response = file_resp.json()
                attachments.append(file_response)
            deal['attachments'] = attachments
            
        return deals

    def get_file_metadata(self, syncdata_ids):
        metadata = []
        for syncdata in syncdata_ids:
            attachments = []
            deal_id = syncdata.get('deal_id', '')
            deal_url = f"/crm/v3/objects/deals/{deal_id}"
            deal_resp = get_response(deal_url)
            files = syncdata.get('files', [])
            for file_id in files:
                url = f"/files/v3/files/{file_id}"
                response = get_response(url)
                attachments.append(response.json())
            deal_resp = deal_resp.json()
            deal_resp['attachments'] = attachments
            metadata.append(deal_resp)
        return metadata
