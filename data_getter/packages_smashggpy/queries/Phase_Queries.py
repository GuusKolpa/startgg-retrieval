import data_getter.packages_smashggpy.queries.Schema as schema

phase_by_id = """
query PhaseQuery($id: ID!){{
    phase(id: $id){{
        {0}
    }}
}}
""".format(schema.phase_schema)

phase_phase_groups = """
query PhasePhaseGroups($id: ID!, $page: Int, $perPage: Int, $entrantIds: [ID], $filter: PhaseGroupPageQueryFilter){{
   phase(id: $id){{
        phaseGroups(query: {{
            page: $page,
            perPage: $perPage,
            sortBy: "id ASC"
            entrantIds: $entrantIds,
            filter: $filter
        }})
        {{
            pageInfo{{
                totalPages
            }}
            nodes{{
                {0}
            }}  
        }}
    }}
}}
""".format(schema.phase_group_schema)