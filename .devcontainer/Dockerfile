# See https://mcr.microsoft.com/en-us/artifact/mar/devcontainers/python/about
# FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye
FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm
ARG USERNAME=vscode

ENV DEBIAN_FRONTEND=noninteractive
RUN sudo apt-get update \
    && sudo apt-get upgrade -y  \
    && sudo apt-get -y install --no-install-recommends build-essential graphviz iputils-ping \
    && sudo apt-get autoremove -y \
    && sudo apt-get clean -y \
    && sudo rm -rf /var/lib/apt/lists/*

ENV SHELL=/bin/zsh