# Added runtime components

- Postiz CLI 2.0.16, installed unmodified from the npm registry with integrity
  recorded in `/opt/postiz/package-lock.json`.
  Package: https://registry.npmjs.org/postiz/2.0.16
  Source repository: https://github.com/gitroomhq/postiz-agent
  License: AGPL-3.0; accompanying text in `postiz-cli-LICENSE.txt`.
  The consulted main commit is `de2032e46d329c4e01714a65a57da28cd419a5b2`,
  which is not asserted to be the source commit of the npm release.
- Plow Hermes base at commit `c692e807386993b677de13500ce3a1a323d52b48`,
  OCI index digest `e04a373ed7b8a1f6440e4813eb282c2b6087d31e77c6e5e386ae40a307163d32`.
  Source: https://github.com/plow-pbc/plow-hermes-agent/tree/c692e807386993b677de13500ce3a1a323d52b48
  License/notice: `plow-base-LICENSE.txt`, `plow-base-NOTICE.txt`.
- Transitive npm dependencies retain their notices in
  `/opt/postiz/node_modules`; versions/integrities are recorded in the lock.

The image contains no Postiz server, modified CLI, replacement Plow gateway or
custom publication runtime. Base components retain their existing notices.
