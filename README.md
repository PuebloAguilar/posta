# Posta — seu agente de conteúdo pelo iMessage

Mande uma ideia, foto ou vídeo pelo iMessage. O agente prepara o conteúdo, mostra
uma prévia e agenda nas suas redes pelo Postiz depois da sua aprovação.

Cada pessoa tem sua própria instalação Plow, linha iMessage, contas e preferências.
O número usado no teste do criador pertence à instalação dele. Esta versão contém
**persona e skill**; usa as sessões do Hermes e a fila do Postiz, sem banco,
registro de execução ou scheduler próprio.

## Exemplos de conversa

> Crie um post sobre meu lançamento usando essa foto para amanhã às 9h.

O agente mostra texto, foto, formato, conta e data/hora/fuso. Depois:

> Aprovado. Pode agendar.

Outros pedidos: “melhore o CTA”, “me mostre a agenda da semana”, “o post já saiu?”
e “cancele o post que ficou agendado para sexta”. Alterar uma prévia exige aprovação
da nova versão. Fotos e vídeos enviados continuam sendo seus; capas e artes novas
precisam de um provedor de imagens IA configurado no Hermes.

## Executar localmente

Requisitos: Docker rodando, Python 3.11+ e uma conta Plow. Ao clonar este projeto,
use `git submodule update --init --depth 1` para obter as referências.

No diretório do projeto, coloque o CLI oficial fixado desta referência no PATH da
sessão ou use diretamente `.references/plow-agents/bin/plow-agents`:

```sh
export PATH="$PWD/.references/plow-agents/bin:$PATH"
plow-agents login
plow-agents lines
```

O dono deve enviar pelo próprio telefone a frase de ativação ao número que o login
mostrar. Escolha uma linha disponível; `ln_p1` no exemplo do Plow não garante uma
linha livre na sua conta.

Mantenha um diretório/credencial e home exclusivos por instalador/linha. Se operar
várias instalações no mesmo host, use `COMPOSE_PROJECT_NAME` distinto e o fluxo
`mint --credential-file` abaixo com arquivo privado distinto para cada uma.
Não reutilize o volume de outra pessoa ao trocar o dono ou a linha.

O padrão começa desconectado do Postiz. Você pode copiar `.env.example` para
`.env` privado e definir seu fuso, mas não precisa fornecer uma chave para o
onboarding cloud. Chaves `POSTIZ_API_KEY`/URLs exportadas no terminal do operador
não são passadas automaticamente ao agente.

```sh
plow-agents deploy --local --line ID_DA_LINHA_LIVRE
docker compose logs --tail=80 agent
```

Nesse fluxo, deixe `PLOW_CREDENTIALS` sem definição: o CLI gera
`./plow-credentials` e o Compose deve ler esse mesmo arquivo. Para manter a
credencial fora do checkout, use explicitamente `plow-agents mint
ID_DA_LINHA_LIVRE --credential-file /caminho/privado/plow-credentials` e depois
`PLOW_CREDENTIALS=/caminho/privado/plow-credentials docker compose up -d --build`,
em vez de combinar esse override com `deploy --local`.

O Compose constrói a imagem, recebe o token de agente em `plow-credentials` e mantém
as conversas/credenciais OAuth no volume `agent-home`. Mande “oi” ao número da
linha e peça “conectar meu Postiz”. O agente conduz o fluxo abaixo.

Não envie chaves pelo iMessage. O agente roda `auth:status` sem devolver sua saída
bruta ao chat. Uma credencial OAuth salva tem precedência sobre ambiente: confira
que ela pertence ao host/organização desejados antes de trocar a configuração.

## Conectar suas próprias contas

