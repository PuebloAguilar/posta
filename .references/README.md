# Referências somente de consulta

Os submodules preservam o código original e ficam fora do contexto Docker. O
runtime usa a imagem OCI da base e instala o CLI Postiz pelo npm; não compila nem
importa estas pastas. Atualize esta tabela quando mover um pin.

| Referência | Propósito | Licença | Commit consultado |
| --- | --- | --- | --- |
| [plow-hermes-agent](https://github.com/plow-pbc/plow-hermes-agent) | Contrato de persona/skills, boot e Agent Index embutido | Apache-2.0 | `c692e807386993b677de13500ce3a1a323d52b48` |
| [plow-agents](https://github.com/plow-pbc/plow-agents) | CLI de login, linha, Compose e publicação/admissão | Apache-2.0 | `53dd92242e88f6e877cc09dbfb08b31b0e3925cb` |
| [postiz-agent](https://github.com/gitroomhq/postiz-agent) | Cliente mantido de contas, upload, criação, auth e status | AGPL-3.0 | `de2032e46d329c4e01714a65a57da28cd419a5b2` |

Consultados em 2026-10-14. Todos estavam ativos, com pushes recentes em setembro/
outubro; atividade não equivale a garantia de estabilidade. Postiz exige Node
>=18. O CLI Plow usa Python 3.11+ (`tomllib`) e Docker.

O `main` do Postiz aponta a versão 2.0.21, mas o registry npm consultado publicou
2.0.16 como latest; por isso o runtime fixa 2.0.16 com integridade no lock. A versão
instalável e o commit de consulta são fatos distintos. A base também fixa suas
próprias versões de Hermes/plugin; esta variante não troca esses componentes.

## Reutilização escolhida

CLI npm oficial em vez de cliente próprio: cobre descoberta de schemas, upload,
draft/schedule/now por JSON e consulta de posts. A integração consiste em
instruções de domínio e credenciais por instalação. O MCP oficial Postiz é uma
alternativa quando a instância oferece suas ferramentas, mas exigiria outra
conexão/configuração sem necessidade nesta versão.

O usuário rejeitou ledger/executor próprio. Portanto não se justifica implementar
um backend, scheduler ou camada de estado neste projeto. Postiz fornece o relógio
de publicação e Hermes conserva as conversas. Aprovação por instrução de modelo
não oferece a garantia de um bloqueio determinista.

## Imagem base

`public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-c692e807386993b677de13500ce3a1a323d52b48@sha256:e04a373ed7b8a1f6440e4813eb282c2b6087d31e77c6e5e386ae40a307163d32`

Índice público conferido com linux/amd64 e linux/arm64. A referência completa usa
digest, impedindo que uma troca de tag altere os bytes escolhidos.
