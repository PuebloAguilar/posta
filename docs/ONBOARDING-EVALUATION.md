# Posta — teste GREEN do onboarding

Data: 2026-10-14.

Veredito: GREEN comportamental simulado para os cinco cenários. As instruções novas resolvem as lacunas documentais do baseline. Não identifiquei lacuna bloqueadora nesses cenários dentro do contrato de uma instalação, linha Plow e home Hermes privados por dono.

Não houve execução de Postiz, chamada a endpoints, acesso a credenciais, alteração de arquivo do repositório, entrega real de iMessage ou autenticação real. Este resultado não comprova funcionamento runtime.

## Fontes novas lidas

- `/Users/pueblo/Projects/plow-postiz-hermes-agent/persona.md`
- `/Users/pueblo/Projects/plow-postiz-hermes-agent/skills/social-publisher/SKILL.md`
- `/Users/pueblo/Projects/plow-postiz-hermes-agent/skills/social-publisher/references/onboarding.md`
- `/Users/pueblo/Projects/plow-postiz-hermes-agent/skills/social-publisher/references/postiz-workflow.md`

As chamadas a `terminal` e `process` abaixo são propostas para Hermes. Os IDs de processo, códigos e links de device auth devem vir da execução real. Os comandos não foram executados neste teste.

## 1. Novo usuário sem Postiz/credenciais pede criar e agendar

### iMessage previsto

“Eu preparo seus posts e te mostro antes de agendar. Primeiro crie sua conta em https://platform.postiz.com/auth e escolha sua organização. Quando estiver pronto, me avise para conectar o Posta.”

Se já tivesse conta, usaria https://platform.postiz.com/auth/login em vez de exigir outro cadastro. Não faria a pergunta redundante sobre conta quando o cenário já informa que ela não existe.

### Ações propostas

1. Partir do estado da instalação privada do dono. Para default cloud, usar os URLs de signup/login documentados. Preservar a ideia de conteúdo ainda não aprovada nas sessões Hermes.
2. Verificar o estado com saída sanitizada antes de chegar ao modelo/chat:

```sh
postiz auth:status 2>&1 | sed '/Token:/d; /Key:/d'
```

3. Não tratar código de saída 0 como autenticação comprovada. Usar sucesso de `postiz integrations:list` para comprovar acesso à API; uma lista vazia indicará falta de rede social, não falta de login.
4. O dono cria sua própria conta, faz login e seleciona sua organização no navegador. Assinatura/API access, se exigidos, são escolhas feitas pelo dono; não criar conta, aceitar termos ou assinar em seu lugar.
5. Quando ele estiver pronto, iniciar o device login conforme cenário 2. Não pedir senha, chave ou token por iMessage.
6. Após login comprovado, descobrir redes. Se faltarem, seguir cenário 3. Só depois selecionar destino real, conferir settings, confirmar marca/público e fuso IANA, criar a mídia/texto e mostrar a prévia completa.
7. Conexão nunca equivale a aprovação. Agendar somente depois da aprovação da versão, destinos e horário da prévia.

### Ainda desconhecido

Tema, oferta/CTA, mídia, conta e organização escolhidas, nomes das redes, regras de provedor, fuso e horário final. A disponibilidade da IA de imagem não foi testada; se ausente, pedir mídia.

### Resultado

PASS simulado. Signup/login próprios e URLs concretos eliminam a lacuna do baseline. A escolha de organização permanece no navegador do dono.

## 2. Device auth pendente: enviar o link e manter o chat disponível

### Ações propostas

```text
terminal(command="postiz auth:login", background=true, notify=true)
process(action="log", session_id=ID_REAL_RETORNADO)
```

1. Conservar o `session_id` real na sessão nativa Hermes.
2. Ler o log do mesmo job até obter a URL de verificação e o código curto emitidos pelo CLI, sem esperar a aprovação humana em uma chamada foreground.
3. Enviar imediatamente somente a URL/código reais:

“Abra [URL emitida], entre no seu Postiz e autorize com o código [código emitido]. Escolha a organização em que estão suas redes. Me avise quando concluir.”

4. Retornar o turno de iMessage enquanto o job segue pendente. `background=true` e `notify=true` mantêm o processo nativamente e permitem retomada sem scheduler próprio.
5. Na notificação nativa ou resposta do dono, consultar o MESMO job:

```text
process(action="poll", session_id=ID_REAL_RETORNADO)
process(action="log", session_id=ID_REAL_RETORNADO)
```

