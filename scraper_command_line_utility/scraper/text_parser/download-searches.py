#download-searches.py
import text_parser.local_parse as local_parse

query = 'mulatto*+negro*'

local_parse.getSearchResults(query, "advanced", "1700", "00", "1750", "99", 13)

local_parse.getIndivTrials(query)