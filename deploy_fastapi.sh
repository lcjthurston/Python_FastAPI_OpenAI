#!/bin/bash

# This script deploys a FastAPI application to Azure App Service.
# Before running:
# 1. Ensure you have Azure CLI installed and logged in (`az login`).
# 2. Make sure you have a `requirements.txt` file in your project root
#    containing fastapi, uvicorn, and pydantic.
# 3. Replace the placeholder values with your desired names and location.

# --- Configuration Variables ---
RESOURCE_GROUP_NAME="My_new_resource_group"           # Name of your Azure Resource Group
LOCATION="Canada Central"                             # Azure region (e.g., eastus, westeurope)
APP_SERVICE_PLAN_NAME="ASP-Mynewresourcegroup-83fd (B1: 1)"         # Name for your App Service Plan
WEBAPP_NAME="hopefulwebapp"    # IMPORTANT: THIS MUST BE GLOBALLY UNIQUE IN AZURE!
PYTHON_RUNTIME="PYTHON|3.13.2"                  # Python runtime version

echo "--- Deploying FastAPI App to Azure App Service ---"

# 1. Log in to Azure (if not already logged in).
#    This command will open a browser for authentication.
echo "Logging into Azure..."
az login --output none # --output none to suppress verbose output

# 2. Set your default subscription (if you have multiple).
#    Replace "Your Subscription Name or ID" with your actual subscription name or ID.
echo "Setting Azure subscription..."
az account set --subscription "f7585061-da51-47c8-aa79-c0fb336125b3"

# 3. Create a resource group if it doesn't exist.
echo "Creating resource group: $RESOURCE_GROUP_NAME in $LOCATION..."
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"

# 4. Create an App Service Plan (e.g., Free tier - F1).
#    The --is-linux flag is important for Python apps.
echo "Creating App Service Plan: $APP_SERVICE_PLAN_NAME..."
az appservice plan create --name "$APP_SERVICE_PLAN_NAME" --resource-group "$RESOURCE_GROUP_NAME" --sku F1 --is-linux

# 5. Create the Web App.
echo "Creating Web App: $WEBAPP_NAME..."
az webapp create --resource-group "$RESOURCE_GROUP_NAME" --plan "$APP_SERVICE_PLAN_NAME" --name "$WEBAPP_NAME" --runtime "$PYTHON_RUNTIME"

# 6. Deploy your code from the current directory.
#    This command detects your FastAPI app and sets up Uvicorn.
echo "Deploying code to Web App..."
az webapp up --name "$WEBAPP_NAME" --resource-group "$RESOURCE_GROUP_NAME"

# 7. Get the public URL of the deployed app
echo "Retrieving deployed app URL..."
APP_URL=$(az webapp show --name "$WEBAPP_NAME" --resource-group "$RESOURCE_GROUP_NAME" --query "defaultHostName" --output tsv)
PUBLIC_URL="https://$APP_URL"

echo "Deployment complete!"
echo "Your FastAPI application is deployed at: $PUBLIC_URL"
echo "You can access the OpenAPI schema at: $PUBLIC_URL/openapi.json"
echo "Remember to update your FastAPI app's servers URL in main.py to this public URL and redeploy."

az webapp deploy \  --resource-group "My_new_resource_group" \  --name "hopefulwebapp" \  --src-path "." \  --startup-command "uvicorn main:app --host 0.0.0.0 --port $PORT"