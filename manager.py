#! python3

import sys

MIN_PY_VERSION = (3,10)
expected = '.'.join([str(i) for i in MIN_PY_VERSION])
was = '.'.join([str(i) for i in sys.version_info])
assert sys.version_info >= MIN_PY_VERSION, f'Python version {expected} required, but found {was}.'

# -

import time

VERBOSE = 0

BEGIN = time.time()
def print2(text, v=0):
   if VERBOSE >= v:
      print(f'[+{time.time() - BEGIN:.3f}s] {text}')

# -

from collections import namedtuple
import concurrent.futures
import io
import json
from pathlib import *
import re
import shutil
import subprocess
import sys
import time
import zipfile

# -
# Packages from pip

while True:
   try:
      import packaging.version
      import requests
      import urllib.parse
      break
   except ModuleNotFoundError as e:
      print2(e)
      subprocess.run("py -m pip  install  packaging requests urllib3", shell=True)
      continue

# -

ADDONS_DIR = Path.cwd()
if ADDONS_DIR.parts[-1] != 'AddOns':
    ADDONS_DIR = Path(__file__).parent.parent
assert ADDONS_DIR.parts[-1] == 'AddOns', f'Could not find "AddOns" folder at {ADDONS_DIR}!'

DUMP_REQUESTS = 0
MOCK_REQUESTS = False

# -

RE_TOC_KV = re.compile('## *([^:]+): *(.*)')

class TocKV:
   def __init__(self, line):
      m = RE_TOC_KV.match(line)
      self.k = m.group(1)
      self.v = m.group(2)

if True:
   g = RE_TOC_KV.match('## Version: v10.2.20').groups()
   assert g == ('Version', 'v10.2.20'), g


def kvs_from_toc_file(file):
   kvs = {}
   for line in file.read_text(encoding='utf8').split('\n'):
      line = line.strip()
      if line and line.startswith('## '):
         (k, v) = RE_TOC_KV.match(line).groups()
         kvs[k] = v

   return kvs

# -

