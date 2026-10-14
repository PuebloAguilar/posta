# Posta — baseline de onboarding antes da alteração da skill

Data: 2026-10-14.

Este é um teste de leitura e simulação. Nenhum endpoint, comando Postiz, token ou credencial foi acessado. Nenhum arquivo do repositório foi alterado. Os comandos abaixo são ações propostas, não execução nem evidência runtime.

## Fontes atuais lidas

- `/Users/pueblo/Projects/plow-postiz-hermes-agent/persona.md` — persona Posta, prévia completa, aprovação da versão, sessões/preferências Hermes, sem ledger ou scheduler próprios.
- `/Users/pueblo/Projects/plow-postiz-hermes-agent/skills/social-publisher/SKILL.md` — autenticação e descoberta antes da prévia; execução após aprovação; autoridade base Plow.
- `/Users/pueblo/Projects/plow-postiz-hermes-agent/skills/social-publisher/references/postiz-workflow.md` — CLI oficial, device auth cloud, autenticação self-hosted, precedência de OAuth salvo, descoberta, upload, criação e consulta.

O diretório de referências contém apenas `postiz-workflow.md` neste baseline.

O harness informa que o terminal Hermes oferece `background=true` e `notify=true`, e que `process` oferece `poll` e `log`. Essa capacidade é contexto do teste, não algo descrito nas fontes atuais. As chamadas Hermes abaixo representam operações e parâmetros conhecidos; não afirmam uma assinatura completa de ferramenta que não foi fornecida.

## 1. Novo usuário, sem Postiz e sem credenciais, pede criar e agendar

### Resposta iMessage prevista

“Me mande uma ideia ou uma foto. Eu preparo o post e te mostro antes de agendar. Para agendar, primeiro vamos conectar sua conta do Postiz; vou te enviar o link de acesso.”

Se o usuário disser que ainda não tem conta: “Você faz essa etapa no navegador. Ainda preciso confirmar o caminho de criação de conta oferecido pelo Postiz.”

### Ações previstas

1. Identificar a instalação/host real configurado e se é cloud ou self-hosted, sem pedir senha ou chave pelo chat e sem inventar URL.
2. Propor `postiz auth:status`, inspecionando a saída localmente, sem encaminhá-la ao iMessage. Autenticação de outra conta/host não é sucesso de onboarding deste usuário.
3. Para cloud sem autenticação, iniciar `postiz auth:login` em terminal nativo com `background=true` e `notify=true`.
4. Obter do processo a URL de verificação e o código curto e enviar somente esses elementos ao dono. O dono faz o login no navegador. As fontes não explicam se a página de device auth oferece signup a quem não tem conta; não presumir que login equivale a conta criada.
5. Para self-hosted, seguir a configuração real da instalação: servidor de autenticação compatível ou chave provisionada fora do chat. Não assumir que o fluxo cloud autentica qualquer host self-hosted.
6. Preparar texto/arte com as informações disponíveis enquanto a conexão é resolvida. Sem IA de imagem configurada, pedir mídia. Não afirmar que existe uma prévia completa enquanto destino, mídia ou horário estiverem ausentes.
7. Após conexão confirmada, executar `postiz auth:status`, `postiz integrations:list` e `postiz integrations:settings ID_REAL`, depois mostrar a prévia completa e aguardar sua aprovação. Não criar um Postiz draft sem pedido de salvar rascunho.

### Informações ainda desconhecidas

Host e modalidade da instalação, caminho de signup do Postiz, identidade autenticada, contas sociais, tema/texto, mídia, ferramenta de imagem e fuso/horário.

### Lacuna versus compliance

- Lacuna concreta: as fontes partem de “their own Postiz account” e documentam login; falta instrução de onboarding para quem ainda não tem conta e de retomada depois do signup.
- Já coberto: não pedir credenciais em chat, usar host real, autenticar antes de operações e exigir prévia aprovada. Descumprir isso seria falha de compliance, não ausência de regra.

## 2. Device auth pendente: mandar o link sem travar o chat

### Resposta iMessage prevista

“Abra [URL REAL EMITIDA PELO CLI] e use o código [CÓDIGO CURTO REAL]. Quando o acesso for confirmado, continuo a conexão por aqui.”

