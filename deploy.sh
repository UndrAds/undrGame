#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${PROJECT_ROOT}/docker-compose.yml"
COMPOSE=()

if [[ ! -f "${COMPOSE_FILE}" ]]; then
  echo "docker-compose.yml not found at ${COMPOSE_FILE}" >&2
  exit 1
fi

require_command() {
  local cmd="$1"
  if ! command -v "${cmd}" >/dev/null 2>&1; then
    return 1
  fi
  return 0
}

install_docker_linux() {
  if [[ "$(uname -s)" != "Linux" ]]; then
    echo "Automatic Docker installation is only supported on Linux." >&2
    return 1
  fi

  if [[ -f /etc/os-release ]]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    if [[ "${ID_LIKE:-}" == *"debian"* || "${ID:-}" == "debian" || "${ID:-}" == "ubuntu" ]]; then
      echo "Installing Docker Engine via apt..."
      sudo apt-get update
      sudo apt-get install -y ca-certificates curl gnupg
      sudo install -m 0755 -d /etc/apt/keyrings
      curl -fsSL https://download.docker.com/linux/${ID}/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
      sudo chmod a+r /etc/apt/keyrings/docker.gpg
      echo \
        "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/${ID} ${VERSION_CODENAME} stable" |
        sudo tee /etc/apt/sources.list.d/docker.list >/dev/null
      sudo apt-get update
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
      sudo systemctl enable docker
      sudo systemctl start docker
      return 0
    fi
  fi

  echo "Automatic Docker installation is not supported on this distribution." >&2
  return 1
}

ensure_docker() {
  if require_command docker; then
    return 0
  fi

  echo "Docker not found. Attempting installation..."
  if ! install_docker_linux; then
    echo "Please install Docker manually and re-run this script." >&2
    exit 1
  fi
}

ensure_compose() {
  if docker compose version >/dev/null 2>&1; then
    COMPOSE=(docker compose)
    return 0
  fi

  if require_command docker-compose; then
    COMPOSE=(docker-compose)
    return 0
  fi

  echo "Docker Compose is not installed. Attempting installation..."
  install_docker_linux || {
    echo "Please install Docker Compose manually and re-run this script." >&2
    exit 1
  }

  if docker compose version >/dev/null 2>&1; then
    COMPOSE=(docker compose)
    return 0
  fi

  echo "Docker Compose plugin installation failed." >&2
  exit 1
}

ensure_permissions() {
  if ! docker info >/dev/null 2>&1; then
    echo "Current user lacks permission to access the Docker daemon." >&2
    echo "Add your user to the docker group or re-run with sudo." >&2
    exit 1
  fi
}

deploy() {
  cd "${PROJECT_ROOT}"

  echo "Pruning dangling Docker builder cache..."
  docker builder prune --force >/dev/null 2>&1 || true

  echo "Building fresh images..."
  "${COMPOSE[@]}" -f "${COMPOSE_FILE}" build --no-cache --pull

  echo "Applying containers..."
  "${COMPOSE[@]}" -f "${COMPOSE_FILE}" up -d --remove-orphans

  echo "Deployment complete."
}

ensure_docker
ensure_compose
ensure_permissions
deploy