if MOCK_REQUESTS:
   MOCK_REQUESTS = {}
   #MOCK_REQUESTS[''] = ''

   MOCK_REQUESTS['https://api.github.com/repos/WeakAuras/WeakAuras2/releases/latest'] = '''\
{
    "url": "https://api.github.com/repos/WeakAuras/WeakAuras2/releases/135736294",
    "assets_url": "https://api.github.com/repos/WeakAuras/WeakAuras2/releases/135736294/assets",
    "upload_url": "https://uploads.github.com/repos/WeakAuras/WeakAuras2/releases/135736294/assets{?name,label}",
    "html_url": "https://github.com/WeakAuras/WeakAuras2/releases/tag/5.9.0",
    "id": 135736294,
    "author": {
        "login": "github-actions[bot]",
        "id": 41898282,
        "node_id": "MDM6Qm90NDE4OTgyODI=",
        "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/github-actions%5Bbot%5D",
        "html_url": "https://github.com/apps/github-actions",
        "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
        "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
        "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
        "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
        "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
        "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
        "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
        "type": "Bot",
        "site_admin": false
    },
    "node_id": "RE_kwDOAX5T-M4IFyvm",
    "tag_name": "5.9.0",
    "target_commitish": "main",
    "name": "5.9.0",
    "draft": false,
    "prerelease": false,
    "created_at": "2024-01-03T20:13:42Z",
    "published_at": "2024-01-03T20:20:48Z",
    "assets": [{
        "url": "https://api.github.com/repos/WeakAuras/WeakAuras2/releases/assets/143627333",
        "id": 143627333,
        "node_id": "RA_kwDOAX5T-M4Ij5RF",
        "name": "release.json",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/json",
        "state": "uploaded",
        "size": 231,
        "download_count": 3046,
        "created_at": "2024-01-03T20:20:50Z",
        "updated_at": "2024-01-03T20:20:50Z",
        "browser_download_url": "https://github.com/WeakAuras/WeakAuras2/releases/download/5.9.0/release.json"
    }, {
        "url": "https://api.github.com/repos/WeakAuras/WeakAuras2/releases/assets/143627331",
        "id": 143627331,
        "node_id": "RA_kwDOAX5T-M4Ij5RD",
        "name": "WeakAuras-5.9.0.zip",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/zip",
        "state": "uploaded",
        "size": 8281915,
        "download_count": 30130,
        "created_at": "2024-01-03T20:20:49Z",
        "updated_at": "2024-01-03T20:20:50Z",
        "browser_download_url": "https://github.com/WeakAuras/WeakAuras2/releases/download/5.9.0/WeakAuras-5.9.0.zip"
    }],
    "tarball_url": "https://api.github.com/repos/WeakAuras/WeakAuras2/tarball/5.9.0",
    "zipball_url": "https://api.github.com/repos/WeakAuras/WeakAuras2/zipball/5.9.0",
    "body": "# [5.9.0](https://github.com/WeakAuras/WeakAuras2/tree/5.9.0) (2024-01-03)\\r\\n\\r\\n[Full Changelog](https://github.com/WeakAuras/WeakAuras2/compare/5.8.7...5.9.0)\\r\\n\\r\\n## Highlights\\r\\n\\r\\n - Add Currency Trigger\\r\\n- Enable receiving WA links in whispers from guild mates\\r\\n- Added Classic SoD Rune templates\\r\\n- Bug Fixes \\r\\n\\r\\n## Commits\\r\\n\\r\\nBoneshock (2):\\r\\n\\r\\n- fix %powertype show selected first then primary power type\\r\\n- Currency trigger: don't specify test on value block\\r\\n\\r\\nInfusOnWoW (19):\\r\\n\\r\\n- Classic Templates: Add missing race specific Priest spells\\r\\n- Fix KR/TW/CN large number formatting for >= 100.000.000\\r\\n- Classic: Remove LibClassicCasterino\\r\\n- Classic: Remove LibClassicDurations\\r\\n- Classic: Replace LibClassicSpellActionCount with GetSpellCount\\r\\n- Classic: Show warning that SAY/YELL are restricted too\\r\\n- Classic: Less special code in Combat Log Event trigger\\r\\n- Enable Modern Blizzard Time Formatting on Classic\\r\\n- BT2: Add a condition checking for caster's name/realm\\r\\n- Item Type trigger: Add Equipment Slot option\\r\\n- Remove unused table\\r\\n- Max Quantity: Fix enable check\\r\\n- BT2: Rename condition to less confussing name\\r\\n- BT: Remove left over code from old buff trigger\\r\\n- ApplyFrameLevel: Correctly handle auras without a subbackground\\r\\n- Make FixGroupChildrenOrderForGroup not recurse into subgroups\\r\\n- Options: Ignore newFeatureString for sorting\\r\\n- Reputation: Handle collapsed headers, and use DropDown with Headers\\r\\n- Currency Trigger: Fix collapsed currency headers\\r\\n\\r\\nJordi (2):\\r\\n\\r\\n- Currency Trigger: support classic wrath, disable on classic era (#4755)\\r\\n- Add Currency Trigger (#4672)\\r\\n\\r\\nNightwarden24 (5):\\r\\n\\r\\n- Fix texture search in texture picker Since texture names may contain characters that have special meaning when used in patterns, it's better to use the find function with plain text search enabled rather than the match function\\r\\n- Fix StopMotion thumbnail\\r\\n- Set region size to flipbook tile size\\r\\n- Make flipbook display proportional in texture picker\\r\\n- Add new flipbooks and correct some others\\r\\n\\r\\nRealityWinner (1):\\r\\n\\r\\n- Use spellIds in classic\\r\\n\\r\\nemptyrivers (1):\\r\\n\\r\\n- batch BAG_UPDATE_COOLDOWN events (#4756)\\r\\n\\r\\nmrbuds (16):\\r\\n\\r\\n- BossMod triggers: following a change in bigwigs, rename Key into ID BigWigs change: https://github.com/BigWigsMods/BigWigs/commit/9c65fd38132f38eacc341c0be4e430abacb1d19c\\r\\n- BossMod trigger: fix %message with bigwigs %text %name or %n worked, but tooltip advertise %message fixes #4785\\r\\n- Classic SoD priest runes template\\r\\n- Classic SoD rogue runes template\\r\\n- Classic SoD paladin runes template\\r\\n- add C_Seasons to luacheckrc\\r\\n- Classic SoD warrior runes template\\r\\n- Classic SoD shaman runes template\\r\\n- Classic SoD druid runes template\\r\\n- Classic SoD hunter runes template\\r\\n- Classic Sod warlock runes template\\r\\n- Classic SoD mage runes template\\r\\n- Cast trigger: drop leftoverinternal events for unused LibClassicCasterino\\r\\n- Classic Era CLEU extraSpellId is still stuck at 0\\r\\n- Classic: Fix softtarget units with aura trigger\\r\\n- Enable weakauras link received in whisper from guild mates\\r\\n\\r\\n",
    "reactions": {
        "url": "https://api.github.com/repos/WeakAuras/WeakAuras2/releases/135736294/reactions",
        "total_count": 2,
        "+1": 0,
        "-1": 0,
        "laugh": 0,
        "hooray": 0,
        "confused": 0,
        "heart": 2,
        "rocket": 0,
        "eyes": 0
    }
}'''

   MOCK_REQUESTS['https://api.github.com/repos/BigWigsMods/BigWigs/releases/latest'] = '''\
{
    "url": "https://api.github.com/repos/BigWigsMods/BigWigs/releases/136254060",
    "assets_url": "https://api.github.com/repos/BigWigsMods/BigWigs/releases/136254060/assets",
    "upload_url": "https://uploads.github.com/repos/BigWigsMods/BigWigs/releases/136254060/assets{?name,label}",
    "html_url": "https://github.com/BigWigsMods/BigWigs/releases/tag/v313.1",
    "id": 136254060,
    "author": {
        "login": "github-actions[bot]",
        "id": 41898282,
        "node_id": "MDM6Qm90NDE4OTgyODI=",
        "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/github-actions%5Bbot%5D",
        "html_url": "https://github.com/apps/github-actions",
        "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
        "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
        "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
        "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
        "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
        "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
        "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
        "type": "Bot",
        "site_admin": false
    },
    "node_id": "RE_kwDOA9q5Hs4IHxJs",
    "tag_name": "v313.1",
    "target_commitish": "master",
    "name": "v313.1",
    "draft": false,
    "prerelease": false,
    "created_at": "2024-01-08T23:16:41Z",
    "published_at": "2024-01-08T23:18:36Z",
    "assets": [{
        "url": "https://api.github.com/repos/BigWigsMods/BigWigs/releases/assets/144483646",
        "id": 144483646,
        "node_id": "RA_kwDOA9q5Hs4InKU-",
        "name": "BigWigs-v313.1.zip",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/zip",
        "state": "uploaded",
        "size": 4036910,
        "download_count": 264,
        "created_at": "2024-01-08T23:18:37Z",
        "updated_at": "2024-01-08T23:18:37Z",
        "browser_download_url": "https://github.com/BigWigsMods/BigWigs/releases/download/v313.1/BigWigs-v313.1.zip"
    }, {
        "url": "https://api.github.com/repos/BigWigsMods/BigWigs/releases/assets/144483650",
        "id": 144483650,
        "node_id": "RA_kwDOA9q5Hs4InKVC",
        "name": "release.json",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/json",
        "state": "uploaded",
        "size": 264,
        "download_count": 2834,
        "created_at": "2024-01-08T23:18:38Z",
        "updated_at": "2024-01-08T23:18:38Z",
        "browser_download_url": "https://github.com/BigWigsMods/BigWigs/releases/download/v313.1/release.json"
    }],
    "tarball_url": "https://api.github.com/repos/BigWigsMods/BigWigs/tarball/v313.1",
    "zipball_url": "https://api.github.com/repos/BigWigsMods/BigWigs/zipball/v313.1",
    "body": "# BigWigs\\r\\n\\r\\n## [v313.1](https://github.com/BigWigsMods/BigWigs/tree/v313.1) (2024-01-08)\\r\\n[Full Changelog](https://github.com/BigWigsMods/BigWigs/compare/v313...v313.1) [Previous Releases](https://github.com/BigWigsMods/BigWigs/releases)\\r\\n\\r\\n- Update ptBR (#1568)  \\r\\n- Loader: Add compat code for the C\\\\_AddOns API  \\r\\n"
}'''

   MOCK_REQUESTS['https://api.github.com/repos/BigWigsMods/LittleWigs/releases/latest'] = '''\
{
    "url": "https://api.github.com/repos/BigWigsMods/LittleWigs/releases/136212469",
    "assets_url": "https://api.github.com/repos/BigWigsMods/LittleWigs/releases/136212469/assets",
    "upload_url": "https://uploads.github.com/repos/BigWigsMods/LittleWigs/releases/136212469/assets{?name,label}",
    "html_url": "https://github.com/BigWigsMods/LittleWigs/releases/tag/v10.2.31",
    "id": 136212469,
    "author": {
        "login": "github-actions[bot]",
        "id": 41898282,
        "node_id": "MDM6Qm90NDE4OTgyODI=",
        "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/github-actions%5Bbot%5D",
        "html_url": "https://github.com/apps/github-actions",
        "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
        "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
        "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
        "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
        "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
        "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
        "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
        "type": "Bot",
        "site_admin": false
    },
    "node_id": "RE_kwDOA_Hh_84IHm_1",
    "tag_name": "v10.2.31",
    "target_commitish": "master",
    "name": "v10.2.31",
    "draft": false,
    "prerelease": false,
    "created_at": "2024-01-08T16:55:15Z",
    "published_at": "2024-01-08T16:58:41Z",
    "assets": [{
        "url": "https://api.github.com/repos/BigWigsMods/LittleWigs/releases/assets/144425464",
        "id": 144425464,
        "node_id": "RA_kwDOA_Hh_84Im8H4",
        "name": "LittleWigs-v10.2.31.zip",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/zip",
        "state": "uploaded",
        "size": 1504664,
        "download_count": 246,
        "created_at": "2024-01-08T16:58:41Z",
        "updated_at": "2024-01-08T16:58:42Z",
        "browser_download_url": "https://github.com/BigWigsMods/LittleWigs/releases/download/v10.2.31/LittleWigs-v10.2.31.zip"
    }, {
        "url": "https://api.github.com/repos/BigWigsMods/LittleWigs/releases/assets/144425469",
        "id": 144425469,
        "node_id": "RA_kwDOA_Hh_84Im8H9",
        "name": "release.json",
        "label": "",
        "uploader": {
            "login": "github-actions[bot]",
            "id": 41898282,
            "node_id": "MDM6Qm90NDE4OTgyODI=",
            "avatar_url": "https://avatars.githubusercontent.com/in/15368?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/github-actions%5Bbot%5D",
            "html_url": "https://github.com/apps/github-actions",
            "followers_url": "https://api.github.com/users/github-actions%5Bbot%5D/followers",
            "following_url": "https://api.github.com/users/github-actions%5Bbot%5D/following{/other_user}",
            "gists_url": "https://api.github.com/users/github-actions%5Bbot%5D/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/github-actions%5Bbot%5D/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/github-actions%5Bbot%5D/subscriptions",
            "organizations_url": "https://api.github.com/users/github-actions%5Bbot%5D/orgs",
            "repos_url": "https://api.github.com/users/github-actions%5Bbot%5D/repos",
            "events_url": "https://api.github.com/users/github-actions%5Bbot%5D/events{/privacy}",
            "received_events_url": "https://api.github.com/users/github-actions%5Bbot%5D/received_events",
            "type": "Bot",
            "site_admin": false
        },
        "content_type": "application/json",
        "state": "uploaded",
        "size": 274,
        "download_count": 2906,
        "created_at": "2024-01-08T16:58:42Z",
        "updated_at": "2024-01-08T16:58:43Z",
        "browser_download_url": "https://github.com/BigWigsMods/LittleWigs/releases/download/v10.2.31/release.json"
    }],
    "tarball_url": "https://api.github.com/repos/BigWigsMods/LittleWigs/tarball/v10.2.31",
    "zipball_url": "https://api.github.com/repos/BigWigsMods/LittleWigs/zipball/v10.2.31",
    "body": "# LittleWigs\\r\\n\\r\\n## [v10.2.31](https://github.com/BigWigsMods/LittleWigs/tree/v10.2.31) (2024-01-08)\\r\\n[Full Changelog](https://github.com/BigWigsMods/LittleWigs/compare/v10.2.30...v10.2.31) [Previous Releases](https://github.com/BigWigsMods/LittleWigs/releases)\\r\\n\\r\\n- Update zhTW (#987)  \\r\\n- Update zhCN (#986)  \\r\\n- Cataclysm/ThroneTides/Ozumat: Warmup bar  \\r\\n"
}'''

   # This was actually page=3, but pretend 1 and 2
   MOCK_REQUESTS['https://api.github.com/repos/Tercioo/Details-Damage-Meter/tags?per_page=100&page=1'] = '''\
[{
    "name": "DetailsRetail.8.3.0.7335.141",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7335.141",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7335.141",
    "commit": {
        "sha": "5384f5826bb311c1466e737736730cdae1312b01",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/5384f5826bb311c1466e737736730cdae1312b01"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMzUuMTQx"
}, {
    "name": "DetailsRetail.8.3.0.7334.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7334.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7334.140",
    "commit": {
        "sha": "2ccc88cf31796e95dba0647b63479a7ec22a51c9",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/2ccc88cf31796e95dba0647b63479a7ec22a51c9"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMzQuMTQw"
}]'''

   MOCK_REQUESTS['https://api.github.com/repos/Tercioo/Details-Damage-Meter/tags?per_page=100&page=2'] = '''\
[{
    "name": "DetailsRetail.8.3.0.7330.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7330.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7330.140",
    "commit": {
        "sha": "646732e0a6bcbcbde4a5969a85ddd1be5d2bad41",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/646732e0a6bcbcbde4a5969a85ddd1be5d2bad41"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMzAuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7329.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7329.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7329.140",
    "commit": {
        "sha": "79c86f99455fa7ec90254668f57c80cf0c12ff01",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/79c86f99455fa7ec90254668f57c80cf0c12ff01"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMjkuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7325.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7325.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7325.140",
    "commit": {
        "sha": "8350ea2054d861fd1299c903a9c333d6092b4123",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8350ea2054d861fd1299c903a9c333d6092b4123"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMjUuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7303.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7303.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7303.140",
    "commit": {
        "sha": "2149413da3e8b6884bd7cde1cd95da11e34fbecb",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/2149413da3e8b6884bd7cde1cd95da11e34fbecb"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjczMDMuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7282.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7282.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7282.140",
    "commit": {
        "sha": "149986e6cc374a575ae3fc49813a2d6b9122aa16",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/149986e6cc374a575ae3fc49813a2d6b9122aa16"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyODIuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7281.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7281.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7281.140",
    "commit": {
        "sha": "3d7f299207ddcef3f3ab6ba0c47d71eab0e326e1",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/3d7f299207ddcef3f3ab6ba0c47d71eab0e326e1"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyODEuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7269.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7269.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7269.140",
    "commit": {
        "sha": "bcdd7ae6831b6d4f3436e70f4aad288cae059304",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/bcdd7ae6831b6d4f3436e70f4aad288cae059304"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyNjkuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7259.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7259.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7259.140",
    "commit": {
        "sha": "2519ea0b9668ef9680be43f59cb83b6eb5bf6bfa",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/2519ea0b9668ef9680be43f59cb83b6eb5bf6bfa"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyNTkuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7255.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7255.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7255.140",
    "commit": {
        "sha": "6161cc451722a6f780b676cd72b0914dbeea1e7d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/6161cc451722a6f780b676cd72b0914dbeea1e7d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyNTUuMTQw"
}, {
    "name": "DetailsRetail.8.3.0.7246.140",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.8.3.0.7246.140",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.8.3.0.7246.140",
    "commit": {
        "sha": "baf7d2f3b2111e398402995bb544cc8bb71e824d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/baf7d2f3b2111e398402995bb544cc8bb71e824d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLjguMy4wLjcyNDYuMTQw"
}, {
    "name": "DetailsRetail.v9.2.7.10018.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10018.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10018.146",
    "commit": {
        "sha": "27ca0d6df73caa348f61ca1e3b95c7e33a050e31",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/27ca0d6df73caa348f61ca1e3b95c7e33a050e31"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAxOC4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10017.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10017.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10017.146",
    "commit": {
        "sha": "bd433b8319de78531ef324ce30b176447fed9946",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/bd433b8319de78531ef324ce30b176447fed9946"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAxNy4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10015.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10015.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10015.146",
    "commit": {
        "sha": "09845aa96d9895aeda2c6c330d60934cf637dcd6",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/09845aa96d9895aeda2c6c330d60934cf637dcd6"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAxNS4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10010.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10010.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10010.146",
    "commit": {
        "sha": "cd1492ab40745b2428e381280017a198eb1c5329",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/cd1492ab40745b2428e381280017a198eb1c5329"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAxMC4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10008.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10008.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10008.146",
    "commit": {
        "sha": "62c06ffe2bc76b4a531b600e9aff2144b1cc432d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/62c06ffe2bc76b4a531b600e9aff2144b1cc432d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAwOC4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10001.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10001.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10001.146",
    "commit": {
        "sha": "ab2d87b27e4a9e9eefbc7eccd498a1a798dd48a1",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/ab2d87b27e4a9e9eefbc7eccd498a1a798dd48a1"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAwMS4xNDY="
}, {
    "name": "DetailsRetail.v9.2.7.10000.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.7.10000.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.7.10000.146",
    "commit": {
        "sha": "af8c94f7ff2a1238a490da61e82bd57f8d97760b",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/af8c94f7ff2a1238a490da61e82bd57f8d97760b"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuNy4xMDAwMC4xNDY="
}, {
    "name": "DetailsRetail.v9.2.0.9694.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.2.0.9694.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.2.0.9694.146",
    "commit": {
        "sha": "27f69675caec0c1ad11d38c15425e7f8aa556122",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/27f69675caec0c1ad11d38c15425e7f8aa556122"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjIuMC45Njk0LjE0Ng=="
}, {
    "name": "DetailsRetail.v9.1.5.9693.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.5.9693.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.5.9693.146",
    "commit": {
        "sha": "8594fbb85406dbf0113c15af39a34ee6efd45dd2",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8594fbb85406dbf0113c15af39a34ee6efd45dd2"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuNS45NjkzLjE0Ng=="
}, {
    "name": "DetailsRetail.v9.1.5.9692.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.5.9692.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.5.9692.146",
    "commit": {
        "sha": "338174631422e0c6cbc2919d31017f5a4e7c0b4d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/338174631422e0c6cbc2919d31017f5a4e7c0b4d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuNS45NjkyLjE0Ng=="
}, {
    "name": "DetailsRetail.v9.1.5.9688.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.5.9688.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.5.9688.146",
    "commit": {
        "sha": "1850624374c96cb4a70c16dc919247725e651d97",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/1850624374c96cb4a70c16dc919247725e651d97"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuNS45Njg4LjE0Ng=="
}, {
    "name": "DetailsRetail.v9.1.0.8889.145",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.0.8889.145",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.0.8889.145",
    "commit": {
        "sha": "12d31f2b2923313e6629816e840829651e851b1d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/12d31f2b2923313e6629816e840829651e851b1d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuMC44ODg5LjE0NQ=="
}, {
    "name": "DetailsRetail.v9.1.0.8888.145",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.0.8888.145",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.0.8888.145",
    "commit": {
        "sha": "9e25e245d4ac35c87dcbdd7ad798430f8b105afe",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/9e25e245d4ac35c87dcbdd7ad798430f8b105afe"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuMC44ODg4LjE0NQ=="
}, {
    "name": "DetailsRetail.v9.1.0.8888a.145",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/DetailsRetail.v9.1.0.8888a.145",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/DetailsRetail.v9.1.0.8888a.145",
    "commit": {
        "sha": "d6964804f0566b36fe69e01a629cb81f740e56a4",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/d6964804f0566b36fe69e01a629cb81f740e56a4"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzUmV0YWlsLnY5LjEuMC44ODg4YS4xNDU="
}, {
    "name": "Details.20231229.12197.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231229.12197.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231229.12197.155",
    "commit": {
        "sha": "64675e2f71749a99c5ba69e7449c7a7c7204ac13",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/64675e2f71749a99c5ba69e7449c7a7c7204ac13"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjI5LjEyMTk3LjE1NQ=="
}, {
    "name": "Details.20231228.12190.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231228.12190.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231228.12190.155",
    "commit": {
        "sha": "a094f4364504ece809234e21ce85240115b70415",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/a094f4364504ece809234e21ce85240115b70415"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjI4LjEyMTkwLjE1NQ=="
}, {
    "name": "Details.20231228.12188.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231228.12188.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231228.12188.155",
    "commit": {
        "sha": "d789c8ded9ea23292247084679e7453c552052d1",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/d789c8ded9ea23292247084679e7453c552052d1"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjI4LjEyMTg4LjE1NQ=="
}, {
    "name": "Details.20231219.12111.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231219.12111.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231219.12111.155",
    "commit": {
        "sha": "0bd0343034a65aaa3f96debe50733704d1a9ed22",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/0bd0343034a65aaa3f96debe50733704d1a9ed22"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjE5LjEyMTExLjE1NQ=="
}, {
    "name": "Details.20231214.12109.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231214.12109.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231214.12109.155",
    "commit": {
        "sha": "18303599439a9ed2d78b5f01bea1b88be8d546c9",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/18303599439a9ed2d78b5f01bea1b88be8d546c9"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjE0LjEyMTA5LjE1NQ=="
}, {
    "name": "Details.20231201.12097.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231201.12097.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231201.12097.155",
    "commit": {
        "sha": "74f987ab95c8bb2eb569ca0dba59baed604e3867",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/74f987ab95c8bb2eb569ca0dba59baed604e3867"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjAxLjEyMDk3LjE1NQ=="
}, {
    "name": "Details.20231201.12096.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231201.12096.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231201.12096.155",
    "commit": {
        "sha": "19562de6d226b36b4b775c5fcbbdc0acc09bcaf1",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/19562de6d226b36b4b775c5fcbbdc0acc09bcaf1"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMjAxLjEyMDk2LjE1NQ=="
}, {
    "name": "Details.20231120.12044.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231120.12044.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231120.12044.155",
    "commit": {
        "sha": "22483cb77cd8b845fb135078f13c801c5e1949a2",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/22483cb77cd8b845fb135078f13c801c5e1949a2"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTIwLjEyMDQ0LjE1NQ=="
}, {
    "name": "Details.20231114.12043.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231114.12043.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231114.12043.155",
    "commit": {
        "sha": "e4140664ed80f16a3796e6184ec57037cc81726d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/e4140664ed80f16a3796e6184ec57037cc81726d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTE0LjEyMDQzLjE1NQ=="
}, {
    "name": "Details.20231114.12042.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231114.12042.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231114.12042.155",
    "commit": {
        "sha": "448a31671b4ef32f29e6e9e275b733f6c4aaafe1",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/448a31671b4ef32f29e6e9e275b733f6c4aaafe1"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTE0LjEyMDQyLjE1NQ=="
}, {
    "name": "Details.20231114.12041.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231114.12041.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231114.12041.155",
    "commit": {
        "sha": "cf80fe5182bb839fe54404bf0ed4b0c70cb11144",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/cf80fe5182bb839fe54404bf0ed4b0c70cb11144"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTE0LjEyMDQxLjE1NQ=="
}, {
    "name": "Details.20231114.12040.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231114.12040.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231114.12040.155",
    "commit": {
        "sha": "e721a070684981941eddd047fcf3b0b4e63b51e9",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/e721a070684981941eddd047fcf3b0b4e63b51e9"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTE0LjEyMDQwLjE1NQ=="
}, {
    "name": "Details.20231113.12039.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231113.12039.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231113.12039.155",
    "commit": {
        "sha": "4b7463a307d88c0fa4fd04668299fc106fe0d114",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/4b7463a307d88c0fa4fd04668299fc106fe0d114"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEzLjEyMDM5LjE1NQ=="
}, {
    "name": "Details.20231112.12038.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231112.12038.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231112.12038.155",
    "commit": {
        "sha": "ed489fcb6b9842088fb43df371a71c5f4863c34e",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/ed489fcb6b9842088fb43df371a71c5f4863c34e"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEyLjEyMDM4LjE1NQ=="
}, {
    "name": "Details.20231112.12037.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231112.12037.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231112.12037.155",
    "commit": {
        "sha": "29427009e58491a1d09f4bc4146c40065a7f42f3",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/29427009e58491a1d09f4bc4146c40065a7f42f3"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEyLjEyMDM3LjE1NQ=="
}, {
    "name": "Details.20231112.12036.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231112.12036.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231112.12036.155",
    "commit": {
        "sha": "7e7dda8ee74a17bb92bc46af84e65e0036fc3366",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/7e7dda8ee74a17bb92bc46af84e65e0036fc3366"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEyLjEyMDM2LjE1NQ=="
}, {
    "name": "Details.20231112.12034.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231112.12034.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231112.12034.155",
    "commit": {
        "sha": "ba7d2c2c2dd052ee69ca718812428dac4bae058c",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/ba7d2c2c2dd052ee69ca718812428dac4bae058c"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEyLjEyMDM0LjE1NQ=="
}, {
    "name": "Details.20231111.12033.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231111.12033.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231111.12033.155",
    "commit": {
        "sha": "8fc05069b1f44e202437cd82f19c37b34365f5a7",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8fc05069b1f44e202437cd82f19c37b34365f5a7"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTExLjEyMDMzLjE1NQ=="
}, {
    "name": "Details.20231110.12032.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231110.12032.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231110.12032.155",
    "commit": {
        "sha": "daaa3a7f1f9ae9a27f9cba53492f25f0265d9f2b",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/daaa3a7f1f9ae9a27f9cba53492f25f0265d9f2b"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEwLjEyMDMyLjE1NQ=="
}, {
    "name": "Details.20231110.12031.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231110.12031.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231110.12031.155",
    "commit": {
        "sha": "7a5529d4e4a606949d3cafb71dcea992e7f6c5c0",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/7a5529d4e4a606949d3cafb71dcea992e7f6c5c0"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEwLjEyMDMxLjE1NQ=="
}, {
    "name": "Details.20231110.12030.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231110.12030.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231110.12030.155",
    "commit": {
        "sha": "d95ff2b827e8b4cbcf8b115519941b3bebe2d792",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/d95ff2b827e8b4cbcf8b115519941b3bebe2d792"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEwLjEyMDMwLjE1NQ=="
}, {
    "name": "Details.20231110.12029.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231110.12029.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231110.12029.155",
    "commit": {
        "sha": "60819b914323b5d2d0c1df4bd068709a12408daf",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/60819b914323b5d2d0c1df4bd068709a12408daf"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTEwLjEyMDI5LjE1NQ=="
}, {
    "name": "Details.20231109.12028.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231109.12028.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231109.12028.155",
    "commit": {
        "sha": "89b84ced684bc0db479bf992bd80111abd28d028",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/89b84ced684bc0db479bf992bd80111abd28d028"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA5LjEyMDI4LjE1NQ=="
}, {
    "name": "Details.20231109.12027.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231109.12027.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231109.12027.155",
    "commit": {
        "sha": "8b026db68bf281150bb4304f9a4e35f254e86bad",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8b026db68bf281150bb4304f9a4e35f254e86bad"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA5LjEyMDI3LjE1NQ=="
}, {
    "name": "Details.20231108.12026.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231108.12026.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231108.12026.155",
    "commit": {
        "sha": "5e7df0d94af57c1dce367cf1ed2d8b6617734295",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/5e7df0d94af57c1dce367cf1ed2d8b6617734295"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA4LjEyMDI2LjE1NQ=="
}, {
    "name": "Details.20231108.12025.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231108.12025.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231108.12025.155",
    "commit": {
        "sha": "3b2ba40b29f69a219ead741ebe35e358cc0a9488",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/3b2ba40b29f69a219ead741ebe35e358cc0a9488"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA4LjEyMDI1LjE1NQ=="
}, {
    "name": "Details.20231108.12024.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231108.12024.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231108.12024.155",
    "commit": {
        "sha": "dd13aff9616ffa673ca24455ed57931d67a45dc4",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/dd13aff9616ffa673ca24455ed57931d67a45dc4"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA4LjEyMDI0LjE1NQ=="
}, {
    "name": "Details.20231108.12023.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231108.12023.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231108.12023.155",
    "commit": {
        "sha": "57535baddfee16dd87747b6cc45c70a052eac425",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/57535baddfee16dd87747b6cc45c70a052eac425"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTA4LjEyMDIzLjE1NQ=="
}, {
    "name": "Details.20231102.12020.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231102.12020.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231102.12020.155",
    "commit": {
        "sha": "d11f8a1ccd59b36f74dfc40e65a5960289dd0e69",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/d11f8a1ccd59b36f74dfc40e65a5960289dd0e69"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMTAyLjEyMDIwLjE1NQ=="
}, {
    "name": "Details.20231029.12019.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231029.12019.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231029.12019.155",
    "commit": {
        "sha": "21f30af11fd59edd75a85d4c9dbab636f8752a7f",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/21f30af11fd59edd75a85d4c9dbab636f8752a7f"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMDI5LjEyMDE5LjE1NQ=="
}, {
    "name": "Details.20231028.12018.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231028.12018.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231028.12018.155",
    "commit": {
        "sha": "718cd9b93b579f1d47ceab6581431b9146216023",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/718cd9b93b579f1d47ceab6581431b9146216023"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMDI4LjEyMDE4LjE1NQ=="
}, {
    "name": "Details.20231027.12012.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20231027.12012.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20231027.12012.155",
    "commit": {
        "sha": "966e0c3a995289b0951103bf7619d6b880c84886",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/966e0c3a995289b0951103bf7619d6b880c84886"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMxMDI3LjEyMDEyLjE1NQ=="
}, {
    "name": "Details.20230913.11914.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230913.11914.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230913.11914.155",
    "commit": {
        "sha": "4d9a0d5a029b3c3ab6b1903b50e37d8b3f865101",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/4d9a0d5a029b3c3ab6b1903b50e37d8b3f865101"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwOTEzLjExOTE0LjE1NQ=="
}, {
    "name": "Details.20230909.11902.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230909.11902.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230909.11902.155",
    "commit": {
        "sha": "3adadfe17ab1d2d197ab7a090ffdebc941dd8271",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/3adadfe17ab1d2d197ab7a090ffdebc941dd8271"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwOTA5LjExOTAyLjE1NQ=="
}, {
    "name": "Details.20230909.11901.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230909.11901.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230909.11901.155",
    "commit": {
        "sha": "f27d73d562289e9a1b311cdcd66eeb0e1d06fb4e",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/f27d73d562289e9a1b311cdcd66eeb0e1d06fb4e"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwOTA5LjExOTAxLjE1NQ=="
}, {
    "name": "Details.20230825.11857.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230825.11857.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230825.11857.155",
    "commit": {
        "sha": "5cef044c5c29187b159beab818d8d0ca4c31f383",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/5cef044c5c29187b159beab818d8d0ca4c31f383"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwODI1LjExODU3LjE1NQ=="
}, {
    "name": "Details.20230813.11856.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230813.11856.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230813.11856.155",
    "commit": {
        "sha": "4ae7c24268b198efdfe61650b78073c6d35d240d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/4ae7c24268b198efdfe61650b78073c6d35d240d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwODEzLjExODU2LjE1NQ=="
}, {
    "name": "Details.20230812.11855.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230812.11855.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230812.11855.155",
    "commit": {
        "sha": "0b32fe3459b1fe96dafc1a9943230ac07111e9ea",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/0b32fe3459b1fe96dafc1a9943230ac07111e9ea"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwODEyLjExODU1LjE1NQ=="
}, {
    "name": "Details.20230731.11774.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230731.11774.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230731.11774.155",
    "commit": {
        "sha": "080c63f584149d1333cb81a6a03699abb8db68aa",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/080c63f584149d1333cb81a6a03699abb8db68aa"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzMxLjExNzc0LjE1NQ=="
}, {
    "name": "Details.20230730.11773.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230730.11773.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230730.11773.155",
    "commit": {
        "sha": "104fd7398a34751b8f8f622bdc7074b63b32b83a",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/104fd7398a34751b8f8f622bdc7074b63b32b83a"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzMwLjExNzczLjE1NQ=="
}, {
    "name": "Details.20230729.11770.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230729.11770.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230729.11770.155",
    "commit": {
        "sha": "89e6ffd8afaa91dd928678a0fd48cb998f89c56f",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/89e6ffd8afaa91dd928678a0fd48cb998f89c56f"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzI5LjExNzcwLjE1NQ=="
}, {
    "name": "Details.20230720.11718.155",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230720.11718.155",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230720.11718.155",
    "commit": {
        "sha": "ae490f434db0ea38e984a33aaeba74ebb0875c60",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/ae490f434db0ea38e984a33aaeba74ebb0875c60"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzIwLjExNzE4LjE1NQ=="
}, {
    "name": "Details.20230713.11701.154",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230713.11701.154",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230713.11701.154",
    "commit": {
        "sha": "e2e2369a81f7100f0eaa7fd8fd81d780b77cacf9",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/e2e2369a81f7100f0eaa7fd8fd81d780b77cacf9"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzEzLjExNzAxLjE1NA=="
}, {
    "name": "Details.20230713.11700.154",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230713.11700.154",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230713.11700.154",
    "commit": {
        "sha": "7a0e045308af60c622645c6b092b23743f4c8e0b",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/7a0e045308af60c622645c6b092b23743f4c8e0b"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNzEzLjExNzAwLjE1NA=="
}, {
    "name": "Details.20230520.11023.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230520.11023.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230520.11023.151",
    "commit": {
        "sha": "a20a4737db5fa91a352cedcb7e7d1523807c6fc5",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/a20a4737db5fa91a352cedcb7e7d1523807c6fc5"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTIwLjExMDIzLjE1MQ=="
}, {
    "name": "Details.20230520.11022.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230520.11022.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230520.11022.151",
    "commit": {
        "sha": "64a7053089bfdfbb651434e4bd94bf8b065422f5",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/64a7053089bfdfbb651434e4bd94bf8b065422f5"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTIwLjExMDIyLjE1MQ=="
}, {
    "name": "Details.20230513.11011.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230513.11011.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230513.11011.151",
    "commit": {
        "sha": "907d88fad5e5a2e6cc9f37e811eb6ce541f042d8",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/907d88fad5e5a2e6cc9f37e811eb6ce541f042d8"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTEzLjExMDExLjE1MQ=="
}, {
    "name": "Details.20230512.11010.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230512.11010.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230512.11010.151",
    "commit": {
        "sha": "21da70e1587fc9b5f7a8c50ecea1a4675f63279e",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/21da70e1587fc9b5f7a8c50ecea1a4675f63279e"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTEyLjExMDEwLjE1MQ=="
}, {
    "name": "Details.20230511.11004.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230511.11004.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230511.11004.151",
    "commit": {
        "sha": "bad49954517607dce145d94c9417c4e92a4492f8",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/bad49954517607dce145d94c9417c4e92a4492f8"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTExLjExMDA0LjE1MQ=="
}, {
    "name": "Details.20230509.11001.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230509.11001.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230509.11001.151",
    "commit": {
        "sha": "b78b35e557bf56cdf9f5ec317252b826d648749c",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/b78b35e557bf56cdf9f5ec317252b826d648749c"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTA5LjExMDAxLjE1MQ=="
}, {
    "name": "Details.20230509.11000.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230509.11000.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230509.11000.151",
    "commit": {
        "sha": "a54e80c47548f329fe3e7552bcff775787c771a8",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/a54e80c47548f329fe3e7552bcff775787c771a8"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTA5LjExMDAwLjE1MQ=="
}, {
    "name": "Details.20230507.10993.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230507.10993.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230507.10993.151",
    "commit": {
        "sha": "57aa3d2ae3b8efb4985b83b8d1aff8437678b2d0",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/57aa3d2ae3b8efb4985b83b8d1aff8437678b2d0"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTA3LjEwOTkzLjE1MQ=="
}, {
    "name": "Details.20230507.10990.151",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.20230507.10990.151",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.20230507.10990.151",
    "commit": {
        "sha": "cb5dc42db8f630b4a45fa5362e11837c79b99475",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/cb5dc42db8f630b4a45fa5362e11837c79b99475"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLjIwMjMwNTA3LjEwOTkwLjE1MQ=="
}, {
    "name": "Details.Wrath.SL.DF.10030.146",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.Wrath.SL.DF.10030.146",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.Wrath.SL.DF.10030.146",
    "commit": {
        "sha": "2432bc6919cfddaf314003b8d21c9efe6dd6fe71",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/2432bc6919cfddaf314003b8d21c9efe6dd6fe71"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLldyYXRoLlNMLkRGLjEwMDMwLjE0Ng=="
}, {
    "name": "Details.DF.Wrath.10562.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10562.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10562.148",
    "commit": {
        "sha": "93dd3e2a279799085de031fc4fb11be2ee17760a",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/93dd3e2a279799085de031fc4fb11be2ee17760a"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNTYyLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10561.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10561.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10561.148",
    "commit": {
        "sha": "eac488a4001cdf0d99b941197e6a12b27a38c1b3",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/eac488a4001cdf0d99b941197e6a12b27a38c1b3"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNTYxLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10410.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10410.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10410.148",
    "commit": {
        "sha": "e9f9adab230b98cd7269157b5100b0448bf82129",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/e9f9adab230b98cd7269157b5100b0448bf82129"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDEwLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10409.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10409.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10409.148",
    "commit": {
        "sha": "597dac46992bd96c1876af6f01dbdc080c980ac6",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/597dac46992bd96c1876af6f01dbdc080c980ac6"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA5LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10408.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10408.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10408.148",
    "commit": {
        "sha": "72558971345bca3d979c75ce33a386d4638a7ac3",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/72558971345bca3d979c75ce33a386d4638a7ac3"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA4LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10407.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10407.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10407.148",
    "commit": {
        "sha": "802516539897958cb38f8f742eb1afcbe1c72713",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/802516539897958cb38f8f742eb1afcbe1c72713"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA3LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10406.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10406.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10406.148",
    "commit": {
        "sha": "764b7798136332c966b68203f44f7d5d5cccfe72",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/764b7798136332c966b68203f44f7d5d5cccfe72"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA2LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10405.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10405.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10405.148",
    "commit": {
        "sha": "9ca2636db4085b223b1a073a2e1f807b74219d11",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/9ca2636db4085b223b1a073a2e1f807b74219d11"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA1LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10404.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10404.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10404.148",
    "commit": {
        "sha": "3ac60e3e29263671ec750e4c5882bb9e0ce81e5a",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/3ac60e3e29263671ec750e4c5882bb9e0ce81e5a"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDA0LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10403.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10403.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10403.148",
    "commit": {
        "sha": "77f8e7cab3e768b903627cb8aa05f6cbcb2dfadb",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/77f8e7cab3e768b903627cb8aa05f6cbcb2dfadb"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDAzLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10402.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10402.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10402.148",
    "commit": {
        "sha": "30c41429b111c82271658930d1514cfb9caeefcb",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/30c41429b111c82271658930d1514cfb9caeefcb"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDAyLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10401.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10401.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10401.148",
    "commit": {
        "sha": "ee6d89e6a257dfebb68f3b1b772ac2788302209a",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/ee6d89e6a257dfebb68f3b1b772ac2788302209a"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwNDAxLjE0OA=="
}, {
    "name": "Details.DF.Wrath.10337.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10337.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10337.148",
    "commit": {
        "sha": "8d93d677ca54f67ec87aeb9922525a5e9344b146",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8d93d677ca54f67ec87aeb9922525a5e9344b146"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzM3LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10336.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10336.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10336.148",
    "commit": {
        "sha": "388154a5408f10b5c7ffc0f2fa4b874a700b23e8",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/388154a5408f10b5c7ffc0f2fa4b874a700b23e8"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzM2LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10335.148",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10335.148",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10335.148",
    "commit": {
        "sha": "3f298dcc7707577656f1e1e37cdca2660717ba3c",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/3f298dcc7707577656f1e1e37cdca2660717ba3c"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzM1LjE0OA=="
}, {
    "name": "Details.DF.Wrath.10334.147",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10334.147",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10334.147",
    "commit": {
        "sha": "6609580f092bdb80f665c079409d98b66eb32ca3",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/6609580f092bdb80f665c079409d98b66eb32ca3"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzM0LjE0Nw=="
}, {
    "name": "Details.DF.Wrath.10333.147",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10333.147",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10333.147",
    "commit": {
        "sha": "fd25f6e75318803351904935e142d376c9103d08",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/fd25f6e75318803351904935e142d376c9103d08"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzMzLjE0Nw=="
}, {
    "name": "Details.DF.Wrath.10304.147",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10304.147",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10304.147",
    "commit": {
        "sha": "4b3237f809684fd51fd5f5e3cef427c1fb34ba3d",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/4b3237f809684fd51fd5f5e3cef427c1fb34ba3d"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzA0LjE0Nw=="
}, {
    "name": "Details.DF.Wrath.10302.147",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10302.147",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10302.147",
    "commit": {
        "sha": "8f6cfe4d69065c33ff0610d7777faddfe1ffc4b7",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/8f6cfe4d69065c33ff0610d7777faddfe1ffc4b7"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzAyLjE0Nw=="
}, {
    "name": "Details.DF.Wrath.10301.147",
    "zipball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/zipball/refs/tags/Details.DF.Wrath.10301.147",
    "tarball_url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/tarball/refs/tags/Details.DF.Wrath.10301.147",
    "commit": {
        "sha": "eb60b77c323ad2705da088b3ad6c69bb2b7ed0a5",
        "url": "https://api.github.com/repos/Tercioo/Details-Damage-Meter/commits/eb60b77c323ad2705da088b3ad6c69bb2b7ed0a5"
    },
    "node_id": "MDM6UmVmMTc5NTA1NzU5OnJlZnMvdGFncy9EZXRhaWxzLkRGLldyYXRoLjEwMzAxLjE0Nw=="
}]'''

   # This was actually page=5, but pretend 3.
   MOCK_REQUESTS['https://api.github.com/repos/Tercioo/Details-Damage-Meter/tags?per_page=100&page=3'] = '''\
[]'''


