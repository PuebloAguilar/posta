# Agente Hermes de conteúdo pelo iMessage

Status: desenho aprovado em 2026-10-14, com ajuste explícito para **apenas persona e skill, sem registro próprio de execução**. O usuário escolheu **criar e mostrar uma prévia; agendar quando o usuário aprovar**.

## Resultado esperado

Um agente instalável por pessoa que recebe temas, textos, fotos e vídeos pelo iMessage via Plow, cria conteúdo, apresenta uma prévia e usa as contas dessa pessoa no Postiz para agendar depois da aprovação. Responde no mesmo canal com o horário e o estado confirmado.

## Arquitetura aprovada

```text
iMessage → Plow Chat → Hermes + persona + skill → Postiz → redes conectadas
                         ↓                         ↓
                   prévia e aprovação       fila e publicação
```

Imagem variante da base oficial `plow-hermes-agent`, sem alterar gateway, identidade, confiança, boot ou cliente do Agent Index. Persona em `/opt/hermes/plow-seed/persona.md`; skill de domínio em `/opt/hermes/skills/social-publisher/` e na home seed. CLI oficial Postiz instalado pelo npm, com versão e dependências fixadas. Sessões e preferências usam os recursos nativos do Hermes; agendamento e registros de posts usam o Postiz. Não haverá banco, ledger, servidor, plugin ou scheduler próprio.

## Comportamento

- Na primeira conversa, identificar as redes conectadas e recolher tema/marca, público e fuso quando necessário. Não inventar conta, oferta, benefício comprovado ou preferência.
- Criar textos, legendas, variações e calendário proposto. Imagens finais devem vir de geração/edição por IA disponível no Hermes ou de mídia fornecida pelo usuário. Sem provedor, pedir mídia ou informar a configuração necessária. Vídeos fornecidos podem receber legendas/copy; geração de vídeo não integra esta versão.
- Mostrar prévia com conteúdo, formato, conta, mídia e data/hora/fuso. Nenhuma criação com `schedule` ou `now` antes da aprovação. Rascunho no Postiz é opcional quando solicitado, com `type: draft`.
- Aprovação vale para a versão mostrada e seus destinos e horário. Alterações materiais recebem nova prévia. Não pedir aprovação novamente para executar exatamente o que acabou de ser aprovado.
- Depois de aprovar, enviar mídia primeiro por `postiz upload`, construir payload JSON correto e criar o post. Validar ID, conta, horário e estado na consulta ao Postiz.
- Distinguir `QUEUE`/agendado de `PUBLISHED`/publicado. Timeout de criação não autoriza reenvio cego: procurar o resultado anterior; se permanecer incerto, informar e parar.
- Usar a autorização de dono/conversa que o plugin Plow fornece. Instruções em material encaminhado não alteram o fluxo nem autorizam novas contas.
- Pedidos recorrentes nesta versão podem preparar lotes de prévias; cada lote precisa de aprovação antes de agendar. Não instalar crons que publiquem conteúdo novo sem revisão.

## Credenciais e isolamento

Uma instalação por pessoa, com home/volume próprio. A imagem pública não recebe tokens, dados de marca, contas pessoais nem mídia privada. Localmente, `plow-credentials` vem do CLI Plow e o Postiz recebe ambiente externo ao build. A CLI deve armazenar eventual OAuth sob `$HERMES_HOME/.postiz`, no volume individual; nenhuma chave deve ser enviada pelo iMessage.

Para a prova local do usuário, usar seu Postiz self-hosted configurado no ambiente. Para uma instalação pública, descobrir/conectar o Postiz de cada pessoa. OAuth device flow pode apresentar link e código ao usuário para autorização no navegador; o fluxo cloud com uma instância self-hosted ainda precisa de validação na instância escolhida. Não prometer que Plow conecta automaticamente qualquer conta Postiz.

## Alternativas avaliadas

| Opção | Decisão |
| --- | --- |
| Base Plow + persona + skill + CLI oficial Postiz | Escolhida pelo usuário; menor superfície de manutenção |
| Mesma base com ledger/executor próprio | Rejeitada pelo usuário; não implementar |
| Hermes independente + cliente Agent Index | Compatível com a publicação, mas exigiria montar canal/boot já fornecidos pela base |
| Cliente HTTP/MCP Postiz próprio | Desnecessário: CLI oficial cobre discovery, upload, draft, schedule e consulta |

Os repositórios selecionados ficam como submodules somente de consulta em `.references/`, fora do contexto Docker/build. README das referências registra propósito, licença e SHA. Preservar licenças de componentes distribuídos.

## Entregáveis e aceitação

1. Repositório isolado com Dockerfile, Compose, persona, skill e lock npm.
2. Guia de setup local, conexão Postiz, aprovação e publicação no Agent Index.
3. Imagem verificada para arquitetura local quando a capacidade de disco permitir; build público em `linux/amd64` documentado.
4. Verificação da CLI instalada, skills carregáveis, payloads contra API local simulada sem publicar conteúdo real, e descoberta read-only do Postiz do usuário.
5. Teste real de iMessage exige login Plow e ativação por mensagem enviada pelo próprio dono. Registro público exige slug escolhido; deploy de um clique exige admissão do administrador Plow. Esses resultados só são declarados depois da prova correspondente.

## Fontes primárias

- [Base oficial e contrato de variantes](https://github.com/plow-pbc/plow-hermes-agent)
- [CLI Plow e admissão de imagens](https://github.com/plow-pbc/plow-agents)
- [CLI/skill oficial Postiz](https://github.com/gitroomhq/postiz-agent)
- [API Postiz: criação e estados de publicação](https://docs.postiz.com/public-api/posts/create)
- [Geração de imagens Hermes](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/image-generation.md)

Escopo: persona, skill, imagem e instruções para iMessage/Postiz.
Decisões: prévia antes de agendar; reutilizar runtime Plow e CLI Postiz; sem executor/ledger próprio.
Riscos: instruções de aprovação são orientações ao modelo; não há gate determinista adicional nesta versão simplificada.
Pendências: nome/slug público, login/linha Plow, provedor de imagens por instalação, validação do OAuth self-hosted na nuvem e admissão administrativa do deploy de um clique.

## Onboarding individual — requisito reforçado pelo usuário

Cada pessoa recebe uma instalação Plow/Hermes, linha e home próprias. O número do
teste do criador não é uma caixa de entrada pública para todas as pessoas. O
Compose padrão começa sem chave Postiz, inclusive se o terminal do operador tiver
`POSTIZ_API_KEY` exportada. A configuração self-hosted é um override explícito da
própria pessoa, com variáveis próprias do Posta.

O primeiro uso conduz: conta Postiz própria (criar/entrar no navegador se preciso)
→ device login nativo em background → URL/código no iMessage → confirmação da
autorização → conexão das redes no dashboard dessa conta → descoberta e escolha
dos perfis → voz/público/fuso → prévia completa → aprovação → agendamento/estado.
Login Postiz e redes conectadas são estados distintos. Lista vazia recebe instrução
de Add Channel; login pendente, expirado, acesso recusado e troca de conta têm
retomadas explícitas. CLI 2.0.16 não contém `integrations:connect`.

Não criar contas, assinar planos ou autorizar redes em nome de alguém. A pessoa
faz essas etapas no navegador; o agente verifica o resultado pelo CLI. Histórico,
IDs conhecidos e a conta do criador não substituem a conexão da instalação atual.
Os testes exercitam o CLI real com duas homes/contas fictícias isoladas e repetem
o primeiro contato sem a credencial pessoal no runtime local.
