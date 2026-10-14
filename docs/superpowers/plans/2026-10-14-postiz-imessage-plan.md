# Postiz iMessage Implementation Plan

> **For agentic workers:** executar inline nesta sessão, com revisão de skill e revisão final independentes conforme as skills writing-skills e requesting-code-review. O usuário autorizou persona e skill; não adicionar executor/ledger.

**Goal:** entregar uma imagem Hermes Plow que cria prévias no iMessage e agenda conteúdo aprovado pelo CLI oficial Postiz.

**Architecture:** persona e uma skill de domínio sobre a base oficial. Postiz cuida das contas, upload e agendamento; sessões Hermes preservam o contexto. Segredos entram por instalação e ficam fora do build.

**Tech Stack:** Plow Hermes base OCI, Docker Compose, npm postiz 2.0.16, Markdown e Python stdlib apenas para verificação.

## Global Constraints

- Prévia e aprovação antes de `schedule` ou `now`.
- Apenas persona e skill; sem registro próprio de execução, banco, plugin ou scheduler.
- Referências como submodules em `.references/`, fora do build.
- Não embutir credenciais ou dados pessoais na imagem pública.
- Não relatar publicação ou iMessage real sem teste correspondente.

## Task 1: Referências e dependências

- [x] Registrar Kata e baseline da skill sem conhecimento Postiz específico.
- [x] Adicionar `plow-hermes-agent`, `plow-agents` e `postiz-agent` como submodules rasos. Registrar `git rev-parse HEAD` e licença em `.references/README.md`.
- [x] Fixar a imagem base por digest publicado, e instalar `postiz@2.0.16` em `runtime/package.json` com lock via `npm install --package-lock-only --ignore-scripts --cache /tmp/plow-postiz-npm-cache`.

## Task 2: Persona e skill

- [x] Criar `persona.md`: função, voz e prévia/aprovação, sem repetir regras de identidade/trust da base.
- [x] Criar `skills/social-publisher/SKILL.md` e `references/postiz-workflow.md`: auth, descoberta, mídia, formato, payload, approval, status e reconciliação de timeout.
- [x] Rodar os seis cenários baseline com a skill e comparar; corrigir lacunas confirmadas.

## Task 3: Container e setup

- [x] Criar Dockerfile que copia persona, ambas seeds da skill e instala o npm lock em `/opt/postiz`; preservar `/init` da base.
- [x] Criar Compose com `plow-credentials`, ambiente Postiz e home persistente; credenciais OAuth sob home persistente.
- [x] Criar README e `docs/PUBLISH.md` com login/linha reais, Agent Index embutido, imagem pública amd64 e admissão Plow.
- [x] Verificar o tamanho da base antes do pull; preservar trabalho e dados existentes se faltar espaço. Não executar prune/limpeza global.

## Task 4: Prova e revisão

- [x] Executar verificação da skill/frontmatter e `docker compose config --quiet` com credencial fictícia fora do checkout.
- [x] Construir a imagem se couber no disco e executar `postiz --version`, `--help`, discovery e paths de persona/skill com entrypoint de inspeção.
- [x] Exercitar os payloads da documentação com o CLI real contra HTTP local simulado. Confirmar draft/schedule/now, upload→URL e endpoint `/api/public/v1` sem escrita externa.
- [x] Fazer discovery read-only do Postiz real com saída sanitizada, sem copiar segredo para artefatos.
- [x] Revisar diff e arquivos de build por referência/segredos; revisão independente; registrar limites em `docs/VERIFICATION.md` e Kata.
- [x] Commit local da entrega verificada; não presumir login Plow, publicação do Index, imagem pública ou teste iMessage.

## Task 5: Onboarding completo com contas individuais

- [x] Pesquisar auth/social connection na versão npm instalada e executar baseline
  dos cinco estados antes da alteração da skill.
- [x] Adicionar prova de Compose contra uma chave fictícia herdada do ambiente;
  observar a falha e remover essa herança do default. Self-hosted usa override
  explícito com variáveis POSTA próprias; atualizar `.env.example` e README.
- [x] Adicionar `references/onboarding.md` com primeiro uso, login em background,
  conexão social pelo dashboard, confirmação de destinos, troca/logout e erros.
  Atualizar os triggers da skill e a persona para usar essa referência.
- [x] Exercitar device login e descoberta do CLI real com duas homes/contas
  fictícias, pendência, persistência, logout e autenticação recusada.
- [x] Repetir cenários com a nova skill e revisar os riscos de contas/credenciais.
- [x] Recriar somente o runtime Posta sem a chave pessoal; validar primeiro
  contato real sem concluir autorização de conta alheia ou publicar conteúdo.
- [x] Publicar imagem v2, provar pull anônimo e atualizar o handoff de admissão.
