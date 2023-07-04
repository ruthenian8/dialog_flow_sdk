from utils.services import (
    get_sf,
    get_sfp,
    get_midas,
    get_entities,
    get_entity_ids,
    get_wiki_parser_triplets,
    get_intent_and_ext_sf,
)

pre_services = [get_sf, get_sfp, get_midas, get_entities, get_entity_ids, get_wiki_parser_triplets, get_intent_and_ext_sf]