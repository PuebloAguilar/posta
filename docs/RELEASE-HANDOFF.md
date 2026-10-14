# Posta — estado da instalação e publicação

Atualizado em 2026-10-14. Nome/slug escolhidos pelo usuário: **Posta / posta**.

| Campo | Estado |
| --- | --- |
| Projeto local | `/Users/pueblo/Projects/plow-postiz-hermes-agent` |
| Linha Plow | `ln_p3`, +1 650 315 6536 |
| Execução | Docker Compose local, container próprio ativo |
| Postiz | Instância self-hosted do dono autenticada; Instagram standalone ativo |
| Modelo atual | Base Plow default (HTTP 402); login Codex próprio iniciado, aguardando autorização |
| Preview/aprovação | Persona/skill pronta; aguarda inferência funcional para prova iMessage |
| UID do builder | `819e6514-a7f5-4437-820f-62a3238d7c1d` |
| Slug do Agent Index | `posta`, consulta pública retornou inexistente antes do registro |
| Target da imagem v1 | `ghcr.io/puebloaguilar/posta:v1`, definido em `plow-agents.toml` |
| Imagem local | arm64 construída e atualizada com a persona Posta |
| Registry público | Ainda não enviado; não existe digest público da variante verificado |
| Agent Index | Ainda não registrado, esperando teste do modelo/conteúdo |
| Deploy de um clique | Exige primeira admissão administrativa pelo Plow |

Não há código/token de ativação, chave Postiz ou credencial de modelo neste arquivo.
Os dados públicos de identidade acima servem à coordenação da publicação. A
mensagem ao Discord só deve ser enviada quando houver instrução explícita.

Próximo passo: concluir a autorização Codex própria, testar a prévia real, construir a release
amd64 em ambiente com espaço, enviar/publicar a imagem, registrar o Index e
entregar UID/slug/digest ao administrador conforme [PUBLISH.md](PUBLISH.md).
