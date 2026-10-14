# Posta — solicitação à equipe Plow

Mensagem pronta para o canal de publicação do Discord da Plow. Não foi enviada.
A primeira admissão exige um administrador; publicar imagem/listing não a substitui.

```text
Please enable 1-click deploy for Posta.

Builder uid: 819e6514-a7f5-4437-820f-62a3238d7c1d
Agent slug: posta
Image: ghcr.io/puebloaguilar/posta@sha256:9f847ecc27dd314965b39e0b6b4d3a852ca0b88672cdbc3caecf66f8073fdf09
Source: https://github.com/PuebloAguilar/posta
Image source commit: eeae052655e2bd1375cc31287bf19cb0089d89af
Listing: https://aiworthusing.com/agent-index/posta

Posta is a Hermes persona and skill built on the official Plow base. It previews social content over iMessage and uses each user's Postiz account to schedule approved posts.

The v2 public image supports linux/amd64 and was pulled anonymously by this exact digest. Each installation starts disconnected from Postiz and guides its owner through their own account, browser device authorization, social-channel connection and destination confirmation. Real device login in the background delivered its URL/code over iMessage; this test was cancelled before approval. The installed CLI passed two isolated fixture-account logins and the upload/scheduling payload checks. No social post was created during validation. The image contains no user credentials, and default Compose does not inherit the operator's Postiz key.
```

Se precisar conferir os comandos de admissão, a equipe pode usar a
[documentação oficial do CLI Plow](https://github.com/plow-pbc/plow-agents#register-admit-then-promote-an-agent-image).
