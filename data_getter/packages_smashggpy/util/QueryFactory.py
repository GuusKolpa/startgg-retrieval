import time

class QueryFactory(object):

	@staticmethod
	def create(query: str, variables: dict):
		Logger.get_instance().debug('created query with params [{}] [{}]'.format(query, variables))
		return Query(query, variables)


from data_getter.packages_smashggpy.util.Query import Query
from data_getter.packages_smashggpy.util.Logger import Logger