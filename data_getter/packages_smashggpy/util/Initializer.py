
__daemon_thread = None

def initialize(api_token: str, log_level: str='info'):
	Logger.init(log_level)
	TokenHandler.init(api_token)

	# initialize the query queue
	# QueryQueue.init()

	# initialize query queue daemon in background
	QueryQueueDaemon.run_daemon()

def uninitialize():
	TokenHandler.uninit()
	QueryQueueDaemon.kill_daemon()

from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.util.TokenHandler import TokenHandler
from data_getter.packages_smashggpy.util.QueryQueue import QueryQueue
from data_getter.packages_smashggpy.util.ThreadFactory import ThreadFactory
from data_getter.packages_smashggpy.util.QueryQueueDaemon import QueryQueueDaemon
