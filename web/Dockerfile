FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

ENV DOCKER=true

COPY . .

EXPOSE 5173

RUN npm run dev -- --host 0.0.0.0 & sleep 2 && pkill -f vite || true

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
