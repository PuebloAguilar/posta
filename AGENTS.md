# Plow Postiz Hermes agent

Leia `docs/superpowers/specs/2026-10-14-postiz-imessage-design.md` antes de mudar o escopo. O usuário escolheu apenas persona e skill, com prévia antes de agendar; não adicionar registro de execução, scheduler ou cliente HTTP próprio.

A base oficial é dona do boot, gateway, identidade, confiança Plow e Agent Index. Este projeto é dono da persona e da skill de publicação. Referências em `.references/` são submodules somente de consulta e ficam fora do build.

Nunca incluir tokens, dados de usuário, contas sociais ou mídia privada no Git ou na imagem. Validar a conta e o estado pelo Postiz; criação na fila não prova publicação.

Use Kata no projeto `plow-postiz`. Não instalar hooks RoboRev neste projeto. Registre execução e limites reais; um teste com API simulada não prova iMessage ou publicação externa.
