# Postiz CLI workflow

## Authenticate the right instance

`POSTIZ_API_URL` is the API root, without `/public/v1`; the CLI appends that suffix.
For self-hosted reverse proxies it commonly ends in `/api`. Configure the owner's
actual URL before calls. API keys come from the deployment environment, never the
image, persona, skill or iMessage thread.

Run `postiz auth:status` first and inspect its result locally; it can print part of
the key, so never forward its raw output. Saved OAuth credentials override API key
and URL environment variables. If they point at another host, report the mismatch
and have the owner reconnect that installation; do not silently change accounts.

For Postiz cloud onboarding, run `postiz auth:login` using an interactive terminal
session. Send only the verification URL and short device code to the owner, let
them approve in the browser, and resume/poll that same terminal until login finishes.
Never ask for a password or API token in chat. Self-hosted OAuth requires the
instance's supported auth server (`POSTIZ_AUTH_SERVER`); hosted OAuth routing to an
arbitrary self-hosted instance is not established. An operator can provision a
self-hosted API key outside chat instead. Re-run auth status after connection.

## Discover and prepare

```sh
postiz integrations:list
postiz integrations:settings INTEGRATION_ID
postiz upload /absolute/path/to/approved-media.png
```

These outputs can have human-readable lines before their JSON. Read the complete
output and extract the JSON object; do not pipe the complete stdout into `jq` and
assume it is JSON. Keep the real upload object's `id` and `path` in the payload.
Use the discovered integration `identifier` as `settings.__type`.

Check `rules`, `maxLength`, required settings and the actual media. For
`instagram-standalone`, `post_type` is `post` or `story`; a Reel/video uses `post`,
not a fabricated `reel` enum. Story has one media per post. Do not promise music
selection, links/polls/stickers, or unsupported provider features. Revalidate
image/video dimensions and format when the requested surface requires them.

## Date and payload

Convert the confirmed local time using an IANA zone, not a hard-coded offset:

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
local = datetime(2026, 10, 15, 9, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))
print(local.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"))
```

The output is `2026-10-15T12:00:00Z`. Resolve ambiguous/nonexistent daylight-saving
times with the owner. Do not send an already-past schedule date.

After approval, write a temporary JSON request with the owner's exact content,
discovered integration and actual upload result. This illustrative payload is a
schema example; its example IDs/URL must be replaced, never submitted as-is:

```json
{
  "type": "schedule",
  "date": "2026-10-15T12:00:00Z",
  "shortLink": false,
  "tags": [],
  "posts": [{
    "integration": { "id": "integration-from-discovery" },
    "value": [{
      "content": "The exact approved caption",
      "image": [{ "id": "id-from-upload", "path": "https://owner-postiz.example/uploads/approved.png" }]
    }],
    "settings": { "__type": "instagram-standalone", "post_type": "post" }
  }]
}
```

```sh
postiz posts:create --json /absolute/path/to/approved-request.json
postiz posts:list --startDate 2026-10-15T00:00:00Z --endDate 2026-10-16T00:00:00Z
```

Supply a valid UTC `date` for every payload, including drafts and `now`. `draft`
stores without publishing; `schedule` uses date; `now` submits for immediate
publication. In CLI 2.0.16, `-t` lists schedule/draft only, but `--json` supports the
API's `now` type. Immediate publication still requires preview approval.

For text-only supported networks, `image` can be `[]`; never use that shortcut for
Instagram. For multiple providers, build a separate `posts` item/settings per
account. Do not send the Instagram settings to another platform.

## Confirm, reconcile and change

Creation returns `postId` and integration. Consult those IDs in `posts:list`;
check `publishDate`, `state`, integration and the approved content/media.
`QUEUE` means queued; `PUBLISHED` means published; `ERROR` means failure. Keep the
returned IDs in the Hermes conversation to support status checks after restarts.
Future scheduled posts need no extra Hermes cron to publish them.

An uncertain creation response is not a retry signal. Query the interval,
compare content/media/account/date and reuse a matching result. If none is visible
but acceptance remains uncertain, tell the owner the outcome is unresolved.

For an explicitly requested cancellation, inspect the exact post ID then use
`postiz posts:delete POST_ID` and verify it left the queue. This removes the Postiz
record; it does not guarantee removal of content already live on a social network.
Changing an approved scheduled post needs a new preview; do not cancel the old one
until the owner authorizes the replacement. Use `postiz posts:create --help` and the
instance's schema for supported edits instead of inventing an update endpoint.

Sources: [official CLI](https://github.com/gitroomhq/postiz-agent),
[create API](https://docs.postiz.com/public-api/posts/create),
[list API](https://docs.postiz.com/public-api/posts/list),
[self-hosted auth server](https://docs.postiz.com/self-host/cli-auth-server).
