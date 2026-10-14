# Posta — estado da instalação e publicação

Atualizado em 2026-10-14. Nome/slug escolhidos pelo usuário: **Posta / posta**.

| Campo | Estado |
| --- | --- |
| Projeto local | `/Users/pueblo/Projects/plow-postiz-hermes-agent` |
| Linha Plow | `ln_p3`, +1 650 315 6536 |
| Execução | Docker Compose local, container próprio ativo |
| Postiz | Instância self-hosted do dono autenticada; Instagram standalone ativo |
| Modelo atual | `z-ai/glm-5.2` via Plow, inferência funcionando após recarga; tentativa Codex encerrada |
| Preview/aprovação | Prévia de legenda recebida no iMessage; discovery real e zero comandos de escrita social |
| UID do builder | `819e6514-a7f5-4437-820f-62a3238d7c1d` |
| Slug do Agent Index | `posta`, listing registrado; consulta pública confirmou Posta e blurb corretos |
| Target da imagem v1 | `ghcr.io/puebloaguilar/posta:v1`, definido em `plow-agents.toml` |
| Imagem local | arm64 e amd64 construídas; CLI amd64 passou nove checks |
| Registry público | Ainda não enviado; não existe digest público da variante verificado |
| Agent Index | Registrado pelo reporter nativo; https://aiworthusing.com/agent-index/posta |
| Deploy de um clique | Exige primeira admissão administrativa pelo Plow |

Não há código/token de ativação, chave Postiz ou credencial de modelo neste arquivo.
Os dados públicos de identidade acima servem à coordenação da publicação. A
mensagem ao Discord só deve ser enviada quando houver instrução explícita.

Próximo passo: publicar fonte e imagem amd64, confirmar pull anônimo e
entregar UID/slug/digest ao administrador conforme [PUBLISH.md](PUBLISH.md).
