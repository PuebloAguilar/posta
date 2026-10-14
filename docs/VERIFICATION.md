# Verificação — 2026-10-14

Entrega local: persona + skill, como escolhido pelo usuário. O fluxo padrão é
prévia no iMessage e agendamento depois da aprovação. Este documento distingue
imagem/CLI verificados de login, conversa e publicação ainda pendentes.

## Provas realizadas

| Superfície | Evidência | Resultado |
| --- | --- | --- |
| Base imutável | Registry público/`imagetools inspect` do digest no Dockerfile | Índice amd64/arm64 confirmado |
| Imagem local | `docker build --platform linux/arm64 -t plow-postiz-hermes-agent:local .` | PASS |
| CLI no container | `postiz --version` executado como UID 10000 | 2.0.16 |
| Transporte/schema CLI | `tests/cli_contract.py` dentro da imagem, API local e chave fictícia | PASS, 9 checks |
| Skill metadata | `quick_validate.py` com o Python da imagem | PASS |
| Descoberta Hermes | `hermes skills list` dentro da imagem como UID 10000 | social-publisher enabled |
| Seeds/persona | Arquivos nas seeds e home lidos pelo UID 10000 | PASS |
| OAuth storage | Node `os.homedir()` retorna `/opt/data`; `.postiz` resolve para `/var/lib/hermes/.postiz`, gravável | PASS, diretório no volume persistente |
| Compose | `docker compose config --quiet`, credencial fictícia temporária fora do checkout | PASS |
| Postiz real | `auth:status` e `integrations:list` com o CLI da imagem no endpoint self-hosted do usuário | PASS read-only; uma integração instagram-standalone ativa |
| Skill aplicada | Seis cenários antes/depois por avaliador independente | Referência resolveu lacunas de comandos, host/auth, mídia e payload; sem execução social |
| Revisão independente | Revisão de Docker/CLI/skill/docs e fixture repetida pelo revisor | Dois P2 de docs corrigidos; sem achados adicionais no escopo |
| Boot sem identidade | `/init` completo, sem rede/token/API Plow, respeitando a espera de 60s da base | PASS: parked marker, supervisor vivo e gateway retido |
| Segredos no build | Guard oficial `refuse_credentials` + busca pelo valor real da chave nos artefatos próprios | PASS; chave não encontrada |
| Login Plow | Ativação enviada pelo Mensagens com autorização expressa do dono; CLI gravou login mode600 | PASS |
| Deploy autenticado | `plow-agents deploy --local --line ln_p3` | PASS; container/volume próprio ativo |
| Canal iMessage | Mensagem de teste entregue na linha +1 650 315 6536 e resposta recebida | Canal PASS; conteúdo bloqueado por HTTP 402 sem créditos Plow |

O teste de contrato usa o binário oficial realmente instalado. Exercita auth,
descoberta, settings, upload multipart, preservação de JSON e `id/path`, tipos
draft/schedule/now, listagem QUEUE, prefixo `/api/public/v1` e Authorization. A API
simulada aceita payloads; isso não prova validação de um servidor Postiz real,
permissões dos providers ou entrega de mídia pelas redes sociais.

Os primeiros checks de boot usaram um orçamento menor que a espera transitória de
60s por credencial definida em `plow-init.py`; por isso não observaram ainda o
marker. A inspeção da fonte identificou essa causa. O check respeitando essa espera
confirmou `no PLOW_API_BASE ... after 60s`, mantendo o supervisor ativo e sem
iniciar o gateway. Nenhum componente da base foi alterado para obter esse resultado.

O baseline sem a skill conhecia a necessidade de aprovação, mas não fornecia a
sequência auth/discovery/upload/payload executável. Com a skill, o avaliador usou
auth-first, host da instalação, `id/path` do upload, UTC e consulta de estado. Esses
são cenários de instruções em um agente de avaliação; não equivalem ao modelo
Hermes da base respondendo a mensagens reais no iMessage.

## Correções de revisão

