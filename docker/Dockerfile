FROM ubuntu:24.04
# For ML/GPU workloads, replace the above line with:
# FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update && apt-get install -y --no-install-recommends \
        # Basic tools
        git \
        curl \
        wget \
        ca-certificates \
        # Image processing dependencies
        libgl1 \
        libglib2.0-0 \
        # Utilities
        zip \
        unzip \
        procps \
        nano \
        sudo \
        gosu \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Tokyo

ARG USER_UID
ARG USER_GID
ARG USER_NAME
ARG GROUP_NAME=${USER_NAME}

ENV HOME=/home/${USER_NAME}

RUN userdel -r ubuntu 2>/dev/null || true \
    && groupadd --gid ${USER_GID} --non-unique ${GROUP_NAME} \
    && useradd -m --no-log-init --uid ${USER_UID} --gid ${USER_GID} --groups sudo --base-dir /home --shell /bin/bash ${USER_NAME} \
    && touch ${HOME}/.sudo_as_admin_successful \
    && printf '%s\n' '%sudo ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/90-sudo-group-nopasswd \
    && chmod 0440 /etc/sudoers.d/90-sudo-group-nopasswd \
    && visudo -cf /etc/sudoers.d/90-sudo-group-nopasswd

RUN chown -R ${USER_UID}:${USER_GID} /home

USER ${USER_NAME}
ARG REPO_NAME
ENV WORK_DIR=${HOME}/workspace/${REPO_NAME}
ENV PYTHON_VERSION=3.14.2 \
    UV_PROJECT_ENVIRONMENT=${HOME}/.venv
WORKDIR ${WORK_DIR}

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="${UV_PROJECT_ENVIRONMENT}/bin:${HOME}/.local/bin:${PATH}"

COPY --chown=${USER_UID}:${USER_GID} pyproject.toml uv.lock README.md ./

RUN --mount=type=cache,target=${HOME}/.cache/uv,uid=${USER_UID},gid=${USER_GID},mode=0755 \
    uv python install ${PYTHON_VERSION} \
    && uv sync --frozen --no-install-project\
    && find ${UV_PROJECT_ENVIRONMENT} -name "*.pyc" -delete

# Default command
CMD ["bash"]

USER root
COPY --chmod=755 docker/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
