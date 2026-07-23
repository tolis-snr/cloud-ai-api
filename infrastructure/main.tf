# 1. Instruct Terraform to download the Azure Provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# 2. Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  skip_provider_registration = true
}

# 3. Variable for the Gemini API Key (Passed securely, not hardcoded!)
variable "gemini_api_key" {
  type        = string
  description = "The API key for Google Gemini"
  sensitive   = true
}

# --- SKELETON 1: Resource Group ---
# A logical container for your Azure resources.
resource "azurerm_resource_group" "rg" {
  # Name it something like "terraform-ai-rg"
  # Set the location to "Italy North" (or whatever worked for you)
  # --- WRITE YOUR CODE BELOW ---
  name = "terraform-ai-rg"
  location = "Italy North"
}

# --- SKELETON 2: App Service Plan ---
# The underlying server/VM that runs your app.
resource "azurerm_service_plan" "app_plan" {
  # Name it "terraform-ai-plan"
  # Link it to the Resource Group's name and location
  # Set os_type to "Linux" and sku_name to "F1" (Free tier)
  # --- WRITE YOUR CODE BELOW ---
  name                = "terraform-ai-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "F1"
}

# --- SKELETON 3: Linux Web App (The actual API) ---
resource "azurerm_linux_web_app" "web_app" {
  # Name it something UNIQUE (e.g., "tolis-tf-ai-api") - This becomes the URL!
  # Link it to the resource group and the app plan
  # --- WRITE YOUR CODE BELOW ---
  name                = "tolis-tf-ai-api"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_service_plan.app_plan.location
  service_plan_id     = azurerm_service_plan.app_plan.id

  # Configuration for Docker
  site_config {
    always_on = false # Must be false for Free (F1) tier
    application_stack {
      # Replace 'tolissnr' and 'tolis-ai-api' with your exact Docker Hub details
      docker_image_name   = "tolissnr/tolis-ai-api:latest"
      docker_registry_url = "https://index.docker.io"
    }
  }

  # Environment Variables
  app_settings = {
    "WEBSITES_PORT"                      = "8000"
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE"= "false"
    "GEMINI_API_KEY"                      = var.gemini_api_key
  }
}

# Output the final URL so Terraform prints it at the end
output "website_url" {
  value = "https://${azurerm_linux_web_app.web_app.name}.azurewebsites.net/docs"
}
