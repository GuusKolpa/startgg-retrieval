import data_getter.packages_smashggpy.queries.Schema as schema

phase_group_by_id = """
query PhaseGroupQueries($id: ID!){{
    phaseGroup(id: $id){{
        {0}
    }}
}}
""".format(schema.phase_group_schema)

phase_group_attendees = """
query PhaseGroupAttendees($id: ID!, $page: Int, $perPage: Int, $filter: SeedPageFilter){{
    phaseGroup(id: $id){{
        paginatedSeeds(
            query: {{
                page: $page,
                perPage: $perPage,
                sortBy: "id ASC"
                filter: $filter
            }}
        )
        {{
            pageInfo{{
                totalPages
            }}
            nodes{{
                entrant{{
                    participants{{
                        {0}
                    }}
                }}
            }}
        }}
    }}
}}
""".format(schema.attendee_schema)

phase_group_entrants = """
query PhaseGroupEntrants($id: ID!, $page: Int, $perPage: Int, $filter: SeedPageFilter){{
    phaseGroup(id: $id){{
        paginatedSeeds(
            query: {{
                page: $page,
                perPage: $perPage,
                sortBy: "id ASC",
                filter: $filter
            }}
        )
        {{
            pageInfo{{
                totalPages
            }}
            nodes{{
                entrant{{
                    {0}
                }}
            }}
        }}
    }}
}}
""".format(schema.entrant_schema)

phase_group_sets = """
query PhaseGroupEntrants($id: ID!, $page: Int, $perPage: Int){{
    phaseGroup(id: $id){{
        sets(page:$page, perPage:$perPage, sortType:CALL_ORDER , filters: {{state:3}}){{
            pageInfo{{
                totalPages
            }}
            nodes{{
                {0}
            }}
        }}
    }}
}}
""".format(schema.gg_set_schema)