- CLI Plow `image push` apenas envia uma tag existente. O roteiro agora executa
  `image build` para a mesma tag antes de cada push/promoção e atribui amd64 ao build.
- `deploy --local` gera `./plow-credentials`. O onboarding padrão deixa
  `PLOW_CREDENTIALS` indefinido; override externo usa `mint --credential-file`
  seguido de Compose, com o mesmo arquivo.

## Recursos e ambiente

Somente arm64 foi construído nesta máquina. A base precisou de download inicial;
houve pressão temporária no disco e depois o espaço disponível recuperou. Não foi
feito prune global, exclusão de imagens antigas, limpeza de volumes ou alteração
de outros projetos. O contexto de build transferido foi de aproximadamente 38 KB;
referências e credenciais ficaram excluídas pela allowlist Docker.

## Instalação local atual

Nome escolhido pelo usuário: **Posta**; slug: **posta**. Linha local: `ln_p3`,
número **+1 650 315 6536**. Conta Plow ativada; credencial de agente mode600, excluída
de Git/build. Container `plow-postiz-hermes-agent-agent-1` ativo com home própria.
Configuração local self-hosted preservada em `.env` privado, sem copiar a chave
Postiz para esse arquivo. A chave entra pelo ambiente.

A primeira mensagem pediu apenas discovery das redes, sem criar/agendar. Ela foi
recebida; o gateway tentou o modelo default da base (`z-ai/glm-5.2` via Plow), mas
recebeu HTTP 402 e respondeu no iMessage que a conta está sem créditos. A conexão
com o canal está comprovada; comportamento do modelo e criação de prévia real
ainda não foram comprovados. Não repetir o pedido até resolver o saldo/provedor.

O Hermes local do dono está configurado com `openai-codex`/`gpt-5.5`; a base tem
suporte a esse provedor. Após o usuário perguntar sobre usar a conta Codex, foi
iniciado o login nativo do Posta (`hermes auth add openai-codex --type oauth`), com
sessão própria no volume privado. O fluxo aguarda a autorização da conta no
navegador. Nenhuma credencial Codex do Hermes principal foi copiada ou renovada,
nenhuma recarga feita, e o modelo não será trocado antes do login confirmado.

A fonte runtime `auth_oauth_grants.py` classifica openai-codex como refresh de uso
único: duplicar o grant em dois arquivos pode invalidar uma das sessões quando a
outra renova. Por isso a instalação usa a mesma conta com um grant independente.
Compose validou os knobs nativos `HERMES_PROVIDER` e `HERMES_MODEL`; o código de
boot/gateway da base permanece intacto. A tela oficial de autorização foi aberta
no Chrome, mas leitura da URL via Apple Events não estava disponível nesta sessão.

A documentação oficial consultada nesta continuação indica a retirada de GPT-5.5
do Codex em 2026-10-14; o modelo encontrado na configuração do Hermes principal não
foi alterado. Os exemplos do Posta usam `gpt-6.1-sol`, com disponibilidade/inferência
pendentes do login e teste da conta. Fonte: [OpenAI models](https://learn.chatgpt.com/docs/models#gpt-61-sol).

## Pendências reais

- Concluir autorização Codex do Posta no navegador; depois configurar o provedor
  local e validar prévia/edição/aprovação pela conversa real.
- Upload e agendamento em Postiz real de conteúdo aprovado; nenhum post foi criado
  nos testes acima.
- Provedor de imagens IA para arte nova; não foi feita geração de imagem.
- OAuth self-hosted/device flow cloud: rota da instância escolhida precisa de prova.
- Repo remoto, push GHCR, pull anônimo, listing Index e admissão
  administrativa de deploy de um clique. A imagem atual é local.

As regras de aprovação são orientações de persona/skill, sem gate determinista ou
registro próprio, conforme o escopo escolhido. Não declarar garantia absoluta de
deduplicação, cumprimento pelo modelo ou isolamento de contas sem a prova runtime
que a situação exige.