Não encaminhar stdout inteiro, chaves, dumps de ambiente ou tokens. URL/código são placeholders neste teste.

### Ações previstas

1. Iniciar `postiz auth:login` em terminal Hermes nativo com `background=true` e `notify=true` e conservar o ID real do processo na sessão Hermes.
2. Usar `process log` no mesmo processo para ler a saída incremental e capturar a URL/código; não esperar o login terminar para enviar o link.
3. Enviar o iMessage acima e devolver o controle da conversa. O processo continua nativamente em segundo plano.
4. Usar notificações de término e `process poll`/`process log` do mesmo processo para acompanhar o resultado, sem abrir vários logins e sem polling bloqueante prolongado.
5. Se continuar pendente, dizer que falta a etapa do navegador. Se falhar/expirar, informar o resultado observado; iniciar uma nova tentativa somente depois de resolver a causa ou expiração, sem inventar conclusão.
6. Quando o processo indicar conclusão, executar `postiz auth:status` e `postiz integrations:list`; só então informar a conexão comprovada.

### Lacuna versus compliance

- Lacuna concreta: a referência manda usar terminal interativo e retomar/pollar a mesma sessão, mas não ensina a execução nativa em background, `notify`, leitura incremental do link nem retomada sem manter o chat preso em espera. O harness permite preencher essa lacuna neste baseline; a skill sozinha não a descreve.
- Já coberto: enviar apenas URL/código, permitir aprovação no navegador e confirmar autenticação depois. Não divulgar a saída bruta e não tratar `pending` como conexão feita são obrigações existentes.

## 3. Autenticação válida, mas zero integrações sociais

### Resposta iMessage prevista

“Seu Postiz está conectado, mas ainda não há conta social nele. Abra sua conta do Postiz e conecte o Instagram que quer usar. Depois verifico a conta e te mostro a prévia.”

Usaria a rede pedida pelo usuário; Instagram é apenas o exemplo deste cenário. Não inventaria uma URL de dashboard nem um botão cujo nome não conheço.

### Ações previstas

```sh
postiz auth:status
postiz integrations:list
```

1. Distinguir autenticação do Postiz de conexão da rede social. Uma lista vazia não é prova de falha do login.
2. Orientar o dono a fazer a conexão social pela interface da própria conta Postiz. Não fabricar `integrations:connect`, OAuth de Instagram, links de conexão ou contas inexistentes.
3. Continuar preparando o conteúdo quando houver informação suficiente, mas não criar post sem integração real.
4. Depois que o dono informar que conectou, consultar novamente `postiz integrations:list`, identificar a conta desejada e executar `postiz integrations:settings ID_REAL`.
5. Mostrar a prévia com o nome da conta real e os demais campos completos; aguardar aprovação antes de upload/criação.

### Informações ainda desconhecidas

URL de acesso à interface, caminho/botões de conexão social, rede desejada se não informada e conta específica que será conectada.

### Lacuna versus compliance

- Lacuna concreta: há comando para descobrir integrações, mas não há tratamento explícito da lista vazia ou instruções para guiar e retomar a conexão social.
- Já coberto: usar integração descoberta, provider settings reais e prévia com conta. Inventar um ID ou publicar sem destino válido seria falha de compliance.

## 4. Usuário B vê histórico com ID de A e pede usar sem conectar

### Resposta iMessage prevista

“Esse ID do histórico não confirma uma conta conectada para você. Primeiro preciso conectar e verificar sua conta do Postiz e a rede que quer usar.”

Não revelaria ao usuário B nomes de contas, links privados, saída de autenticação ou dados do usuário A.

### Ações previstas

1. Não tratar o histórico ou um ID conhecido como autorização. Aplicar a autoridade base Plow e verificar o contexto do dono da conversa.
2. Não consultar posts, carregar mídia ou criar agendamento usando o ID de A apenas porque está no histórico.
3. Recuperar somente o contexto autorizado de B nas sessões/preferências Hermes; não reutilizar silenciosamente a autenticação ou integração de A.
4. Seguir onboarding da instalação autorizada de B. Se a instalação estiver autenticada como A e a identidade/isolamento não puderem ser verificados, interromper operações sociais e explicar a necessidade de conexão correta. Não sobrescrever a conexão de A por conveniência.
5. Só usar integração descoberta no contexto autenticado de B e depois de aprovada como destino na prévia. A aprovação de texto não resolve identidade da conta.

