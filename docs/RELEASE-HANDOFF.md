# Posta — estado da instalação e publicação

Atualizado em 2026-10-14. Nome/slug escolhidos pelo usuário: **Posta / posta**.

| Campo | Estado |
| --- | --- |
| Projeto local | `/Users/pueblo/Projects/plow-postiz-hermes-agent` |
| Fonte pública | https://github.com/PuebloAguilar/posta, main |
| Linha Plow | `ln_p3`, +1 650 315 6536 |
| Execução | Docker Compose local, container próprio ativo |
| Postiz | Default desconectado; chave pessoal removida do runtime; cada pessoa conecta a própria conta |
| Modelo atual | `z-ai/glm-5.2` via Plow, inferência funcionando após recarga; tentativa Codex encerrada |
| Onboarding | Cadastro próprio, login em background, URL/código reais recebidos no iMessage; teste cancelado sem autorização |
| Preview/aprovação | Prévia v1 validada; v2 mantém aprovação e acrescenta onboarding individual |
| UID do builder | `819e6514-a7f5-4437-820f-62a3238d7c1d` |
| Slug do Agent Index | `posta`, listing registrado; consulta pública confirmou Posta e blurb corretos |
| Release v2 | `ghcr.io/puebloaguilar/posta:v2`, linux/amd64 |
| Imagem local | arm64 e amd64 construídas; CLI amd64 passou nove checks |
| Registry público | GitHub visibility public; pull anônimo pelo digest PASS |
| Agent Index | Registrado pelo reporter nativo; https://aiworthusing.com/agent-index/posta |
| Deploy de um clique | Exige primeira admissão administrativa pelo Plow |

Referência publicada e verificada:

```text
ghcr.io/puebloaguilar/posta@sha256:9f847ecc27dd314965b39e0b6b4d3a852ca0b88672cdbc3caecf66f8073fdf09
```

Fonte dos arquivos incluídos nessa imagem: commit
`eeae052655e2bd1375cc31287bf19cb0089d89af`. Os commits posteriores documentam a
publicação. O pacote GHCR contém somente amd64; arm64 foi verificado localmente e
não integra esse manifest público. Cada instalador precisa conectar seu Postiz.

Dois usuários fictícios, com homes e autorizações distintas, passaram no teste
do CLI real. Signup/OAuth social completos de outra pessoa e primeiro deploy cloud
ainda exigem a ação dessa pessoa/equipe; não foram simulados como sucesso real.

Não há código/token de ativação, chave Postiz ou credencial de modelo neste arquivo.
Os dados públicos de identidade acima servem à coordenação da publicação. A
mensagem ao Discord só deve ser enviada quando houver instrução explícita.

Próximo passo externo: entregar [a solicitação preparada](ADMISSION-MESSAGE.md)
à equipe Plow e aguardar a primeira admissão. Nenhuma mensagem ao Discord foi
enviada. Depois da confirmação administrativa, consultar `plow-agents image show
posta` e validar a primeira instalação cloud. [PUBLISH.md](PUBLISH.md) descreve o
fluxo e as atualizações seguintes.
