# Onboarding v2 — evidência e limites

2026-10-14. Requisito reforçado: cada instalador conecta suas próprias contas.
Fluxo e escolhas em [ONBOARDING.md](ONBOARDING.md) e
[ONBOARDING-RESEARCH.md](ONBOARDING-RESEARCH.md).

| Prova | Resultado |
| --- | --- |
| Default Compose com chave/URL de operador fictícias | RED herdou a chave na v1; GREEN ignora ambas na v2 |
| Runtime local após recriar | Sem chave/URL Postiz no ambiente, sem chave no `.env` da home e sem OAuth salvo |
| CLI oficial, duas homes/contas fictícias | PASS pending/success, API/organização próprias, persistência 0600/0700, rejeição isolada e logout sem afetar a outra conta |
| Mesma fixture dentro da imagem v2 amd64 | PASS sem rede externa e sem credenciais reais |
| Skill/frontmatter da imagem v2 | PASS |
| Cinco cenários de instruções | Baseline encontrou lacunas; avaliação GREEN 5/5, simulação independente |
| Revisão independente | Corrigida ordem de parar login antes do logout; sem achados abertos |
| Sync nativo de skills | Revisor validou seed limpa, upgrade pristine e preservação de customizações sem rede |
| Primeiro uso real | Sessão nova apresentou cadastro próprio em platform.postiz.com; nenhum destino do criador foi usado |
| Device flow real pelo iMessage | `terminal` background=true/notify=true, `process_manage` log; URL/código real entregues sem bloquear o chat |
| Cancelamento real | Job encerrado com exit -15 antes do logout; status não autenticado, zero jobs e zero OAuth salvo |
| Distribuição v2 | GHCR public e pull anônimo amd64 pelo digest do handoff PASS |

A primeira tentativa de teste usou a conversa v1 que ainda tinha o prompt
persistido anterior e afirmou, pelo histórico, que a conta do criador estava
conectada. O ambiente já estava sem chave. A inspeção confirmou SOUL atualizado
e prompt da sessão antigo. O comando nativo `/new`, confirmado uma vez, criou a
sessão `20261014_142103_0be49175`, com parent da sessão anterior arquivada; ela
carregou a persona nova e conduziu o onboarding. Nenhum runtime da base foi alterado.

O primeiro texto de cadastro ainda acrescentou detalhes de UI/valores de memória;
a referência final v2 usa um texto explícito que remete organização/plano/trial
ao site atual, sem prometer conta cloud grátis. A mudança final do texto foi
verificada na imagem, mas essa variante de copy não teve outra resposta real.

Não foram concluídos login/consentimento social de uma pessoa nova, seleção de
múltiplas organizações ou agendamento real nessa nova conta. O device login real
foi interrompido antes da autorização. Fixtures comprovam o CLI com contas
fictícias, não credenciais de clientes. Cada pessoa ainda deve fazer o consentimento
no navegador. Self-hosted arbitrário não é prometido pelo auth server cloud.

A primeira admissão Plow e o smoke de uma instalação cloud permanecem externos.
Persona/skill orientam o modelo; não foi adicionado gate, auth server ou ledger.
