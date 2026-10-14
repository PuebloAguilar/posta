FROM public.ecr.aws/e1h7x4a2/plow-cloud-agents:base-c692e807386993b677de13500ce3a1a323d52b48@sha256:e04a373ed7b8a1f6440e4813eb282c2b6087d31e77c6e5e386ae40a307163d32

LABEL org.opencontainers.image.title="Posta" \
      org.opencontainers.image.description="Hermes persona and skill for previewing and scheduling approved social content on Plow" \
      co.plow.postiz.version="2.0.16"

COPY runtime/package.json runtime/package-lock.json /opt/postiz/
RUN npm ci --prefix /opt/postiz --omit=dev --ignore-scripts --no-audit --no-fund --cache /tmp/postiz-npm-cache \
 && npm cache clean --cache /tmp/postiz-npm-cache --force \
 && ln -s /opt/postiz/node_modules/.bin/postiz /usr/local/bin/postiz \
 && postiz --version \
 && install -d -o 10000 -g 10000 -m 0700 /var/lib/hermes/.postiz \
 && agent_home="$(getent passwd hermes | cut -d: -f6)" \
 && test -n "$agent_home" \
 && if [ "$agent_home" != /var/lib/hermes ]; then \
      ln -s /var/lib/hermes/.postiz "$agent_home/.postiz"; \
    fi

COPY --chown=0:0 persona.md /opt/hermes/plow-seed/persona.md
RUN chmod 0644 /opt/hermes/plow-seed/persona.md
COPY --chown=10000:10000 skills/ /opt/hermes/skills/
COPY --chown=10000:10000 skills/ /var/lib/hermes/skills/
COPY licenses/ /usr/share/doc/plow-postiz/

# Keep the base's /init, plow-init, gateway and Agent Index reporter unchanged.
