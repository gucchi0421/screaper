ARG PYTHON_VERSION=3.13 \
    GID=1000 \
    UID=1000 \
    USERNAME=user

FROM python:${PYTHON_VERSION}-alpine

WORKDIR /app

RUN <<EOF
cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
addgroup -g $GID usergroup
adduser -u $UID -G usergroup -D $USERNAME
chown -R $USERNAME:usergroup /app

echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
apk add --no-cache curl bash git sudo

curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin
EOF

ENV PATH="/usr/local/bin:${PATH}"
ENV TZ=Asia/Tokyo

USER $USERNAME

COPY --chown=$USERNAME:usergroup pyproject.toml uv.lock ./

CMD [ "sh", "-c", "task" , "new"]