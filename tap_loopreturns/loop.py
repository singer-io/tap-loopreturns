import logging
from urllib import parse
import backoff
import requests

LOGGER = logging.getLogger()

#pylint: disable=too-few-public-methods
class Loop:

    def __init__(self, api_key, start_date, end_date=None):
        self.headers = {
            "X-Authorization": api_key,
            "Content-Type": "application/json"
        }
        self.start_date = start_date
        self.end_date = end_date
        self.base_url = 'https://api.loopreturns.com/api/v1/warehouse/return/list'

    @backoff.on_exception(backoff.expo,
                          requests.exceptions.RetryError,
                          max_tries=5)
    def _get(self, uri):
        response = requests.get(uri, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def returns(self, column_name, bookmark):
        url = self.base_url + "?from={start_date}&filter={column_name}"
        if self.end_date is not None:
            url += "&to={end_date}"
        url = url.format(start_date=parse.quote(bookmark),
                         column_name=column_name,
                         end_date=self.end_date)
        LOGGER.info("Sending request to %s", url)
        return self._get(url)
