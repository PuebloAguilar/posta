# Seu Posta, suas contas

Cada instalador recebe uma identidade/linha Plow e um volume Hermes próprios.
A imagem é comum; credenciais, conversas e redes são da pessoa que instala.
O default não inclui API key Postiz e ignora a chave Postiz do terminal do operador.
O número de teste do criador não é uma linha pública compartilhada.

## Primeiro uso pelo iMessage

| Você | Posta |
| --- | --- |
| “Oi, quero conectar minhas redes.” | Verifica a conexão desta instalação e pergunta se você já tem Postiz. |
| “Ainda não.” | Envia https://platform.postiz.com/auth para criar sua própria conta; você escolhe organização/plano. |
| “Já entrei no meu Postiz.” | Inicia o login nativo em background e envia o link/código reais no iMessage. |
| Autoriza no navegador e avisa “pronto”. | Confere acesso ao Postiz; mantém o chat disponível enquanto o login está pendente. |
| Ainda não conectou uma rede. | Orienta Calendar → Add Channel e autorização da sua conta/página social. |
| “Conectei.” | Consulta os perfis, mostra os nomes e confirma seus destinos, marca/público/fuso. |
| Envia tema/mídia. | Mostra a prévia completa. |
| Aprova essa versão. | Envia a mídia ao seu Postiz, agenda e verifica conta/data/estado. |

Login Postiz e rede social conectada são etapas diferentes. Quem tem várias
organizações deve escolher a correta no dashboard antes de autorizar o device
flow; a autorização pertence a essa organização. Acesso API/billing depende do
Postiz escolhido e deve ser resolvido diretamente pela pessoa no site.

## Retomar ou trocar

- Código expirado: peça um novo link. O agente não considera uma autorização
  pendente como conexão concluída e não inicia vários logins ao mesmo tempo.
- Rede ausente/desconectada: adicione/reconecte no seu dashboard e diga ao agente
  para conferir novamente.
- Conta/organização diferente: peça para trocar; saia do OAuth local, selecione a
  organização no navegador e autorize de novo. Os destinos são redescobertos.
- Para revogar remotamente, use **Settings → Approved Apps** no seu Postiz.
  Logout do agente apenas remove OAuth local. Ele não remove canais nem cancela
  posts que já estavam agendados na organização anterior.
- Em modo de API key self-hosted, remover acesso também exige retirar essa chave
  da configuração privada da instalação e recriar o container. Nunca envie a
  chave pelo iMessage.

## Limites de implantação

O deploy de um clique exige admissão da equipe Plow. Enquanto isso, o setup local
do README permite obter sua linha com a CLI Plow e iniciar sua instalação.
Em um upgrade de uma instalação de teste já existente, uma conversa antiga pode
continuar usando o prompt anterior. Use o comando nativo `/new` e confirme uma
vez para iniciar o novo fluxo; as sessões anteriores continuam arquivadas pelo
Hermes. Instalações novas já começam com a persona e skill atuais.
Self-hosted exige um auth server compatível já existente ou a configuração
individual explícita em `compose.self-hosted.yml`; o Posta não cria um servidor
de autenticação nem usa a organização do criador como alternativa.

Fontes: [conta/setup](https://docs.postiz.com/general/quickstart),
[conectar canais](https://docs.postiz.com/general/channels/connect),
[autenticação CLI](https://docs.postiz.com/cli/authentication),
[organizações](https://docs.postiz.com/general/concepts).