# -

class ExButNotVerbose(Exception):
   pass

def request_json(url):
   def fetch():
      global DUMP_REQUESTS
      with requests.get(url) as r:
         r.raise_for_status()
         j = r.json()
         if DUMP_REQUESTS:
            DUMP_REQUESTS -= 1
            t = r.text
            t = t.replace('\\', '\\\\')
            lines = [
               f'[DUMP_REQUESTS] url: {url}',
               "'''",
               t,
               "'''",
            ]
            print2('\n'.join(lines))
      return j


   if MOCK_REQUESTS:
      try:
         text = MOCK_REQUESTS[url]
      except KeyError:
         if DUMP_REQUESTS:
            return fetch()
         raise

      text = text.replace('\r\n', '\n')
      j = json.loads(text)
      return j

   return fetch()


# -

class AddonAssetInfo:
   def __init__(self, version, download_url):
      self.set_version(version)
      self.download_url = download_url

      parsed_url = urllib.parse.urlparse(download_url)
      url_path = parsed_url.path
      self.download_name = PurePath(url_path).name

   def set_version(self, version):
      version = lstrip_non_digits(version)
      self.version = packaging.version.parse(version)


def lstrip_non_digits(version):
   while version and not version[0].isdigit():
      version = version[1:]
   return version


def parse_version__default(version):
   version = lstrip_non_digits(version)
   return packaging.version.parse(version)

