# Postiz pelo iMessage — agente Hermes no Plow

Mande uma ideia, foto ou vídeo pelo iMessage. O agente prepara o conteúdo, mostra
uma prévia e agenda nas suas redes pelo Postiz depois da sua aprovação.

Uma imagem por pessoa, com contas e preferências próprias. Esta versão contém
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

Configure `POSTIZ_API_URL`, `POSTIZ_API_KEY` e `AGENT_TIMEZONE` no ambiente ou em uma
cópia privada de `.env.example` chamada `.env`. Use o endereço da sua instância:
o CLI acrescenta `/public/v1`, então um host self-hosted exposto sob `/api` precisa
desse prefixo na URL. Não use credenciais cloud para uma organização self-hosted.

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
linha. Se você usa uma API key no ambiente, a conexão Postiz já estará disponível.
Se usa OAuth, peça “conectar meu Postiz”; o agente inicia o device flow e envia o
link/código para você autorizar no navegador. OAuth para uma instância self-hosted
precisa do auth server compatível dela; o fluxo hosted para hosts arbitrários não
foi comprovado.

Não envie chaves pelo iMessage. O agente roda `auth:status` sem devolver sua saída
bruta ao chat. Uma credencial OAuth salva tem precedência sobre ambiente: confira
que ela pertence ao host/organização desejados antes de trocar a configuração.

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

## Componentes e limites

Base OCI e CLI Plow: Apache-2.0. Hermes: MIT. CLI Postiz distribuído: AGPL-3.0,
instalado sem modificação. Licenças/referências dos componentes adicionados estão
em `licenses/` e [`.references/README.md`](.references/README.md).

As regras de aprovação são persona/skill, não um bloqueio de execução separado.
Imagem genérica não conecta automaticamente as redes de quem a instala. Cada
pessoa autentica seu Postiz; geração de imagens depende das ferramentas dessa
instalação. Publicar na fila não equivale a publicação concluída: o agente consulta
o estado e só informa “publicado” ao obter `PUBLISHED`.
