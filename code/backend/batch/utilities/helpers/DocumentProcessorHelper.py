import logging
from typing import List

from .AzureSearchIVIndexHelper import AzureSearchIVIndexHelper
from .AzureSearchIVIndexerHelper import AzureSearchIVIndexerHelper
from .AzureSearchIVDatasourceHelper import AzureSearchIVDatasourceHelper
from .AzureSearchIVSkillsetHelper import AzureSearchIVSkillsetHelper
from .AzureSearchHelper import AzureSearchHelper
from .DocumentLoadingHelper import DocumentLoading, LoadingSettings
from .DocumentChunkingHelper import DocumentChunking, ChunkingSettings
from ..common.SourceDocument import SourceDocument
from .EnvHelper import EnvHelper

logger = logging.getLogger(__name__)


class Processor(ChunkingSettings, LoadingSettings):
    def __init__(
        self, document_type: str, chunking: ChunkingSettings, loading: LoadingSettings
    ):
        self.document_type = document_type
        self.chunking = chunking
        self.loading = loading


class DocumentProcessor:
    def __init__(self):
        pass

    def process(self, source_url: str, processors: List[Processor]):
        env_helper: EnvHelper = EnvHelper()
        if env_helper.AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION:
            try:
                search_datasource_helper = AzureSearchIVDatasourceHelper()
                search_datasource_helper.create_or_update_datasource()
                search_index_helper = AzureSearchIVIndexHelper()
                search_index_helper.get_iv_search_store()
                search_skillset_helper = AzureSearchIVSkillsetHelper()
                search_skillset = search_skillset_helper.create_skillset()
                search_indexer_helper = AzureSearchIVIndexerHelper()
                search_indexer_helper.create_or_update_indexer(
                    env_helper.AZURE_SEARCH_INDEXER_NAME, skillset_name=search_skillset
                )
            except Exception as e:
                logger.error(f"Error processing {source_url}: {e}")
                raise e
        else:
            vector_store_helper = AzureSearchHelper()
            vector_store = vector_store_helper.get_vector_store()
            for processor in processors:
                try:
                    document_loading = DocumentLoading()
                    document_chunking = DocumentChunking()
                    documents: List[SourceDocument] = []
                    documents = document_loading.load(source_url, processor.loading)
                    documents = document_chunking.chunk(documents, processor.chunking)
                    keys = list(map(lambda x: x.id, documents))
                    documents = [
                        document.convert_to_langchain_document()
                        for document in documents
                    ]
                    return vector_store.add_documents(documents=documents, keys=keys)
                except Exception as e:
                    logger.error(f"Error adding embeddings for {source_url}: {e}")
                    raise e
