import data_getter.packages_smashggpy.queries.Tournament_Queries as queries
from data_getter.packages_smashggpy.util import Initializer
from data_getter.packages_smashggpy.util.Logger import Logger
from data_getter.packages_smashggpy.util.QueryQueueDaemon import QueryQueueDaemon
from data_getter.packages_smashggpy.util.NetworkInterfaceTournaments import NetworkInterfaceTournaments as NI
import os
import tracemalloc

tracemalloc.start()

country_codes = ['NL', 'BE', 'UK', 'FR', 'IE', 'SE', 'ES', 'IT', 'DE', 'AT', 'CH', 'PT', 'NO', 'FI', 'DK', 'GR']
# country_codes = ['IT']
# arguments = sys.argv[0:1]

if __name__ == '__main__':

    tournament_list = []
    SGG_API_KEY = os.getenv('startgg_api_key')
    Initializer.initialize(SGG_API_KEY, 'info')

    for country_code in country_codes:
        data = NI.paginated_query(queries.get_tournaments_by_country, {"cCode":country_code})
        Logger.info('Retrieved tournament list for country: {}'.format(country_code))
        tournament_list.extend([slug_dict['slug'].split('/')[-1] for slug_dict in data])

    print(os.getcwd())
    with open("tournament_slug_list.txt", "w") as f:
        for s in tournament_list:
            f.write(str(s) +"\n")
    
QueryQueueDaemon.kill_daemon()