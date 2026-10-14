# Posta — estado da instalação e publicação

Atualizado em 2026-10-14. Nome/slug escolhidos pelo usuário: **Posta / posta**.

| Campo | Estado |
| --- | --- |
| Projeto local | `/Users/pueblo/Projects/plow-postiz-hermes-agent` |
| Fonte pública | https://github.com/PuebloAguilar/posta, main |
| Linha Plow | `ln_p3`, +1 650 315 6536 |
| Execução | Docker Compose local, container próprio ativo |
| Postiz | Instância self-hosted do dono autenticada; Instagram standalone ativo |
| Modelo atual | `z-ai/glm-5.2` via Plow, inferência funcionando após recarga; tentativa Codex encerrada |
| Preview/aprovação | Prévia de legenda recebida no iMessage; discovery real e zero comandos de escrita social |
| UID do builder | `819e6514-a7f5-4437-820f-62a3238d7c1d` |
| Slug do Agent Index | `posta`, listing registrado; consulta pública confirmou Posta e blurb corretos |
| Release v1 | `ghcr.io/puebloaguilar/posta:v1`, linux/amd64 |
| Imagem local | arm64 e amd64 construídas; CLI amd64 passou nove checks |
| Registry público | GitHub visibility public; pull anônimo pelo digest PASS |
| Agent Index | Registrado pelo reporter nativo; https://aiworthusing.com/agent-index/posta |
| Deploy de um clique | Exige primeira admissão administrativa pelo Plow |

Referência publicada e verificada:

```text
ghcr.io/puebloaguilar/posta@sha256:4e93403e36a5db1bca1d6d3e6e904e917b49ebddb6e2262e49f1f1892c459be0
```

Fonte dos arquivos incluídos nessa imagem: commit
`be17377f2f0145e173c6c165b9e33ddf6735abe7`. Os commits posteriores documentam a
publicação. O pacote GHCR contém somente amd64; arm64 foi verificado localmente e
não integra esse manifest público. Cada instalador precisa conectar seu Postiz.

Não há código/token de ativação, chave Postiz ou credencial de modelo neste arquivo.
Os dados públicos de identidade acima servem à coordenação da publicação. A
mensagem ao Discord só deve ser enviada quando houver instrução explícita.

Próximo passo externo: entregar [a solicitação preparada](ADMISSION-MESSAGE.md)
à equipe Plow e aguardar a primeira admissão. Nenhuma mensagem ao Discord foi
enviada. Depois da confirmação administrativa, consultar `plow-agents image show
posta` e validar a primeira instalação cloud. [PUBLISH.md](PUBLISH.md) descreve o
fluxo e as atualizações seguintes.
