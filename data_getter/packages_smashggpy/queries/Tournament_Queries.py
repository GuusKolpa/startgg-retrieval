import data_getter.packages_smashggpy.queries.Schema as schema

get_tournament = """
query TournamentQuery($id: ID!){{
    tournament(id: $id){{
        {0}
    }}
}}
""".format(schema.tournament_schema)

get_tournament_by_slug = """
query TournamentQuery($slug: String){{
    tournament(slug: $slug){{
        {0}
    }}
}}
""".format(schema.tournament_schema)


get_tournament_events = """
query TournamentEvents($id: ID!){{
    tournament(id: $id){{
        events{{
            {0}
        }}
    }}
}}
""".format(schema.event_schema)

get_tournament_phases = """
query TournamentPhases($id: ID!){{
    tournament(id: $id){{
        events{{
            phases{{
                {0}
            }}
        }}
    }}
}}
""".format(schema.phase_schema)

get_tournament_phase_groups = """
query TournamentPhaseGroups($id: ID!){{
    tournament(id: $id){{
        events{{
            phaseGroups{{
                {0}
            }}
        }}
    }}
}}
""".format(schema.phase_group_schema)

get_tournament_players = """
query TournamentPlayersQuery($id: ID!, $page: Int, $perPage: Int) {
  tournament(id: $id) {
    participants(query: {
      page: $page
      perPage: $perPage
      sortBy: "id ASC"
    }) {
            pageInfo{
                totalPages
                perPage
                page
            }
      nodes {
        player{
          id
          gamerTag
          user{
            genderPronoun
            location{
              country
              city
            }
          }
        }
      }
    }
  }
}
"""

get_tournaments_by_country = """
query TournamentsByCountry($cCode: String!, $perPage: Int, $page:Int) {{
  tournaments(query: {{
    perPage: $perPage
    page: $page
    filter: {{
      countryCode: $cCode
      videogameIds: {0}
      
    }}
  }})
  {{pageInfo{{
    perPage
    totalPages
  }}
   
    nodes {{
      id
      slug
      countryCode
    }}
  }}
}}""".format(schema.video_game_list)