# Auto-Screenshot
Auto-Screenshot is a service that captures screenshots from [cvedetails](https://www.cvedetails.com/) based on package names provided in a text file.

## File Structure
- Front-End: `auto-screenshot`
- Back-End: `backend`

## Running the Service
### Option 1: Run with Docker (Recommended)

To run the service using Docker, execute the following command:
```bash
docker compose up -d
```
By default, the front-end service will be accessible at http://localhost:8932/screenshot.

### Option 2: Run Locally
To run the service locally, follow these steps:
1. **Modify Ports Configuration**: Edit the port settings in `compose.yml` and `auto-screenshot/.env` to suit your environment.

2. **Install Chrome Driver**: You must install the Chrome driver to run the service locally. Detailed instructions can be found in the `backend/README.md`.

#### Start the Front-End Server
In the `auto-screenshot` directory, run:
```bash
npm run dev
```
#### Start the Back-End Server
In the `backend` directory, run:
```bash
uvicorn api:app --log-level debug --reload
```

## Ports Configuration
In the `compose.yml` file, you can configure the ports for both the front-end and back-end servers. By default, the front-end server is mapped to port `8932`, and the back-end server is mapped to port `8933`.

### Key Environment Variables

- In `compose.yml`:
    - `FRONTEND_DOMAIN_FROM_BACKEND`: The front-end URL as seen by the back-end server.
    - `FRONTEND_DOMAIN_FROM_CLIENT`: The front-end URL as seen by the client.

- In `auto-screenshot/.env`:
    - `BACKEND_DOMAIN_FROM_CLIENT`: The back-end URL as seen by the front-end client.

When changing the default port settings in `compose.yml`, ensure to update the corresponding environment variables in both `compose.yml` and `auto-screenshot/.env`.