def filter_likely_assets__default(likely_assets):
   likely_assets = [a for a in likely_assets if a.download_name.startswith(self.name)]
   likely_assets = [a for a in likely_assets if a.download_name.endswith('.zip')]
   return likely_assets

class Addon:
   def __init__(self, name, fn_query_latest_asset, fn_install):
      self.name = name
      self.fn_query_latest_asset = fn_query_latest_asset
      self.fn_install = fn_install
      self.fn_parse_version = parse_version__default
      self.fn_asset_version_from_download_name = None


   def print(self, text, **kwargs):
      print2(f'[{self.name}] {text}', **kwargs)


   def get_installed_version(self):
      addon_dir = ADDONS_DIR / self.name
      if not addon_dir.exists():
         return None
      toc = addon_dir / f'{self.name}.toc'
      assert toc.exists(), toc


      self.print(f'Reading version from {toc}', v=1)
      kvs = kvs_from_toc_file(toc)

      version = kvs['Version']
      version = self.fn_parse_version(version)
      return version


   def request_json(self, req_url):
      try:
         return request_json(req_url)
      except requests.exceptions.HTTPError as e:
         if not VERBOSE:
            self.print(f'!!! FAILED: {e}')
            raise ExButNotVerbose()
         raise


   def query_latest_asset(self):
      asset = self.fn_query_latest_asset(self)
      if self.fn_asset_version_from_download_name:
         version = self.fn_asset_version_from_download_name(asset.download_name)
         asset.set_version(version)
      return asset


   def github_latest_release(self, repo):
      req_url = f'https://api.github.com/repos/{repo}/releases/latest'
      self.print(f'Checking releases via {req_url}', v=1)
      release = self.request_json(req_url)

      assets = [AddonAssetInfo(release['name'], a['browser_download_url']) for a in release['assets']]

      def asset_filter(asset):
         if not asset.download_name.lower().startswith(self.name.lower()):
            return False
         if not asset.download_name.endswith('.zip'):
            return False
         for unlikely in ['-bc.zip', '-classic.zip', '-wrath.zip']:
            if asset.download_name.endswith(unlikely):
               return False
         return True

      likely_assets = [a for a in assets if asset_filter(a)]
      assert len(likely_assets) == 1, (self.name, [a.download_name for a in likely_assets], [a.download_name for a in assets], req_url)
      return likely_assets[0]


   def github_latest_tag(self, repo):
      raw_tags = []
      page = 0
      while True:
         page += 1
         assert page <= 10, page
         req_url = f'https://api.github.com/repos/{repo}/tags?per_page=100&page={page}'
         self.print(f'Checking tags via {req_url}', v=1)
         page_tags = self.request_json(req_url)
         if len(page_tags) == 0:
            page -= 1
            break
         raw_tags += page_tags

      self.print(f'Sorting {len(raw_tags)} tags from {page} pages', v=1)
      assets = []
      for x in raw_tags:
         try:
            a = AddonAssetInfo(x['name'], x['zipball_url'])
         except packaging.version.InvalidVersion:
            name = x['name'] # Python 3.10
            self.print(f'(Warning: Tag not parseable as version: "{name}")', v=2)
            continue
         assets.append(a)
      assets = sorted(assets, key=lambda t: t.version)
      latest_asset = assets[-1]
      return latest_asset

   # -

   def install_from_asset(self, asset, extract_to=ADDONS_DIR):
      self.print(f'(Downloading {asset.download_url})')
      with requests.get(asset.download_url) as res:
         b = res.content

      self.print(f'(Extracting {asset.download_name}/* to {extract_to}/*)')
      with io.BytesIO(b) as f:
         with zipfile.ZipFile(f) as z:
            z.extractall(path=extract_to)
      return True

