FROM python:3.9 as builder
WORKDIR /
COPY deployment/requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM node AS js-builder
WORKDIR /usr/src/app
COPY . .
RUN npm install -D
RUN npm run css-build
RUN npm run webpack-release

FROM python:3.9-slim
ENV TZ=Europe/Moscow
ENV LANG C.UTF-8
WORKDIR /usr/src/app
COPY . .
COPY --from=builder /app/wheels /wheels
COPY --from=js-builder /usr/src/app/dist ./dist
RUN pip install --no-cache /wheels/*
CMD $LAUNCH_COMMAND