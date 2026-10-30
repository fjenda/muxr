FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install && npm cache clean --force

ENV DOCKER=true

COPY . .

RUN cd node_modules/wavesurfer-multitrack && npm install && npm run build && npm cache clean --force
EXPOSE 5173

RUN npm run dev -- --host 0.0.0.0 & sleep 2 && pkill -f vite || true

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