# -

def install_details_damage_meter(addon, asset):
   import tempfile
   with tempfile.TemporaryDirectory() as temp:
      temp = Path(temp)
      if not addon.install_from_asset(asset, extract_to=temp):
         return False

      temp_contents = [x for x in temp.iterdir()]
      assert len(temp_contents) == 1, temp_contents
      temp_addon_dir = temp_contents[0]

      toc = temp_addon_dir / f'{addon.name}.toc'
      project_version_key = '@project-version@'
      project_version = f'{addon.name}.{asset.version}'
      addon.print(f'[{toc.name}] s/{project_version_key}/{project_version}/')
      t = toc.read_text(encoding='utf8')
      t = t.replace(project_version_key, project_version)
      toc.write_text(t, encoding='utf8')

      def move(src, dst):
         addon.print(f'Moving {src}/* to {dst}/*')
         shutil.copytree(src, dst, dirs_exist_ok=True)
         shutil.rmtree(src)
      move(temp_addon_dir / 'plugins', ADDONS_DIR)
      move(temp_addon_dir, ADDONS_DIR / addon.name)

   return True

# -

ADDON_BY_NAME = {}
def RegisterAddon(name, *args):
   addon = Addon(name, *args)
   ADDON_BY_NAME[name.lower()] = addon
   return addon

