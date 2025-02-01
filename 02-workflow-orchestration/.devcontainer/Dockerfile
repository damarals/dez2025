FROM sunpeek/poetry:py3.11-slim

ENV PYTHONUNBUFFERED=1

ARG USERNAME=zoomcamp
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Configuração do usuário
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Configuração do ambiente Python
USER $USERNAME
WORKDIR /home/zoomcamp/app

RUN poetry config virtualenvs.in-project true \
    && poetry config virtualenvs.prompt "venv"

# Instalação de dependências do Python
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root

CMD ["tail", "-f", "/dev/null"]