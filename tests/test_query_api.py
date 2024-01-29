from import_ovapi_transport_data import query_api

import json
import unittest
from unittest.mock import patch, MagicMock


class TestQueryApi(unittest.TestCase):

    @patch("requests.get")
    def test_query_api(self, mock_requests_get):

        # Load success data from sample
        with open("./sample_data/success_data.json") as f:
            success_data = json.load(f)

        # Create mocked http success response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = success_data
        mock_requests_get.return_value = mock_response

        assert query_api("url", "/endpoint") == success_data

    @patch("requests.get")
    def test_query_api_server_error(self, mock_requests_get):

        # Create mocked http server error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests_get.return_value = mock_response

        assert query_api("url", "/endpoint") == None

    @patch("requests.get")
    def test_query_api_succes_with_retry(self, mock_requests_get):

        # Create mocked http server error response
        mock_error_response = MagicMock()
        mock_error_response.status_code = 500

        # Load success data from sample
        with open("./sample_data/success_data.json") as f:
            success_data = json.load(f)

        # Create mocked http success response
        mock_success_response = MagicMock()
        mock_success_response.status_code = 200
        mock_success_response.json.return_value = success_data

        mock_requests_get.side_effect = [
            mock_error_response,
            mock_error_response,
            mock_success_response
        ]

        assert query_api("url", "/endpoint", max_tries=5) == success_data


if __name__ == '__main__':
    unittest.main()