# -

RegisterAddon('Details', lambda addon: addon.github_latest_tag('Tercioo/Details-Damage-Meter'), install_details_damage_meter)

for (name, repo) in [
   ('BigWigs', 'BigWigsMods/BigWigs'),
   ('LittleWigs', 'BigWigsMods/LittleWigs'),
   ('WeakAuras', 'WeakAuras/WeakAuras2'),
   ('AstralKeys', 'astralguild/AstralKeys'),
   ('MRT', 'curseforge-mirror/method-raid-tools'),
   ('Plater', 'Tercioo/Plater-Nameplates'),
   ('DBM-Core', 'DeadlyBossMods/DBM-Retail'),
   ('DBM-Party-Dragonflight', 'DeadlyBossMods/DBM-Dungeons'),
   ('DBM-PvP', 'DeadlyBossMods/DBM-PvP'),
   ('OmniCC', 'tullamods/OmniCC'),
   ('OmniCD', 'curseforge-mirror/omnicd'),
   ('Simulationcraft', 'simulationcraft/simc-addon'),
]:
   addon = RegisterAddon(name, lambda addon: addon.github_latest_release(addon.repo), Addon.install_from_asset)
   addon.repo = repo

# -
# Errata:

def parse_version__plater(version):
   parts = version.split('-')
   parts = [lstrip_non_digits(p) for p in parts]
   for p in parts:
      if p:
         version = p
         break
   else:
      assert False, f'Parse failed: {version}'

   version = parse_version__default(version)
   return version