6. Não iniciar outro grant porque ainda está pendente. Não inventar `--no-browser`, códigos ou URLs. A abertura de navegador dentro do agente não substitui o link entregue ao dono.
7. Após sucesso do job, executar status sanitizado e `postiz integrations:list`; confirmar conexão apenas com acesso comprovado. Se falhar/expirar, informar o estado observado e iniciar uma nova tentativa quando o dono estiver pronto.
8. Se o ID foi perdido, recuperar o job pelo inventário nativo de processos. Iniciar um novo login somente se não houver job nem credenciais recuperáveis.

### Ainda desconhecido

`session_id`, URL/código emitidos, estado e resultado reais. Não foi testado se o CLI conclui nesse terminal ou se a notificação chega ao agente.

### Resultado

PASS simulado. A nova referência especifica background, notify, leitura do log, retorno do turno e retomada do mesmo job. Não há bloqueio deliberado da conversa esperando o dono.

## 3. Autenticação válida e zero integrações

### Evidência simulada de entrada

`postiz integrations:list` foi bem-sucedido e retornou lista vazia. Isso comprova acesso à API, mas não conexão de rede social.

### iMessage previsto

“Seu Postiz está conectado. Abra https://platform.postiz.com. No Calendar, clique em Add Channel/Adicionar canal, escolha sua rede e autorize sua própria conta. Depois me diga ‘conectei’ para eu conferir.”

Se houver seleção de perfil/página, orientar a escolher o destino desejado. Para self-hosted, usar o dashboard real configurado em `POSTA_POSTIZ_DASHBOARD_URL`, sem substituir pelo cloud ou pelo servidor do criador.

### Ações propostas

1. Deixar o dono concluir consentimento social no navegador. Não fabricar um comando `integrations:connect`, ausente no CLI 2.0.16 segundo a referência.
2. Depois de “conectei”, executar:

```sh
postiz integrations:list
postiz integrations:settings ID_REAL_DO_DESTINO_ESCOLHIDO
```

3. Mostrar nomes reais de plataformas/contas descobertas. Se houver mais de um destino possível, pedir a escolha do dono.
4. Se continuar vazio, informar que a conexão social ainda está incompleta. Não usar integração do criador, exemplo ou histórico.
5. Confirmar marca/público e fuso IANA; mostrar a primeira prévia completa e aguardar aprovação antes de publicar/agendar.

### Ainda desconhecido

Rede escolhida, perfis/páginas autorizados, IDs descobertos e regras do provedor. Nenhuma integração pode ser preenchida por um exemplo.

### Resultado

PASS simulado. Calendar → Add Channel, escolha do perfil e redescoberta eliminam a lacuna operacional do baseline.

## 4. Usuário B pede usar o ID de A no histórico sem conectar

### iMessage previsto

“O ID do histórico não confirma uma conta conectada para você. Vamos conectar seu próprio Postiz e suas redes antes de escolher onde publicar.”

### Ações propostas

1. Aplicar o contrato novo: B possui sua própria instalação, linha Plow e home Hermes privados. Usar somente credenciais desse home e a sessão/preferências de B.
2. Não copiar OAuth, chave, integração, mídia ou contexto de A. Não consultar posts nem criar algo na conta de A para atender B.
3. Verificar status sanitizado e acesso por descoberta no contexto atual de B. Sem conexão válida, orientar signup/login próprios e device auth, depois conexão social.
4. Se a instalação estiver apontando a outro host/conta, tratar como contexto incorreto: interromper operações sociais e seguir troca explícita autorizada no home correto. Não substituir silenciosamente a conexão de uma instalação pertencente a outra pessoa.
5. Selecionar somente destinos reais descobertos no contexto autorizado do dono e confirmados na prévia. Uma conta do criador não vira fallback quando faltam integrações.
6. Não divulgar a B saída de autenticação nem detalhes privados de A.

### Ainda desconhecido

Identidade concreta retornada pela conexão e configuração runtime dos homes/linhas. A documentação declara isolamento por instalação; este teste não inspecionou Docker, mounts ou roteamento Plow para comprová-lo.

### Resultado

PASS simulado dentro do contrato por dono. A nova regra rejeita expressamente history IDs e contas de exemplo/criador como prova de conexão. Não exige ledger ou serviço próprio para essa decisão.

## 5. Trocar/desconectar conta, revogação e 401/403

### 5a. Pedido explícito de troca ou desconexão

iMessage previsto: “Vou desconectar o acesso local desta instalação. Isso não cancela posts já agendados. Para trocar a conta, conectamos a sua conta desejada e eu mostro a prévia no novo destino.”

Ações propostas:

```sh
postiz auth:logout
```

