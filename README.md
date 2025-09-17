# SalesVault CRM Integration Backend

## Overview
This Django backend integrates with HubSpot CRM to list, select, and sync files to a local database. It supports JWT authentication, Celery background tasks, and advanced filtering.

## Environment Setup
- Create a `.env` file in the project root.
- Add your API key:
  ```
  API_KEY=your_hubspot_api_key_here
  ```

## Login Details (Demo)
Use the following credentials to obtain an access token:
```json
{
    "username": "abhijith",
    "password": "123"
}
```

### Get Access Token
**Endpoint:**
```
POST /sync/api/v1/auth/login/
```
**Request Body:**
```json
{
    "username": "abhijith",
    "password": "123"
}
```
**Response:**
```json
{
    "token": "<access_token>",
    "refresh": "<refresh_token>",
    "status": 1
}
```

## API Endpoints

### 1. List CRM Files
- **GET** `/sync/api/v1/crm/files/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Description:** Lists all available files from HubSpot CRM deals.

### 2. Sync Files from CRM
- **POST** `/sync/api/v1/crm/sync-files/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
  ```json
  {
      "syncdata_ids": [
          {"deal_id": "123", "files": ["fileid1", "fileid2"]}
      ]
  }
  ```
- **Description:** Initiates background sync of selected files from CRM to the database.

### 3. List Synced Files
- **GET** `/sync/api/v1/crm/synced-files/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Description:** Lists all files that have been synchronized to the local database.

## Notes
- Make sure to set your HubSpot API key in the `.env` file as `API_KEY`.
- All API requests require a valid JWT access token in the `Authorization` header.
- For background tasks, ensure Redis and Celery are running.

---
For any issues, contact the maintainer.