ADDON_BY_NAME['plater'].fn_parse_version = parse_version__plater

# -

ADDON_BY_NAME['mrt'].fn_asset_version_from_download_name = lambda download_name: download_name.removeprefix('MRT').removesuffix('.zip')

ADDON_BY_NAME['omnicd'].fn_asset_version_from_download_name = lambda download_name: download_name.removeprefix('omnicd-v').removesuffix('.zip')

# -

def update_addon(addon, check_only, installed_only=True):
   try:
      existing_installed_version = addon.get_installed_version()
      if installed_only and existing_installed_version == None:
         addon.print('Not installed, skipping.')
         return True # Well, it's not out of date...

      asset = addon.query_latest_asset()
      if installed_only and existing_installed_version >= asset.version:
         latest_text = 'latest'
         if existing_installed_version != asset.version:
            latest_text = f'v{asset.version} is latest'
         addon.print(f'Already at v{existing_installed_version}. ({latest_text})')
         return True

      if check_only:
         addon.print(f'!!! UPDATE: v{existing_installed_version} installed, but v{asset.version} is available: {asset.download_url}')
         return False

      if not addon.fn_install(addon, asset):
         return False
      post_install_version = addon.get_installed_version()

      if existing_installed_version:
         addon.print(f'Updated v{existing_installed_version}->v{post_install_version}!')
      else:
         addon.print(f'Installed v{post_install_version}!')
      return True
   except ExButNotVerbose:
      return None

