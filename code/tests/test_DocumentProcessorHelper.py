import pytest
from unittest.mock import MagicMock, patch
from backend.batch.utilities.helpers.DocumentProcessorHelper import DocumentProcessor

AZURE_SEARCH_INDEXER_NAME = "mock-indexer-name"


@pytest.fixture(autouse=True)
def env_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.EnvHelper"
    ) as mock:
        env_helper = mock.return_value
        env_helper.AZURE_SEARCH_INDEXER_NAME = AZURE_SEARCH_INDEXER_NAME

        yield env_helper


@pytest.fixture(autouse=True)
def llm_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.LLMHelper"
    ) as mock:
        llm_helper = mock.return_value
        llm_helper.get_embedding_model.return_value.embed_query.return_value = [
            0
        ] * 1536

        yield llm_helper


@pytest.fixture(autouse=True)
def azure_search_iv_index_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.AzureSearchIVIndexHelper"
    ) as mock:
        yield mock


@pytest.fixture(autouse=True)
def azure_search_iv_datasource_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.AzureSearchIVDatasourceHelper"
    ) as mock:
        yield mock


@pytest.fixture(autouse=True)
def azure_search_iv_skillset_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.AzureSearchIVSkillsetHelper"
    ) as mock:
        yield mock


@pytest.fixture(autouse=True)
def azure_search_iv_indexer_helper_mock():
    with patch(
        "backend.batch.utilities.helpers.DocumentProcessorHelper.AzureSearchIVIndexerHelper"
    ) as mock:
        yield mock


def test_process_integrated_vectorisation(
    env_helper_mock: MagicMock,
    llm_helper_mock: MagicMock,
    azure_search_iv_index_helper_mock: MagicMock,
    azure_search_iv_datasource_helper_mock: MagicMock,
    azure_search_iv_skillset_helper_mock: MagicMock,
    azure_search_iv_indexer_helper_mock: MagicMock,
):
    # given
    document_processor = DocumentProcessor()
    source_url = "https://dagrs.berkeley.edu/sites/default/files/2020-01/sample.pdf"

    # when
    result = document_processor.process_using_integrated_vectorisation(source_url)

    # then
    azure_search_iv_datasource_helper_mock.assert_called_once_with(env_helper_mock)
    azure_search_iv_datasource_helper_mock.return_value.create_or_update_datasource.assert_called_once()

    azure_search_iv_index_helper_mock.assert_called_once_with(
        env_helper_mock, llm_helper_mock
    )
    azure_search_iv_index_helper_mock.return_value.create_or_update_index.assert_called_once()

    azure_search_iv_skillset_helper_mock.assert_called_once_with(env_helper_mock)
    azure_search_iv_skillset_helper_mock.return_value.create_skillset.assert_called_once()

    azure_search_iv_indexer_helper_mock.assert_called_once_with(env_helper_mock)
    azure_search_iv_indexer_helper_mock.return_value.create_or_update_indexer.assert_called_once()

    assert (
        result
        == azure_search_iv_indexer_helper_mock.return_value.create_or_update_indexer.return_value
    )
    assert (
        azure_search_iv_skillset_helper_mock.return_value.create_skillset.return_value.skills
        is not None
    )
