# Polyglot Poisoning — participant kit in a container.
#
#   docker build -t polyglot-poisoning .
#   docker run --rm polyglot-poisoning                      # runs the setup check
#   docker run --rm polyglot-poisoning probe.py samples/    # scores the sample pack
#
# Standard library only: no pip install, no model, no network at runtime.
# Contains only the public participant kit (see .dockerignore).
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd --create-home --uid 10001 hunter
WORKDIR /home/hunter/polyglot-poisoning
COPY --chown=hunter:hunter . .
USER hunter

ENTRYPOINT ["python3"]
CMD ["tests/check_setup.py"]
