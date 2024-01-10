import os
import logging
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.keyvault.secrets import SecretClient

logger = logging.getLogger(__name__)

class EnvHelper:
    def __init__(self, **kwargs) -> None:
        load_dotenv()

        self.AUTH_TYPE =os.environ.get("AUTH_TYPE")
        if not self.AUTH_TYPE == 'rbac' and os.environ.get("USE_KEY_VAULT"):
            self.credential = DefaultAzureCredential()
            self.secret_client = SecretClient(os.environ.get("AZURE_KEY_VAULT_ENDPOINT"), self.credential)
            self.AZURE_SEARCH_KEY = self.secret_client.get_secret(os.environ.get("AZURE_SEARCH_KEY")).value
            self.AZURE_OPENAI_KEY = self.secret_client.get_secret(os.environ.get("AZURE_OPENAI_KEY")).value
        else:
            self.AZURE_SEARCH_KEY = None if self.AUTH_TYPE == 'rbac' else os.environ.get("AZURE_SEARCH_KEY")
            self.AZURE_OPENAI_KEY = None if self.AUTH_TYPE == 'rbac' else os.environ.get("AZURE_OPENAI_KEY")
            
        # Azure Search
        self.AZURE_SEARCH_SERVICE = os.getenv('AZURE_SEARCH_SERVICE', '')
        self.AZURE_SEARCH_INDEX = os.getenv('AZURE_SEARCH_INDEX', '')
        self.AZURE_SEARCH_USE_SEMANTIC_SEARCH = os.getenv('AZURE_SEARCH_USE_SEMANTIC_SEARCH', '')
        self.AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG = os.getenv('AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG', '')
        self.AZURE_SEARCH_INDEX_IS_PRECHUNKED = os.getenv('AZURE_SEARCH_INDEX_IS_PRECHUNKED', '')
        self.AZURE_SEARCH_TOP_K = os.getenv('AZURE_SEARCH_TOP_K', '')
        self.AZURE_SEARCH_ENABLE_IN_DOMAIN = os.getenv('AZURE_SEARCH_ENABLE_IN_DOMAIN', '')
        self.AZURE_SEARCH_FIELDS_ID = os.getenv('AZURE_SEARCH_FIELDS_ID', 'id')
        self.AZURE_SEARCH_CONTENT_COLUMNS = os.getenv('AZURE_SEARCH_CONTENT_COLUMNS', 'content')
        self.AZURE_SEARCH_CONTENT_VECTOR_COLUMNS = os.getenv('AZURE_SEARCH_CONTENT_VECTOR_COLUMNS', 'content_vector')
        self.AZURE_SEARCH_DIMENSIONS = os.getenv('AZURE_SEARCH_DIMENSIONS', '1536')
        self.AZURE_SEARCH_FILENAME_COLUMN = os.getenv('AZURE_SEARCH_FILENAME_COLUMN', 'filepath')
        self.AZURE_SEARCH_TITLE_COLUMN = os.getenv('AZURE_SEARCH_TITLE_COLUMN', 'title')
        self.AZURE_SEARCH_URL_COLUMN = os.getenv('AZURE_SEARCH_URL_COLUMN', 'url')
        self.AZURE_SEARCH_FIELDS_TAG = os.getenv('AZURE_SEARCH_FIELDS_TAG', 'tag')
        self.AZURE_SEARCH_FIELDS_METADATA = os.getenv('AZURE_SEARCH_FIELDS_METADATA', 'metadata')
        self.AZURE_SEARCH_CONVERSATIONS_LOG_INDEX = os.getenv('AZURE_SEARCH_CONVERSATIONS_LOG_INDEX', 'conversations')
        # Azure OpenAI
        self.AZURE_OPENAI_RESOURCE = os.getenv('AZURE_OPENAI_RESOURCE', '')
        self.AZURE_OPENAI_MODEL = os.getenv('AZURE_OPENAI_MODEL', '')
        self.AZURE_OPENAI_MODEL_NAME = os.getenv('AZURE_OPENAI_MODEL_NAME', '')
        self.AZURE_OPENAI_TEMPERATURE = os.getenv('AZURE_OPENAI_TEMPERATURE', '')
        self.AZURE_OPENAI_TOP_P = os.getenv('AZURE_OPENAI_TOP_P', '')
        self.AZURE_OPENAI_MAX_TOKENS = os.getenv('AZURE_OPENAI_MAX_TOKENS', '')
        self.AZURE_OPENAI_STOP_SEQUENCE = os.getenv('AZURE_OPENAI_STOP_SEQUENCE', '')
        self.AZURE_OPENAI_SYSTEM_MESSAGE = os.getenv('AZURE_OPENAI_SYSTEM_MESSAGE', '')
        self.AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION', '')
        self.AZURE_OPENAI_STREAM = os.getenv('AZURE_OPENAI_STREAM', '')
        self.AZURE_OPENAI_EMBEDDING_MODEL = os.getenv('AZURE_OPENAI_EMBEDDING_MODEL', '')
        self.AZURE_TOKEN_PROVIDER = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
         # Set env for OpenAI SDK
        self.OPENAI_API_TYPE = "azuread" if self.AUTH_TYPE == 'rbac' else "azure"
        self.OPENAI_API_BASE = f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
        self.OPENAI_API_KEY = self.AZURE_OPENAI_KEY
        self.OPENAI_API_VERSION = self.AZURE_OPENAI_API_VERSION
        os.environ["OPENAI_API_TYPE"] = "azuread" if self.AUTH_TYPE == 'rbac' else "azure"
        os.environ["OPENAI_API_BASE"] = f"https://{os.getenv('AZURE_OPENAI_RESOURCE')}.openai.azure.com/"
        os.environ["OPENAI_API_KEY"] = self.AZURE_OPENAI_KEY
        os.environ["OPENAI_API_VERSION"] = self.AZURE_OPENAI_API_VERSION
        # Azure Functions - Batch processing
        self.BACKEND_URL = os.getenv('BACKEND_URL', '')
        self.AzureWebJobsStorage = os.getenv('AzureWebJobsStorage', '')
        self.DOCUMENT_PROCESSING_QUEUE_NAME = os.getenv('DOCUMENT_PROCESSING_QUEUE_NAME', '')
        # Azure Blob Storage
        self.AZURE_BLOB_ACCOUNT_NAME = os.getenv('AZURE_BLOB_ACCOUNT_NAME', '')
        self.AZURE_BLOB_ACCOUNT_KEY = self.secret_client.get_secret(os.getenv("AZURE_BLOB_ACCOUNT_KEY", '')).value if os.getenv("USE_KEY_VAULT", '') else os.getenv("AZURE_BLOB_ACCOUNT_KEY", '')
        self.AZURE_BLOB_CONTAINER_NAME = os.getenv('AZURE_BLOB_CONTAINER_NAME', '')
        # Azure Form Recognizer
        self.AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv('AZURE_FORM_RECOGNIZER_ENDPOINT', '')
        self.AZURE_FORM_RECOGNIZER_KEY = self.secret_client.get_secret(os.getenv("AZURE_FORM_RECOGNIZER_KEY", '')).value if os.getenv("USE_KEY_VAULT", '') else os.getenv('AZURE_FORM_RECOGNIZER_KEY', '')
        # Azure App Insights
        self.APPINSIGHTS_CONNECTION_STRING = os.getenv('APPINSIGHTS_CONNECTION_STRING', '')
        # Azure AI Content Safety
        self.AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv('AZURE_CONTENT_SAFETY_ENDPOINT', '')
        self.AZURE_CONTENT_SAFETY_KEY = self.secret_client.get_secret(os.getenv("AZURE_CONTENT_SAFETY_KEY", '')).value if os.getenv("USE_KEY_VAULT", '') else os.getenv('AZURE_CONTENT_SAFETY_KEY', '')
        # Orchestration Settings
        self.ORCHESTRATION_STRATEGY = os.getenv('ORCHESTRATION_STRATEGY', 'openai_function')
    
    @staticmethod
    def check_env():
        for attr, value in EnvHelper().__dict__.items():
            if value == '':
                logging.warning(f"{attr} is not set in the environment variables.")
