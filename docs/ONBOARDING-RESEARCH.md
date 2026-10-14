# Onboarding individual do Posta

Pesquisa primária em 2026-10-14. Escopo: persona, skill e CLI oficial Postiz; sem auth server, executor, cadastro próprio ou publicação de teste. Houve somente leitura de documentação, código público, pacote distribuído e schema de ferramentas da imagem local. Não foram criados contas, grants, códigos de login, tokens ou posts reais.

## Regra de produto que prevalece

Cada instalação conecta o **Postiz e as redes da própria pessoa**. Não reutilizar organização, hostname, chave, token, integração, volume ou mídia do criador. A regra 3 da [skill pessoal Postiz](/Users/pueblo/.codex/skills/postiz/SKILL.md:45), que fixa a VPS desse usuário, orienta somente sua operação pessoal. A instrução atual do usuário exige onboarding genérico e prevalece; não copiar essa regra para a imagem pública. Os limites aprovados de persona/skill continuam em [spec](superpowers/specs/2026-10-14-postiz-imessage-design.md) e [AGENTS.md](../AGENTS.md).

## Fontes e diferença entre documentação e pacote

O registry consultado continua com `postiz@2.0.16` como latest. O pacote publicado, não o README de `main`, determina os comandos disponíveis: auth login/status/logout, integrações list/groups/settings/trigger, upload e posts. **Não existem `integrations:connect`, `integrations:me`, `integrations:check` ou um seletor de organização no CLI 2.0.16.** Fonte: [metadata npm](https://registry.npmjs.org/postiz/latest), [tarball distribuído](https://registry.npmjs.org/postiz/-/postiz-2.0.16.tgz), [schema CLI da tag](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/index.ts). O tarball foi lido; a tag é fonte declarada da versão, sem identidade byte a byte comprovada pelo registry, que não informa gitHead.

## Caminho completo recomendado — proposta com componentes existentes

1. **Identificar a pessoa e o modo de Postiz.** Iniciar conexão somente no DM do dono, sob autoridade do plugin Plow. Perguntar se já usa Postiz Cloud ou uma instalação própria. Não tratar ausência de configuração como permissão para escolher o Postiz do criador. Uma instalação limpa não recebe sua chave no ambiente.
2. **Criar ou entrar no Postiz dessa pessoa.** Para Cloud, enviar [cadastro oficial](https://platform.postiz.com/auth) ou [login](https://platform.postiz.com/auth/login). A pessoa preenche dados, aceita termos e escolhe plano diretamente no site. Cloud não tem plano gratuito; a conta precisa de assinatura/trial habilitado. Self-hosted: abrir a URL da instância indicada pela pessoa e entrar/registrar nela; não instalar outra instância nesta versão. Fontes: [quickstart Cloud/self-hosted](https://docs.postiz.com/general/quickstart), [página pública de cadastro](https://platform.postiz.com/auth).
3. **Selecionar organização.** Quem participa de várias organizações escolhe a correta no seletor do topo do dashboard antes de autorizar. O OAuth é vinculado ao `org.id` da sessão autenticada, não a uma organização escolhida pelo agente. Depois, o Posta confirma o ID retornado pelo login e os nomes das redes descobertas com o dono; não muda para outra organização automaticamente. Fontes: [conceitos de organização](https://docs.postiz.com/general/concepts), [selector oficial](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/apps/frontend/src/components/layout/organization.selector.tsx), [autorização vinculada à org](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/apps/backend/src/api/routes/oauth.controller.ts#L172).
4. **Autorizar Postiz no Posta por device flow.** No Cloud, usar `postiz auth:login` já pronto; enviar somente o link de verificação e o código curto exibidos, nunca token/API key. A pessoa autoriza no navegador; o CLI aguarda e salva a credencial no volume individual. Isso conecta Posta ao Postiz, ainda não conecta redes sociais. Fonte: [auth oficial CLI](https://docs.postiz.com/cli/authentication).
5. **Conectar redes da pessoa pelo dashboard.** Após entrar na organização correta, ir a Calendar → Add Channel, escolher a rede, autorizar na rede e concluir passos adicionais como Page, channel ou company. Contas que usam API key/app password são preenchidas pela pessoa no formulário Postiz, não no iMessage. Informar que terminou e rodar `postiz integrations:list` novamente. Fontes: [conectar canal](https://docs.postiz.com/general/channels/connect), [passos de setup](https://docs.postiz.com/general/quickstart).
6. **Confirmar readiness e preferências.** Listagem real deve funcionar e mostrar ao menos uma conta habilitada que o dono reconheça. Coletar voz da marca, público, fuso IANA e destinos preferidos; consultar settings de cada integração escolhida. Salvar preferências usando memória/sessão nativa Hermes. Mostrar uma primeira prévia; não criar `schedule`/`now` antes de aprovação.

Os links de convite Postiz podem conectar a rede de um cliente à organização de quem criou o convite. Esse é outro modelo de produto; **não usar convite da organização do criador** para o onboarding individual Posta. Fonte: [client invite links e destino](https://docs.postiz.com/general/channels/connect#letting-a-client-connect-their-own-account).

## Device flow e operação não bloqueante no Hermes

O CLI 2.0.16 chama `/device/code`, imprime `user_code` + `verification_uri`, tenta abrir o navegador local e passa a consultar `/device/token`. Usa `expires_in`/`interval` da resposta; o servidor oficial de referência configura 15 minutos e polling de 5 segundos. O código OAuth intermediário do Postiz, que não deve ir ao chat, dura 10 minutos. O cliente salva accessToken/apiUrl/organizationId; o arquivo é 0600 e diretório 0700. Fontes: [auth CLI da versão](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/commands/auth.ts), [servidor referência](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/server/index.ts), [validade OAuth](https://docs.postiz.com/oauth).

`postiz auth:login` **não tem `--no-browser` no pacote 2.0.16**. Em Linux headless, sua tentativa de `xdg-open` não abre o navegador do proprietário; o link e o código continuam sendo o caminho de autorização. Não substituir por uma chamada foreground que espera minutos antes de entregar o link. Fonte: [flags CLI](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/index.ts).

A base efetivamente rodando foi inspecionada em `/opt/hermes/tools/terminal_tool.py`: suporta `background=true` e `notify=true`; não tem `persist_on_release` do Hermes mais novo. Proposta de uso nativo:

```text
terminal(command="postiz auth:login", background=true, notify=true)
process(action="log", session_id="<retornado pela ferramenta>")
```

Ler a saída inicial pelo mesmo session_id, enviar link/código ao DM do dono e devolver o controle. Na conclusão ou resposta “pronto”, usar `process poll/log` e depois a descoberta real. Se o dono negar/cancelar, encerrar esse processo. Não iniciar logins paralelos nem criar loops próprios. Se houver timeout, reinício ou processo encerrado, iniciar um novo device flow quando necessário, não tentar ressuscitar o código antigo. Fontes: [terminal/process nativos](https://hermes-agent.nousresearch.com/docs/user-guide/features/tools#background-process-management), [source terminal](https://github.com/NousResearch/hermes-agent/blob/0e427d788d253630d38a3a51cd76849e73cd6925/tools/terminal_tool.py). A disponibilidade na imagem foi verificada por leitura; a duração através de mensagens/restarts e a conclusão de auth real ainda precisam de teste funcional.

## Conferência segura e diagnóstico

`auth:status` imprime os primeiros oito caracteres do token/chave e retorna normalmente mesmo quando diz inválido/não autenticado. Assim, não repetir sua saída crua no chat nem tratar exit 0 como sucesso. Se usado para diagnóstico, remover as linhas `Token:`/`Key:` antes que a saída chegue ao modelo ou ao chat. `integrations:list` confirma acesso com GET real e conserva mensagem/código de erro ao falhar. Fonte: [auth status e logout](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/commands/auth.ts).

| Resultado observado | Interpretação e próximo passo |
|---|---|
| Sem credencial | Oferecer device flow do modo escolhido; não selecionar conta de demonstração |
| HTTP 401, `Invalid OAuth token` / `Invalid API key` | Reautorizar/atualizar a credencial individual no canal seguro |
| `No subscription found` no endpoint Cloud correto | Pode ser assinatura/trial ou organização sem plano; orientar dashboard/billing, não mudar para VPS do criador |
| HTTP 403 | Pode ser autorização, organização/recurso ou policy; ler o body e o endpoint, não diagnosticar genericamente como token expirado |
| Lista vazia | Auth pode estar válida; faltam canais ou foi escolhida outra organização |
| Conta desabilitada / requer reconexão | Corrigir canal no dashboard antes de usá-lo |
| Timeout/5xx/DNS | Informar indisponibilidade e tentar novamente de forma limitada; não refazer grants automaticamente |

O middleware atual retorna `No subscription found` com 401 quando billing está habilitado e a organização não tem subscription. Docs listam Public API/CLI/MCP em todos os planos pagos atuais e Developers em Standard+. Portanto 403 não é prova suficiente de plano errado. Fontes: [middleware real](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/apps/backend/src/services/auth/public.auth.middleware.ts), [Developers](https://docs.postiz.com/general/settings/developers), [planos](https://docs.postiz.com/cloud/plans), [erros API](https://docs.postiz.com/public-api/introduction#errors).

A API atual oferece `/public/v1/me` (org e usuário OAuth) e `/public/v1/social/{provider}` (URL OAuth, com refresh opcional). O segundo também grava state/PKCE no servidor, apesar do verbo GET. Nenhum deles foi chamado nesta pesquisa. O CLI distribuído não expõe esses comandos; o caminho completo dentro do escopo aprovado é dashboard + descoberta CLI, sem novo cliente HTTP. Fontes: [connected account](https://docs.postiz.com/public-api/integrations/me), [OAuth social API](https://docs.postiz.com/public-api/integrations/connect), [implementação](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/apps/backend/src/public-api/routes/v1/public.integrations.controller.ts#L271).

## Reconexão, troca de conta e desconexão

- **Canal social expirado:** Calendar → menu do canal → Reconnect, usando a mesma conta. Reconectar outra identidade cria mismatch com histórico. Para uma identidade diferente, conectar canal novo, redescobrir e obter nova aprovação dos destinos. Posts já falhados não são repetidos automaticamente. Fonte: [reconexão oficial](https://docs.postiz.com/general/channels/manage#reconnecting).
- **Outra organização/conta Postiz:** parar o login pendente, remover o OAuth local quando solicitado, selecionar a organização correta no dashboard, autorizar de novo e redescobrir. CLI não troca de org por flag; token anterior continua vinculado à org que o emitiu. Não usar header superadmin de override. Fontes: [OAuth controller](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/apps/backend/src/api/routes/oauth.controller.ts#L172), [config CLI](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/config.ts).
- **`auth:logout`:** apaga somente o arquivo OAuth local; não revoga grant remoto, não remove chave do ambiente e não desconecta canais sociais. OAuth salvo tem precedência sobre API key/URL de ambiente; após logout, uma chave antiga do ambiente volta a valer. Instalação genérica nunca deve carregar chave do criador como fallback. Para API key em ambiente, remoção requer configuração privada e reinício; não afirmar “desconectado” se discovery ainda autentica. Fonte: [logout/config efetivos](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/src/commands/auth.ts), [precedência](https://docs.postiz.com/cli/authentication).
- **Revogação remota:** o dono usa Settings → Approved Apps. Tokens OAuth não expiram automaticamente, segundo docs. Sair do Posta não cancela posts já agendados no Postiz; isso exige pedido separado e operação explícita nos posts. Fonte: [revoke OAuth](https://docs.postiz.com/oauth#make-api-calls), [agendamento no Postiz](https://docs.postiz.com/general/composer/scheduling).

## Self-hosted: limite exato do fluxo existente

A CLI permite `--auth-server URL`/`POSTIZ_AUTH_SERVER`. Se a própria instância já tem o auth server oficial configurado, usar esse endpoint sem implementar outro. Alternativa: API key da organização dessa pessoa e `POSTIZ_API_URL` correto, provisionados **fora do chat** na configuração privada da instalação. A imagem atual mantém o diretório `.postiz` persistente por symlink do HOME real para o volume; [Dockerfile](../Dockerfile) é a fonte local disso.

Existe conflito entre documentação e código: o [guia de auth server](https://docs.postiz.com/self-host/cli-auth-server) afirma que `cli-auth.postiz.com` também funciona com self-hosted, mas o servidor público fixa FRONTEND/API por configuração e a URL de authorize não pede um resource MCP. O [OAuthService](https://github.com/gitroomhq/postiz-app/blob/25916f12743ea7cc27ebe025f361448f9acfc258/libraries/nestjs-libraries/src/database/prisma/oauth/oauth.service.ts#L266) só permite relay self-hosted para MCP/dynamic/ChatGPT e explicita que tokens relayed não funcionam na Public API; um static app CLI não recebe essa opção normalmente. **Não prometer que o device flow cloud conecta uma VPS arbitrária.** Fonte adicional: [servidor CLI](https://github.com/gitroomhq/postiz-agent/blob/0a5cd5aedaf8edd030895e23642ee51db84c7a66/server/index.ts).

Sem auth server existente ou superfície segura para configuração individual, o Posta pode orientar o dono e preparar copy, mas deve informar que a conexão self-hosted ainda não está concluída. Não pedir chave pelo iMessage, não cadastrar um app/servidor novo e não mover a pessoa para a organização do criador como solução.

## Critério de conclusão e pendências de prova

Onboarding concluído significa: credencial individual válida no endpoint escolhido, organização/destinos reconhecidos pelo dono, ao menos um canal utilizável, settings carregados e preferências essenciais conhecidas. Login aceito, lista vazia ou código enviado isoladamente não satisfazem isso. Nada precisa ser publicado para verificar onboarding.

Ainda não foram testados auth cloud real por pessoa nova, retomada do processo de login entre turnos iMessage, organização múltipla na instalação hosted, revogação/login novamente ou self-hosted com auth server próprio já existente. Essas pendências devem ficar explícitas na entrega e no registro Kata da implementação principal.
