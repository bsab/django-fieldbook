import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FieldbookClient(object):

    # Constructor takes the Fieldbook credentials and base URL to set up a FieldbookClient
    def __init__(self, api_key, api_secret, fieldbook_url):

        self.__key = api_key
        self.__secret = api_secret
        self.__url = fieldbook_url
        pass

    def add_row(self, sheet, new_record_data):
        """Add a row to a Fieldbook sheet"""
        url = self.get_resource_url(sheet)

        request = requests.post(url, auth=(self.__key, self.__secret), json = new_record_data)
        logger.debug("Status Code: {0}".format(request.status_code))

        result = json.loads(request.text)
        logger.debug(result)

        return result

    def get_row(self, sheet, row_id, include_fields=None, exclude_fields=None, **kwargs):
        """Get a single row in a Fieldbook sheet"""
        url = self.get_resource_url(sheet, row_id)

        query_parameters = {}

        if include_fields:
            query_parameters['include'] = ','.join(include_fields)

        if exclude_fields:
            query_parameters['exclude'] = ','.join(exclude_fields)

        for key, value in kwargs.items():
            query_parameters[key] = value

        try:
            request = requests.get(url,
                                   auth=(self.__key, self.__secret),
                                   params=query_parameters)
            logger.debug("Status Code: {0}".format(request.status_code))
            return request.json()

        except requests.ConnectionError as e:
            logger.error('Cannot connect to Fieldbook API', exc_info=True)

        except Exception as e:
            logger.error(exc_info=True)

    def get_all_rows(self, sheet, include_fields=None, exclude_fields=None, **kwargs):
        """Get all rows in a Fieldbook sheet"""
        url = self.get_resource_url(sheet)

        query_parameters = {}

        if include_fields:
            query_parameters['include'] = ','.join(include_fields)

        if exclude_fields:
            query_parameters['exclude'] = ','.join(exclude_fields)

        for key, value in kwargs.items():
            query_parameters[key] = value

        try:
            request = requests.get(url,
                                   auth=(self.__key, self.__secret),
                                   params=query_parameters)
            logger.debug("Status Code: {0}".format(request.status_code))
            logger.debug('JSON: {0}'.format(request.json()))
            return request.json()

        except requests.ConnectionError as e:
            logger.error('Cannot connect to Fieldbook API')
            logger.error(e)

        except Exception as e:
            logger.error(e)

    def update_row(self, sheet, row_id, patch_data):
        """Update an existing row in a Fieldbook sheet"""
        url = self.get_resource_url(sheet, row_id)

        request = requests.patch(url, auth=(self.__key, self.__secret), json = patch_data)
        logger.debug("Status Code: {0}".format(request.status_code))

        result = json.loads(request.text)
        logger.debug(result)

        return result

    def delete_row(self, sheet, row_id):
        """Delete an existing row from a Fieldbook sheet"""
        url = self.get_resource_url(sheet, row_id)

        request = requests.delete(url, auth=(self.__key, self.__secret))
        logger.debug("Status Code: {0}".format(request.status_code))

        result = request.status_code
        logger.debug(result)

    def get_resource_url(self, sheet_name, row_id=None):
        """Take sheet / row parameters and return a valid formatted URL for a fieldbook resource"""
        if row_id:
            # Return a URL for a specific row resource
            url = str.format('{0}/{1}/{2}', self.__url, sheet_name, row_id)
            logger.debug('URL: {0}'.format(url))
            return url
        else:
            # Return a URL for a sheet resource
            url = str.format('{0}/{1}', self.__url, sheet_name)
            logger.debug('URL: {0}'.format(url))
            return url