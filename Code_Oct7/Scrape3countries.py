import time
import getpass
import requests
import pandas as pd

# ---------------------------------------------------------------
# Login: your Bluesky handle + an APP PASSWORD
# (Bluesky > Settings > Privacy and Security > App Passwords)
# ---------------------------------------------------------------
handle = 'nononononononononono.bsky.social'
app_password = 'nonononononononono'  

BASE = 'https://bsky.social/xrpc'

# ---------------------------------------------------------------
# Search terms per language, and time window
# ---------------------------------------------------------------
# Each language is searched with its own terms (singular and plural).
terms_by_lang = {
    'pt': ['eleição', 'eleições'],
    'en': ['midterm', 'midterm elections', 'midterm election'],
    'nl': ['verkiezing', 'verkiezingen'],
}

windows = {
    'campaign_2026': ('2025-03-01T00:00:00Z', '2026-09-30T00:00:00Z'),
}

MAX_PER_QUERY = 30000


# ---------------------------------------------------------------
# Session handling (tokens expire, so we refresh when needed)
# ---------------------------------------------------------------
def login():
    r = requests.post(f'{BASE}/com.atproto.server.createSession',
                      json={'identifier': handle, 'password': app_password})
    r.raise_for_status()
    return r.json()

session = login()
print('Logged in as:', session['handle'])


def refresh():
    global session
    r = requests.post(f'{BASE}/com.atproto.server.refreshSession',
                      headers={'Authorization': f"Bearer {session['refreshJwt']}"})
    if r.status_code == 200:
        session = r.json()
    else:
        session = login()
    print('Session refreshed.')


def search_page(q, since, until, lang, cursor=None):
    params = {'q': q, 'since': since, 'until': until,
              'sort': 'latest', 'limit': 100, 'lang': lang}
    if cursor:
        params['cursor'] = cursor

    for attempt in range(5):
        r = requests.get(f'{BASE}/app.bsky.feed.searchPosts', params=params,
                         headers={'Authorization': f"Bearer {session['accessJwt']}"})
        if r.status_code == 200:
            return r.json()
        if r.status_code in (400, 401) and 'ExpiredToken' in r.text:
            refresh()
            continue
        if r.status_code == 429:  # rate limit
            print('Rate limited, waiting 60 seconds...')
            time.sleep(60)
            continue
        print(f'Error {r.status_code}: {r.text}')
        return None
    return None


# ---------------------------------------------------------------
# Collect
# ---------------------------------------------------------------
data = []

for window_name, (since, until) in windows.items():
    for lang, terms in terms_by_lang.items():
        for q in terms:
            cursor, n = None, 0
            print(f'\n--- {window_name} | {lang} | {q} ---')
            while True:
                page = search_page(q, since, until, lang, cursor)
                if not page or not page.get('posts'):
                    break
                for p in page['posts']:
                    rec = p.get('record', {})
                    embed = p.get('embed', {}) or {}
                    link = (embed.get('external') or {}).get('uri')
                    has_image = 'images' in embed or 'media' in embed
                    data.append([
                        p['uri'],
                        rec.get('createdAt'),
                        p['author'].get('did'),
                        p['author'].get('handle'),
                        p['author'].get('displayName'),
                        rec.get('text'),
                        ','.join(rec.get('langs', []) or []),
                        p.get('likeCount', 0),
                        p.get('repostCount', 0),
                        p.get('replyCount', 0),
                        p.get('quoteCount', 0),
                        link,
                        has_image,
                        q,
                        lang,
                        window_name,
                    ])
                    n += 1
                    if n % 100 == 0:
                        print(f'Collected {n} posts so far...')
                cursor = page.get('cursor')
                if not cursor or n >= MAX_PER_QUERY:
                    break
                time.sleep(0.5)
            print(f'{lang} | {q}: {n} posts')

df = pd.DataFrame(data, columns=[
    'post_uri', 'date', 'author_did', 'author_handle', 'author_name', 'text',
    'langs', 'likes', 'reposts', 'replies', 'quotes', 'link', 'has_image',
    'query', 'search_lang', 'window'
])

# The same post can match several terms; keep one copy and record all terms
df = (df.groupby('post_uri', as_index=False)
        .agg({**{c: 'first' for c in df.columns if c not in ('post_uri', 'query')},
              'query': lambda s: ' | '.join(sorted(set(s)))}))

df.to_csv('bluesky_elections_pt_en_nl-march25_on.csv', index=False, encoding='utf-8-sig')
print(f'\nDone. Saved {len(df)} unique posts to bluesky_elections_pt_en_nl-march25_on.csv')
