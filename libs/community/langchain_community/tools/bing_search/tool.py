"""Refactored Bing Search Tools with updated parameter structure."""

from typing import Dict, List, Literal, Optional, Tuple

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool
from langchain_community.utilities.bing_search import BingSearchAPIWrapper


class BingSearchRun(BaseTool):  # type: ignore[override]
    """Tool that queries the Bing search API and returns a plain string result."""

    name: str = "bing_search"
    description: str = (
        "A simple wrapper around Bing Search API for current events. "
        "Use this tool when you need a quick string-based answer to a search query."
    )
    api_wrapper: BingSearchAPIWrapper

    def _run(
        self,
        *,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Execute the Bing search query and return raw string result."""
        return self.api_wrapper.run(query)


class BingSearchResults(BaseTool):  # type: ignore[override]
    """Tool that queries the Bing search API and returns structured results."""

    name: str = "bing_search_results_json"
    description: str = (
        "Wrapper around Bing Search API. "
        "Best used for getting JSON-formatted results (title, link, snippet). "
        "Input should be a search query. Returns top N search results."
    )
    api_wrapper: BingSearchAPIWrapper
    num_results: int = 4
    response_format: Literal["content_and_artifact"] = "content_and_artifact"

    def _run(
        self,
        *,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Tuple[str, List[Dict]]:
        """Run the search query and return structured response."""
        try:
            results = self.api_wrapper.results(query, self.num_results)
            return str(results), results
        except Exception as e:
            return repr(e), []
