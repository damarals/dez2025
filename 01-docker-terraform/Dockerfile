FROM sunpeek/poetry:py3.11-slim

ENV PYTHONUNBUFFERED=1

ARG USERNAME=zoomcamp
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update && apt-get install -y \
    gnupg \
    software-properties-common \
    curl \
    wget \
    && wget -O- https://apt.releases.hashicorp.com/gpg \
        | gpg --dearmor \
        | tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null \
    && echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
            https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
        | tee /etc/apt/sources.list.d/hashicorp.list \
    && apt-get update \
    && apt-get install -y terraform \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

ENV PATH=/root/.local/bin:/home/$USERNAME/.local/bin:$PATH

USER $USERNAME

WORKDIR /home/zoomcamp/app

RUN poetry config virtualenvs.in-project true \
    && poetry config virtualenvs.prompt "venv"

CMD ["tail", "-f", "/dev/null"]