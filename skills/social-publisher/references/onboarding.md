# Connect the current owner's Postiz and social accounts

One Plow installation, line and Hermes home per owner. Use only this home's
credentials and the current owner's native session/preferences. Examples,
history and another person's account do not establish a connected destination.

## 1. Establish the connection state

Sanitize status before its output reaches the model/chat:

```sh
postiz auth:status 2>&1 | sed '/Token:/d; /Key:/d'
```

Exit 0 does not prove authenticated. Successful `postiz integrations:list`
confirms API access; an empty array means authenticated without social accounts.
Never send raw auth output, keys, tokens, passwords or environment dumps in chat.
The owner chooses their own account/organization in the browser.

| Observed state | Next step |
| --- | --- |
| No credentials | Own Postiz account, then device login |
| Device login pending | Send URL/code; resume the same job |
| Authenticated, desired network missing | Connect that network in the owner's dashboard |
| Desired accounts discovered | Confirm names and collect brand/timezone |
| Expired/invalid credentials | Recover login; rediscover destinations |
| Wrong host/account or account change | Explicit switch, fresh discovery and preview |

## 2. Own account and browser authorization

For default cloud onboarding, ask whether the owner already has Postiz. If not,
send https://platform.postiz.com/auth to create their own account, or
https://platform.postiz.com/auth/login to sign in. The owner
selects their organization and any subscription/API access required by Postiz.
Do not create accounts or subscribe on their behalf. When they are ready, start:

Use this short signup response, adapted to their language:

“Crie sua própria conta em https://platform.postiz.com/auth. Escolha sua
organização e o plano ou período de teste oferecido pelo Postiz no site. Quando
estiver pronto, me avise: vou enviar o link para autorizar este Posta.”

Account buttons, signup providers, prices and trial terms come from the live
Postiz page the owner sees. The response above guides them without inventing those
details or promising a free cloud account.

```text
terminal(command="postiz auth:login", background=true, notify=true)
```

Keep the returned real `session_id` in the native Hermes session. Use
`process(action="log", session_id=...)` to obtain the emitted verification URL and
short user code, then send only those to the owner immediately:

“Abra [URL emitida], entre no seu Postiz e autorize com o código [código emitido].
Escolha a organização em que estão suas redes. Me avise quando concluir.”

Return the iMessage turn while the job is pending. Native completion notifications
or the owner's reply resume `process(action="poll", ...)` and `log` on the SAME
job. Do not start duplicate grants, wait in a foreground tool for the human,
invent flags such as `--no-browser`, or send a made-up code. CLI 2.0.16 exposes
only `--auth-server` for login. Its browser opener runs inside the agent; the owner
uses the link in iMessage on their own device.

After success, run sanitized status and `integrations:list`. The CLI stores OAuth
at `~/.postiz/credentials.json`, linked by this image into the installation's
private persistent home. A failed/expired job never means connected: describe the
observed problem and request one new code when the owner is ready. Recover a lost
job ID through native process inventory; if neither job nor credentials remain,
start one new login. Never copy credentials between homes or installations.

## 3. Connect the owner's social profiles

Postiz login does not connect Instagram or another network automatically.
CLI 2.0.16 has no `integrations:connect` command. For zero integrations or a
missing network, send this installation's dashboard URL (cloud:
https://platform.postiz.com; self-hosted: configured `POSTA_POSTIZ_DASHBOARD_URL`):

“No Calendar do seu Postiz, clique em Add Channel/Adicionar canal, escolha a rede e autorize
sua própria conta. Se houver seleção de perfil/página, escolha o destino que
quer usar. Depois me diga ‘conectei’ para eu conferir.”

The owner completes social consent in their browser. On their reply, run
`integrations:list` again, show the returned platform/account names and ask which
destinations to use if ambiguous. If still empty, explain the connection is
incomplete; never substitute a creator/example integration. Inspect
`integrations:settings ID` for the selected real destinations. Ask briefly for
brand/audience and confirm an IANA timezone before resolving schedule dates.
Then show the first complete preview and await approval. Connecting is not approval.

## 4. Recovery, disconnect and self-hosted

- On an explicit request to switch/disconnect this installation, first stop any
  pending login job with the native process tool and verify it exited. Then run
  `postiz auth:logout`, check sanitized status and API access again, and discard
  prior account choices in native preferences. A job left running could save a
  fresh credential after logout. Logout removes local OAuth;
  it does not revoke the remote grant or disconnect the social network. Direct
  the owner to Settings → Approved Apps for remote grant revocation, or to the
  channel menu for removing/reconnecting a social account. For
  API-key mode, that installation's operator configuration must also be removed
  or changed outside chat; logout must not silently fall back to an environment key.
- After account/network changes, rediscover and show a new preview for changed
  destinations. Logging out does not cancel existing scheduled posts in the old
  organization; do not claim cancellation occurred.
- For 401/403, stop social operations and inspect the observed error. Distinguish
  revoked auth, organization permissions and plan/API restrictions; do not infer
  the cause from status alone, retry creation blindly, or borrow another account.
  Guide correction in the owner's dashboard, then verify access again.
- For self-hosted Postiz, ask for the owner's dashboard URL, never a key in chat.
  Use that instance's supported CLI auth server if provisioned. Otherwise direct
  the owner to private `compose.self-hosted.yml` setup with their OWN API root/key.
  Do not use the creator's instance, invent an auth-server URL or promise the
  cloud CLI auth server can relay authorization to an arbitrary VPS.

Sources: [CLI authentication](https://docs.postiz.com/cli/authentication),
[connect channels](https://docs.postiz.com/general/channels/connect),
[installed CLI source](https://github.com/gitroomhq/postiz-agent),
[self-hosted CLI auth](https://docs.postiz.com/self-host/cli-auth-server).
