from __future__ import absolute_import, unicode_literals

import datetime
import hashlib
import json
import logging
import pprint

from mopidy import local, models

import pyen

BATCH_SIZE = 1000
TASTEPROFILE_NAME = 'Mopidy local library'
TIMEFORMAT = '%Y-%m-%dT%H:%M:%S'

logger = logging.getLogger(__name__)


def uri_to_item_id(uri):
    digest = hashlib.sha256()
    digest.update(uri)
    return digest.hexdigest()


class EchonestLocalLibrary(local.Library):
    name = 'echonest'

    def __init__(self, config):
        self._en = pyen.Pyen(config['echonest']['apikey'])
        self._profile_id = None
        self._items = []

    def browse(self):
        return []

    def load(self):
        try:
            result = self._en.post(
                'tasteprofile/create', name=TASTEPROFILE_NAME, type='song')
            logger.info('Created new echonest tasteprofile: %s', result['id'])
        except pyen.PyenException as e:
            logger.debug('Creating profile failed: %s', e)

        profile = self._en.get('tasteprofile/profile', name=TASTEPROFILE_NAME)
        self._profile_id = profile['catalog']['id']
        return profile['catalog']['total']

    def lookup(self, uri):
        result = self._en.get('tasteprofile/read', id=self._profile_id,
                              item_id=uri_to_item_id(uri))
        pprint.pprint(result)
        # TODO: convert result to track
        return None

    def search(self, query=None, limit=100, offset=0, exact=False, uris=None):
        # TODO: map query to echonest search
        result = self._en.get(
            'song/search',  bucket='id:%s' % self._profile_id, limit=True)
        pprint.pprint(query)
        pprint.pprint(result)
        return models.SearchResult()

    def begin(self):
        start = 0
        while True:
            result = self._en.get('tasteprofile/read', id=self._profile_id,
                                 start=start, results=BATCH_SIZE)

            for item in result['catalog']['items']:
                timestamp = datetime.datetime.strptime(
                    item['last_modified'], TIMEFORMAT).strftime('%s')
                # TODO: should this be a full track instance?
                yield models.Track(uri=item['request']['url'],
                                   last_modified=timestamp)
            start += BATCH_SIZE
            if start > result['catalog']['total']:
                break

    def add(self, track):
        item = {'item_id': uri_to_item_id(track.uri), 'url': track.uri}

        # TODO: add fields that don't cleanly map to the key value fields
        item['song_name'] = track.name
        item['release'] = track.album.name
        item['genre'] = track.genre
        item['track_number'] = track.track_no
        item['disc_number'] = track.disc_no

        if track.musicbrainz_id:
            item['song_id'] = 'musicbrainz:song:%s' % track.musicbrainz_id

        if len(track.artists) == 1:
            artist_id = list(track.artists)[0].musicbrainz_id
            item['artist_id'] = 'musicbrainz:artist:%s' % artist_id
        else:
            item['artist_name'] = ', '.join(a.name for a in track.artists)

        for key in item.keys():
            if not item[key]:
                del item[key]

        self._items.append({'action': 'update', 'item': item})

    def remove(self, uri):
        item_id = uri_to_item_id(uri)
        self._items.append({'action': 'delete', 'item': {'item_id': item_id}})

    def flush(self):
        items, self._items = self._items, []
        pprint.pprint(items)
        result = self._en.post(
            'tasteprofile/update', id=self._profile_id, data=json.dumps(items))
        pprint.pprint(result)

    def close(self):
        self.flush()

    def clear(self):
        profile = self._en.get('tasteprofile/profile', name=TASTEPROFILE_NAME)
        pprint.pprint(profile)
        result = self._en.post('tasteprofile/delete', id=profile['catalog']['id'])
        pprint.pprint(result)