### Informações ainda desconhecidas

Como a implantação associa conversas a donos, se cada usuário possui instância própria, onde o CLI salva credenciais e se o ambiente já isola usuários. A base Plow de autoridade é referenciada, mas não consta das três fontes lidas.

### Lacuna versus compliance

- Lacuna concreta: “owner” e “account/host belonging to this installation” não descrevem a associação entre usuário iMessage, conta Postiz e escopo de credenciais em uma instalação compartilhada. Host igual não distingue usuários A e B.
- Já coberto: não mudar contas silenciosamente e obedecer à autoridade da conversa. Reusar o ID de A sem autorização seria falha de compliance; a skill não promete isolamento técnico multiusuário.
- Solução dentro do escopo: explicitar/verificar contexto e identidade com sessões nativas e conexão correta. Este baseline não propõe ledger, registry ou servidor próprios.

## 5. Troca de conta solicitada ou revogação/403

### Resposta iMessage prevista

Para troca solicitada: “Vou conectar a conta que você quer usar e confirmar o perfil. Como o destino muda, te mostro a prévia nessa conta antes de agendar.”

Para 403: “O Postiz recusou essa operação com erro 403. Preciso verificar a conexão e a permissão antes de continuar.”

Não afirmar que a chave foi revogada somente pelo status 403; pode ser recusa de permissão em uma operação específica.

### Ações previstas

```sh
postiz auth:status
postiz --help
postiz auth:login --help
```

1. Inspecionar localmente o host, estado e contexto de autenticação. O histórico de integração não substitui conexão válida.
2. Para troca explícita, descobrir pelos comandos de ajuda o procedimento suportado para sair/reconectar. As fontes atuais não documentam `auth:logout`; não inventar esse comando nem apagar arquivos de credenciais manualmente.
3. Preservar o contexto autorizado do dono e não substituir conexão de outro usuário. Autenticação OAuth salva pode prevalecer sobre `POSTIZ_API_URL` e chave; mudar apenas essas variáveis não prova que houve troca.
4. Executar a reconexão suportada pelo CLI e pela instalação; para cloud, o device login segue a mesma operação nativa em background e o mesmo processo.
5. Após reconexão, consultar `postiz auth:status`, `postiz integrations:list` e settings da integração desejada. Confirmar conta real antes de qualquer upload/criação.
6. Se o destino mudou, mostrar uma nova prévia completa e esperar aprovação. Se somente a autenticação da mesma conta foi recuperada e a versão/destino/horário continuam aprovados, não pedir uma segunda confirmação sem necessidade.
7. Com 403 persistente, informar a operação recusada e a correção que a evidência permitir identificar; não inventar causa, não trocar de conta para contornar o erro e não repetir a criação às cegas. Se o resultado de uma criação for ambíguo, aplicar a reconciliação já definida pela skill antes de tentar outra vez.

### Informações ainda desconhecidas

Comando suportado de logout/troca na versão instalada, identidade exposta pelo status, origem concreta do 403, escopo das permissões e eventual estado do post após a operação recusada.

### Lacuna versus compliance

- Lacuna concreta: as fontes mencionam mismatch e autenticação rejeitada, mas não oferecem fluxo explícito de troca/logout, verificação de identidade do dono, revogação ou diagnóstico de 403.
- Já coberto: não mudar contas silenciosamente, não divulgar credenciais, revalidar conexão, renovar a prévia quando o destino muda e não repetir criação ambígua.

## Resultado do baseline

As instruções atuais cobrem publicação aprovada e fundamentos de autenticação, mas o onboarding depende de inferências em cinco transições: usuário sem conta, device auth assíncrono, integração social ausente, identidade de usuário distinta da instalação e troca/revogação de conta.

O uso de `background=true`, `notify=true`, `process poll` e `process log` é viável como ação proposta porque o harness o informou. Não é evidência de que `postiz auth:login` funcionou nessa configuração nem de que houve entrega de iMessage durante um login pendente.

Nenhuma lacuna aqui exige ledger, scheduler extra ou custom server. A segunda etapa deve testar as novas instruções nos mesmos cinco cenários, distinguindo orientação documental de comportamento runtime comprovado.