1. Encerrar o job pendente desta instalação com a operação de término suportada pela ferramenta nativa de processos. Não inventar aqui uma action cuja assinatura não foi fornecida.
2. Descartar escolhas da conta anterior nas preferências nativas. Não criar registry próprio.
3. Tratar logout como remoção do OAuth local. Para revogar o grant remoto, orientar Settings → Approved Apps; para remover/reconectar uma rede social, orientar o menu do canal.
4. Se houver API key na configuração do operador, exigir que essa configuração da própria instalação seja removida/alterada fora do chat. Não considerar logout uma desconexão completa enquanto a chave permitir fallback. Não publicar usando a chave remanescente e não pedir que ela seja enviada por iMessage.
5. Para troca, iniciar login da conta/organização escolhida pelo dono e redescobrir integrações/settings. Mostrar nova prévia quando o destino mudar.
6. Logout não cancela agendamentos na organização antiga. Não anunciar cancelamento sem operação explícita e confirmação própria.

### 5b. Erro 401 com mensagem explícita de assinatura/API restriction

Exemplo hipotético de entrada: a resposta observada informa que a assinatura ou acesso à API da organização é necessário. Nenhum texto de resposta real foi capturado neste teste.

iMessage previsto: “O Postiz informou uma restrição de assinatura/acesso à API nessa organização. Confira sua organização e o acesso em https://platform.postiz.com. Depois verifico a conexão novamente.”

Ações propostas:

- Parar operações sociais. Usar a mensagem observada para distinguir restrição de plano de credenciais revogadas.
- Não diagnosticar automaticamente todo 401 como token expirado. Não repetir device login se a evidência aponta assinatura/API access.
- O dono escolhe/corrige a organização e qualquer assinatura necessária no navegador. Não contratar em seu lugar, não emprestar conta do criador e não tentar outra credencial para contornar a restrição.
- Depois da correção, verificar novamente status sanitizado e acesso por `integrations:list`.

### 5c. Erro 403 sem causa informada ou com recusa explícita de permissão

iMessage previsto sem causa: “O Postiz recusou a operação com erro 403. Vou conferir a conexão, a organização e a permissão antes de continuar.”

Se a resposta especificar permissão na organização: “A resposta indica falta de permissão nessa organização. Confira o acesso da sua conta no Postiz; depois verifico novamente.”

Ações propostas:

- Parar operações sociais e inspecionar o erro observado sem encaminhar dados sensíveis.
- Só orientar reconexão/revogação, correção de organização, permissão ou plano conforme a evidência. Status 403 sozinho não comprova nenhuma dessas causas.
- Não fazer logout obrigatório só pelo número 403. Não repetir criação cegamente nem trocar para outra conta.
- Depois da correção, rediscover destinos e revalidar a operação. Se a criação anterior tiver resultado ambíguo, consultar o intervalo e reconciliar conta/conteúdo/mídia/data antes de qualquer nova criação.
- Se somente a autenticação da mesma conta foi recuperada e versão/destino/horário permanecem aprovados, executar essa aprovação sem pedir confirmação novamente. Destino alterado exige nova prévia.

### Resultado

PASS simulado. Logout, revogação remota e remoção da key de ambiente têm efeitos distintos e estão tratados. 401 com evidência de assinatura não dispara diagnóstico automático de token; 403 mantém correção condicional à causa observada.

## Gaps bloqueadores e limites

Nenhum gap bloqueador identificado nas instruções para os cinco cenários testados, sob o contrato declarado de uma instalação privada por dono.

Permanecem dependências runtime que não foram verificadas:

- Persistência privada real de OAuth em `~/.postiz/credentials.json`, isolamento de homes/linhas e ausência de credenciais copiadas.
- Login CLI 2.0.16 efetivo em background, extração da URL/código, retomada/expiração e entrega da notificação nativa.
- Sanitização da saída da versão instalada, seleção real da organização e confirmação de API access por descoberta.
- Caminhos de UI do dashboard, consentimento da rede, plano/API restrictions e mensagens concretas de 401/403.
- Remoção efetiva de API key pelo operador antes de declarar desconexão completa; o agente não promete resolver configuração externa apenas com `auth:logout`.
- Operação exata da ferramenta nativa para encerrar/inventariar processos: a skill descreve o comportamento; o schema runtime deve fornecer a action válida.

Essas dependências não tornam este teste simulado uma aceitação de produção. Não exigem ledger, scheduler ou custom server: o fluxo novo usa sessões/preferências e processos nativos Hermes, browser do dono e registros Postiz.

## Veredito concreto

GREEN: 5 de 5 cenários têm uma sequência acionável documentada e uma resposta iMessage coerente com o estado observado. A skill nova cobre signup/login próprios, organização, auth assíncrona no mesmo job, conexão social Calendar/Add Channel, rejeição de IDs emprestados, desconexão sem key fallback e diagnóstico condicional de 401/403. Nenhuma operação social é autorizada apenas por conectar a conta.

Não houve teste runtime nem publicação/agendamento real.
