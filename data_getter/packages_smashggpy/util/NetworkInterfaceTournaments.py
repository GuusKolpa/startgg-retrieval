import json
import requests
from data_getter.packages_smashggpy.common.Common import flatten

class NetworkInterfaceTournaments(object):
	"""This is a separate class the query for the top level 'tournaments' object differs from any underlying nodes.
	"""
	API_URL='https://api.start.gg/gql/alpha'

	@staticmethod
	def get_headers():
		return {
			'X-Source': 'smashggpy',
			'Content-Type': 'application/json',
			'Authorization': 'Bearer {}'.format(TokenHandler.get_token())
		}

	@staticmethod
	def query(query_string: str, variables: dict):
		Logger.debug('NetworkInterfaceTournaments.query: creating query object')
		query = QueryFactory.create(query_string, variables)
		Logger.debug('NetworkInterfaceTournaments.query: created query {}'.format(query))

		Logger.debug('NetworkInterfaceTournaments.query: sending query to queue')
		QueryQueue.get_instance().add(query)
		return NetworkInterfaceTournaments.execute_query(query)

	@staticmethod
	def paginated_query(query_string: str, variables: dict) -> list:
		Logger.debug('NetworkInterfaceTournaments.paginated_query: creating query object')
		query = QueryFactory.create(query_string, variables)
		Logger.debug('NetworkInterfaceTournaments.paginated_query: created query {}'.format(query))

		Logger.debug('NetworkInterfaceTournaments.paginated_query: sending query to queue')
		QueryQueue.get_instance().add(query)

		results = []
		initial_result = NetworkInterfaceTournaments.execute_query(query)
		base_data = NetworkInterfaceTournaments.parse_paginated_result(initial_result)
		results.append(base_data['nodes'])

		total_pages = base_data['pageInfo']['totalPages']
		for i in range(2, total_pages + 1, 1):
			variables['page'] = i
			current_query = QueryFactory.create(query_string, variables)
			current_result = NetworkInterfaceTournaments.execute_query(current_query)
			current_base_data = NetworkInterfaceTournaments.parse_paginated_result(current_result)
			results.append(current_base_data['nodes'])

		return flatten(results)

	@staticmethod
	def parse_paginated_result(results: dict):
		main_key = list(results['data'].keys())[0]
		secondary_key = list(results['data'][main_key].keys())[0]
		base_data = results['data'][main_key]
		return base_data

	@staticmethod
	def execute_query(query):
		log = Logger.get_instance()
		url = NetworkInterfaceTournaments.API_URL
		headers = NetworkInterfaceTournaments.get_headers()
		payload = query.get_query_dict()

		log.debug('NetworkInterfaceTournaments.query: Payload: {}'.format(payload))
		log.debug('NetworkInterfaceTournaments.query: Headers: {}'.format(headers))

		retry_counter = 0
		response = requests.post(url=url, headers=headers, json=payload)
		while response.status_code != 200 and retry_counter <= 3:
			retry_counter += 1
			log.info('NetworkInterface.query: Retrying request... ({} of 3)'.format(retry_counter))
			response = requests.post(url=url, headers=headers, json=payload)

		log.debug('NetworkInterfaceTournaments.query: {}'.format(response))
		log.debug('NetworkInterfaceTournaments.query: JSON Response: {}'.format(response.json()))
		return response.json()

# Path imports
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.util.TokenHandler import TokenHandler
from data_getter.packages_smashggpy.util.QueryFactory import QueryFactory
from data_getter.packages_smashggpy.util.QueryQueue import QueryQueue