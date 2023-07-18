tournament_schema = """
id
name
slug
city
countryCode
timezone
isOnline
startAt
endAt
owner{
  id
  player{
    gamerTag
  }
}
"""

event_schema = """
id
name
teamRosterSize{
      minPlayers
      }
tournament {
    id
}
videogame {
      id
    }
numEntrants
isOnline
"""

phase_schema = """
id
name
numSeeds
groupCount
"""

phase_group_schema = """
id
phase{
  event{
    id
  }
  name
}
displayIdentifier
bracketType
"""

user_schema = """
id
gamerTag
prefix
color
twitchStream
twitterHandle
youtube
region
state
country
gamerTagChangedAt
"""

attendee_contact_info_schema = """
id
city
state
stateId
country
countryId
name
nameFirst
nameLast
zipcode
"""

attendee_schema = """
id
gamerTag
prefix
createdAt
claimed
verified
playerId
phoneNumber
connectedAccounts
contactInfo{{
    {0}
}}
events{{
    id
}}
""".format(attendee_contact_info_schema)

entrant_schema = """
id
name
eventId
skill
participants{{
    {0}
}}
""".format(attendee_schema)


gg_set_schema = """
id
state
phaseGroup
{
    id
}
completedAt
fullRoundText
displayScore
slots{
    id
    standing {
      placement
    }
    entrant{
      id
    }
}
"""

stream = """
id
eventId
tournamentId
streamName
numSetups
streamSource
streamType
streamTypeId
isOnline
enabled
followerCount
removesTasks
streamStatus
streamGame
streamLogo
"""

video_game_list="[1]"