# -

def update_addons(addons, **kwargs):
   updates_found = 0
   errors_found = 0
   with concurrent.futures.ThreadPoolExecutor() as pool:
      for up_to_date in pool.map(lambda a: update_addon(a, **kwargs), addons):
         if up_to_date == False:
            updates_found += 1
         if up_to_date == None:
            errors_found += 1

   with_errors = ''
   if errors_found:
      with_errors = f' (with {errors_found} errors)'

   if kwargs['check_only']:
      if updates_found:
         print2(f'!!! {updates_found} updates found!{with_errors}')
      else:
         print2(f'No updates found!{with_errors}')
      return True
   else:
      if updates_found:
         print2(f'!!! {updates_found} updates failed!{with_errors}')
         return False
      print2(f'Done!{with_errors}')
      return True

# -

def addons_by_names(names):
   ret = []
   for name in names:
      try:
         addon = ADDON_BY_NAME[name.lower()]
      except KeyError:
         assert False, f'Unrecognized addon name: {name}'
      ret.append(addon)
   return ret

def exit_bool(success):
   exit(int(not success))

if __name__ == '__main__':
   args = sys.argv[1:]
   while args and args[0].startswith('-'):
      arg = args.pop(0)

      if arg.startswith('--verbose'):
         try:
            (_,level) = arg.split('=', 1)
         except:
            level = 2
         VERBOSE = int(level)
         continue
      if arg.startswith('-v'):
         vs = arg[1:]
         for v in vs:
            assert v == 'v', vs
         VERBOSE = len(vs)
         continue
      assert False, f'Bad arg: "{arg}"'

   if len(args) == 0:
      args.append('list')

   cmd = args.pop(0)
   if cmd == 'list':
      assert len(args) == 0, args
      print('Installed:')
      not_installed = []
      for name in sorted(list(ADDON_BY_NAME)):
         addon = ADDON_BY_NAME[name]
         v = addon.get_installed_version()
         if v:
            print(f'   {addon.name} v{v}')
         else:
            not_installed.append(addon)
      print('Available for install:')
      for addon in not_installed:
         print(f'   {addon.name}')

      print('To check for updates, use `check`.')
      exit(0)

   if cmd == 'check':
      addon_names = args
      if not addon_names:
         addon_names = sorted(list(ADDON_BY_NAME))
      addons = addons_by_names(addon_names)
      exit_bool(update_addons(addons, check_only=True))

   if cmd == 'update':
      addon_names = args
      if not addon_names:
         addon_names = sorted(list(ADDON_BY_NAME))
      addons = addons_by_names(addon_names)
      exit_bool(update_addons(addons, check_only=False))

   if cmd == 'install':
      addon_names = args
      if not addon_names:
         assert False, f'Choose one or more names of addons to install!'
      addons = addons_by_names(addon_names)
      exit_bool(update_addons(addons, check_only=False, installed_only=False))

   if cmd != 'help':
      print(f'Unrecognized cmd `${cmd}`.')

   print('''\
   wow-addon-update.py <cmd>

cmd:
* list
* check
* update
''')
   exit(0)
