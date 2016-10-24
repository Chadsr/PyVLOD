#!/usr/bin/env python

import re
from collections import defaultdict
from datetime import datetime
from itertools import islice

from iribaker import to_iri
from rdflib import URIRef, Literal

import constants as c
import load_json as h

# maps mep id to dbr iri
dict_mep = defaultdict(list)
dict_dossier = defaultdict(list)


# def mepid_to_profile_iri(id):
#   return URIRef(to_iri('http://www.europarl.europa.eu/meps/en/' + str(id) + '/_history.html'))

# Needs changing?
def id_to_iri(id_):
    return URIRef(to_iri(c.ont + str(id_)))


def format_name_string(input_string):
    input_string = re.sub('\(.+?\)', '', input_string)
    input_string = input_string.lower().title().encode('utf-8').strip()
    input_string = re.sub('\s+', '_', input_string)
    return input_string


def name_to_dbr(name):
    formatted = format_name_string(name)
    iri = to_iri(c.dbr + formatted)
    uriref = URIRef(iri)
    return uriref


# TODO: See if there is a better dossier url to use instead of dossier['meta']['source']
# TODO: See if there is a better dossier text to use instead of dossier['procedure']['title']
def convert_dossier(path, dataset, graph_uri):
    json_data = h.load_json(path)

    graph = dataset.graph(graph_uri)

    for dossier in islice(json_data, 0, c.DOSSIER_LIMIT):
        for activity in dossier['activities']:
            if 'type' in activity:
                if activity['type'] == c.DOSSIER_TYPE:
                    dossier_id = dossier['_id']
                    dossier_url = Literal(dossier['meta']['source'], datatype=c.URI)
                    dossier_date = Literal(
                        datetime.strptime(dossier['activities'][0]['date'].split('T')[0], '%Y-%m-%d').date(),
                        datatype=c.DATE)
                    dossier_title = Literal(dossier['procedure']['title'].strip(), datatype=c.STRING)

                    # User the meta url as the iri
                    dossier_uri = URIRef(to_iri(dossier_url))

                    graph.add((dossier_uri, c.PROCESSED_BY, c.EUROPEAN_PARLIAMENT))
                    # graph.add((dossier_uri, RDF.type, DOSSIER))
                    dataset.add((dossier_uri, c.DOSSIER_TITLE, dossier_title))
                    dataset.add((dossier_uri, c.URI, dossier_url))
                    dataset.add((dossier_uri, c.DATE, dossier_date))

                    # Store the id and uri in the dictionary for use later
                    dict_dossier[dossier_id].append(dossier_uri)

                    print 'Dossier:', dossier_uri
                    break  # dossier matches DOSSIER_TYPE, no need to search more activities

    return dataset, graph


def convert_votes(path, dataset, graph_uri):

    json_data = h.load_json(path)

    graph = dataset.graph(graph_uri)

    for votes in islice(json_data, 0, c.VOTES_LIMIT):
        if 'dossierid' in votes:
            dossier_id = votes['dossierid']

            # If this dossier is in our dictionary of useful dossiers, continue
            if dossier_id in dict_dossier:
                dossier_uri = dict_dossier[dossier_id][0]
                # title = votes['title']
                # url = dossier['url']
                # ep_title = dossier['eptitle']

                if 'Abstain' in votes:
                    for group in votes['Abstain']['groups']:
                        # group_name = group['group']
                        for vote in group['votes']:
                            # user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], c.ABSTAINS, dossier_uri))
                                print 'Abstains dossier:', dossier_uri

                if 'For' in votes:
                    for group in votes['For']['groups']:
                        # group_name = group['group']
                        for vote in group['votes']:
                            # user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], c.VOTES_FOR, dossier_uri))
                                print 'Vote for dossier:', dossier_uri

                if 'Against' in votes:
                    for group in votes['Against']['groups']:
                        # group_name = group['group']
                        for vote in group['votes']:
                            # user_id = vote['userid']
                            voter_id = vote['ep_id']
                            if voter_id in dict_mep:
                                graph.add((dict_mep[voter_id][0], c.VOTES_AGAINST, dossier_uri))
                                print 'Vote against dossier:', dossier_uri
    return dataset, graph


def convert_mep(path, dataset, graph_uri):
    json_data = h.load_json(path)

    graph = dataset.graph(graph_uri)

    for mep in islice(json_data, 0, c.MEP_LIMIT):
        # Get raw values
        user_id = mep['UserID']

        full_name = Literal(mep['Name']['full'], datatype=c.STRING)

        mep_uri = name_to_dbr(full_name)

        # append to global dictionary
        dict_mep[user_id].append(mep_uri)

        profile_url = Literal(mep['meta']['url'], datatype=c.URI)

        if 'Photo' in mep:
            photo_url = Literal(mep['Photo'], datatype=c.URI)
            dataset.add((mep_uri, c.URI, photo_url))

        if 'Birth' in mep:
            if 'date' in mep['Birth']:
                birth_date = mep['Birth']['date']
                if birth_date != '':
                    birth_date = Literal(datetime.strptime(birth_date.split('T')[0], '%Y-%m-%d').date(),
                                         datatype=c.DATE)
                    dataset.add((mep_uri, c.BIRTH_DATE, birth_date))

            if 'place' in mep['Birth']:
                birth_place = mep['Birth']['place'].strip()
                dataset.add((mep_uri, c.BIRTH_PLACE, name_to_dbr(birth_place)))

        # if 'active' in mep: active = mep['active'] # interesting but unused atm

        # Can be in more than one?
        # organisation = mep['Groups'][0]['Organisation']
        # organisationId = mep['Groups'][0]['groupid']
        # organisationRole = mep['Groups'][0]['role']

        if 'Gender' in mep:
            gender = mep['Gender']
            if gender == 'M':
                dataset.add((mep_uri, c.GENDER, c.MALE))
            elif gender == 'F':
                dataset.add((mep_uri, c.GENDER, c.FEMALE))

        dataset.add((mep_uri, c.FULL_NAME, full_name))
        dataset.add((mep_uri, c.URI, profile_url))

        # graph.add((mep_uri, MEMBER_OF, URIRef(to_iri(dbr + 'European_Parliament'))))

        print 'MEP:', mep_uri

    return dataset, graph