1. Entre ou crie sua conta em [Postiz](https://platform.postiz.com/auth). Escolha
   sua organização e confira o acesso API/assinatura exigido pelo serviço.
2. No iMessage do seu Posta, diga que está pronto para conectar. Ele envia o link
   e o código reais de autorização e continua disponível enquanto você autoriza
   no navegador. Nenhuma senha ou API key precisa ser enviada pelo chat.
3. No Calendar do seu Postiz, escolha **Add Channel**, selecione Instagram ou a
   rede desejada e autorize a sua própria conta. Se necessário, escolha sua
   página/canal/perfil. Diga “conectei” no iMessage.
4. O Posta consulta e mostra os perfis encontrados. Confirme os destinos, a voz da
   sua marca, o público e o fuso. Depois envie uma ideia, foto ou vídeo.
5. Revise a prévia com conta, conteúdo, mídia e horário. O agendamento ocorre
   somente depois da aprovação dessa versão.

Cada pessoa autentica seu próprio Postiz; conexão nenhuma é herdada do criador.
Troca, expiração, reconexão e logout estão em [docs/ONBOARDING.md](docs/ONBOARDING.md).

Para **self-hosted**, use o auth server compatível já existente da sua instância
ou configure sua própria chave fora do chat: preencha as variáveis
`POSTA_SELF_HOSTED_*` e `POSTA_POSTIZ_DASHBOARD_URL` no `.env` privado e execute
`docker compose -f compose.yml -f compose.self-hosted.yml up -d --build` depois
de obter a credencial/linha Plow. A CLI adiciona `/public/v1` ao API root; a sua
URL pode precisar terminar em `/api`. O login cloud não garante conexão a uma
instância self-hosted arbitrária.

## Usar sua conta Codex para o modelo

O canal iMessage continua no Plow. O Hermes da base pode usar `openai-codex` como
provedor de inferência, com um login próprio do Posta na mesma conta ChatGPT/Codex.
Esse uso fica sujeito aos limites da conta. A sessão deve ser independente: os
tokens de renovação Codex são de uso único e copiar a sessão do Hermes principal
pode deixar uma das instalações sem acesso após a renovação.

Com o container ativo, inicie a autorização nativa:

```sh
docker compose exec -T --user 10000:10000 agent hermes auth add openai-codex --type oauth --label posta --no-browser
```

Abra o endereço exibido, use sua conta e autorize o código. O login fica no volume
privado do agente. Não copie `auth.json` para o repositório ou para a imagem. Após
confirmar o login, defina em `.env`:

```dotenv
HERMES_PROVIDER=openai-codex
HERMES_MODEL=gpt-6.1-sol
```

Recrie o container com `docker compose up -d`. A base configura o provedor e remove
a rota de inferência Plow; não é necessário alterar seu gateway. Para voltar ao
modelo Plow, use `HERMES_PROVIDER=plow`, remova `HERMES_MODEL` e recrie.

Use um modelo disponível na sua conta. A documentação OpenAI em 2026-10-14 indica
`gpt-6.1-sol` para o lançamento atual e a retirada de GPT-5.5 do Codex nessa data;
a disponibilidade do alvo deve ser confirmada após autenticar o agente.

Fontes: [OpenAI — login por código](https://learn.chatgpt.com/docs/auth#login-on-headless-devices)
e [GPT-6.1 Sol](https://learn.chatgpt.com/docs/models#gpt-61-sol).

## Construir e verificar sem Plow

```sh
docker build --platform linux/arm64 -t plow-postiz-hermes-agent:local .
docker run --rm --user 10000:10000 --entrypoint postiz plow-postiz-hermes-agent:local --version
docker run --rm -i --user 10000:10000 --entrypoint /opt/hermes/.venv/bin/python plow-postiz-hermes-agent:local - < tests/cli_contract.py
```

Em um host Intel use `linux/amd64`. O teste de contrato usa uma API HTTP simulada
dentro do container, com credencial fictícia: não publica nas redes. Ele verifica
o CLI instalado e os payloads; não prova que um modelo Hermes cumprirá todas as
instruções ou que iMessage está conectado. Consulte [evidências](docs/VERIFICATION.md).

Sem identidade Plow configurada, a base estaciona antes de iniciar o gateway. Isso
é comportamento esperado; não desative a validação de identidade para demonstrar
um chat que ainda não foi conectado.

## Publicar o agente

Siga [docs/PUBLISH.md](docs/PUBLISH.md) para registrar no Agent Index, publicar a
imagem e solicitar deploy de um clique à equipe Plow. Nome/slug públicos devem
ser escolhidos antes do registro. A base já envia uso ao Index quando `AGENT_ID`
está configurado; não precisa instalar outro reporter.

Release v2 com onboarding individual: [Posta no Agent Index](https://aiworthusing.com/agent-index/posta) e
[imagem pública no GHCR](https://github.com/users/PuebloAguilar/packages/container/package/posta).
Imagem `linux/amd64`, com pull anônimo verificado. A primeira admissão para deploy
de um clique ainda depende da equipe Plow; os dados e a mensagem estão em
[docs/ADMISSION-MESSAGE.md](docs/ADMISSION-MESSAGE.md).

## Componentes e limites

Base OCI e CLI Plow: Apache-2.0. Hermes: MIT. CLI Postiz distribuído: AGPL-3.0,
instalado sem modificação. Licenças/referências dos componentes adicionados estão
em `licenses/` e [`.references/README.md`](.references/README.md).

As regras de aprovação são persona/skill, não um bloqueio de execução separado.
Imagem genérica não conecta automaticamente as redes de quem a instala. Cada
pessoa autentica seu Postiz; geração de imagens depende das ferramentas dessa
instalação. Publicar na fila não equivale a publicação concluída: o agente consulta
o estado e só informa “publicado” ao obter `PUBLISHED`.
