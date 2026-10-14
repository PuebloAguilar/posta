# Publicação no Plow e Agent Index

Estas etapas descrevem o fluxo de instalação e release. O usuário escolheu
**Posta**, slug **`posta`**. A instalação local já respondeu com prévia pelo
iMessage e registrou o listing. Consulte [RELEASE-HANDOFF.md](RELEASE-HANDOFF.md)
para o estado da imagem pública e da admissão.

## 1. Validar a instalação

Faça o login e deploy local do README. Use o próprio telefone para ativar a conta.
Teste pelo iMessage uma ideia, uma prévia, uma edição e uma aprovação. Agende um
conteúdo real somente quando o dono aprovar essa prévia, conta e horário. Confira
o ID/estado no Postiz. Testes de fixture não substituem essa prova.

## 2. Registrar o listing

No `plow-credentials` privado, acrescente o slug escolhido e seus textos públicos:

```dotenv
AGENT_ID=posta
AGENT_NAME=Posta
AGENT_BLURB=Create social content over iMessage. Preview, approve, and schedule with Postiz.
```

Recrie o container para carregar o ambiente:

```sh
docker compose up -d
```

O reporter já embutido na base registra e envia uso a cada cinco minutos. Você
também pode definir o listing diretamente pelo CLI, quando tiver slug e repo:

```sh
plow-agents image set posta --name 'Posta' --blurb 'Create social content over iMessage. Preview, approve, and schedule with Postiz.' --repo https://github.com/SEU_USUARIO/SEU_REPO
```

Listing público e instalação na nuvem são etapas distintas. Confirme que a página
correta apareceu e que o uso do seu teste foi reportado. Logo é opcional; se for
criado, a arte final deve ser uma imagem gerada/editada por IA.

## 3. Imagem pública e UID

Escolha sua organização/conta GHCR e uma tag de release:

```sh
docker login ghcr.io -u SEU_USUARIO
plow-agents image build ghcr.io/puebloaguilar/posta:v1
plow-agents image push ghcr.io/puebloaguilar/posta:v1
plow-agents profile --show
```

O comando `image build` do CLI consultado constrói **linux/amd64**, compatível com
o deploy cloud. `image push` só envia a tag já construída; não faz build e não deve
enviar uma tag antiga por engano. O CLI não produz uma imagem multiarch automaticamente. Para distribuir nas duas
arquiteturas, use um builder apropriado e `docker buildx build --platform
linux/amd64,linux/arm64 --push -t ghcr.io/puebloaguilar/posta:v1 .`; faça isso
apenas em uma máquina com capacidade suficiente.

Depois do primeiro push, marque o pacote GHCR como público em Package settings →
Change visibility → Public. GHCR cria o pacote privado mesmo quando seu repo é
público; a mudança para Public é irreversível. Essa mudança é feita pela UI; não
há setter público REST/GraphQL documentado confirmado. Confirme pull anônimo
da referência `repository@sha256:...` impressa pelo push; o sucesso autenticado do
criador não comprova acesso público. A imagem contém código/configuração genérica,
sem `.env`, `plow-credentials`, tokens ou dados sociais.

## 4. Admissão de deploy de um clique

Entregue à equipe Plow no Discord: UID retornado pelo profile, slug, referência
pública da imagem por digest e repo/commit correspondente. Um administrador precisa
admitir a primeira imagem e atribuir o owner. Preparar essas informações não envia
uma mensagem nem significa que a admissão ocorreu.

Cada instalador recebe sua própria identidade Plow e volume. O Postiz de cada um
deve passar pelo onboarding individual. O device flow cloud é a conexão existente
mais direta; self-hosted requer auth server da instância ou provisionamento seguro
de chave fora do chat. O CLI Plow público não oferece `deploy --env`/secrets para
copiar a chave Postiz do criador para os instaladores.

## 5. Releases seguintes

Depois da admissão administrativa:

```sh
plow-agents image build ghcr.io/puebloaguilar/posta:v2
plow-agents image push ghcr.io/puebloaguilar/posta:v2 --promote posta
plow-agents image show posta
```

Promoção altera a imagem para novas instalações; agentes já existentes mantêm sua
imagem. Verifique o digest público e o listing antes de declarar a release ativa.

Fontes: [CLI Plow: registro, admissão e promoção](https://github.com/plow-pbc/plow-agents#register-admit-then-promote-an-agent-image),
[reporter embutido](https://github.com/plow-pbc/plow-hermes-agent#the-agent-index-reporter),
[CLI Postiz auth](https://docs.postiz.com/cli/authentication).
