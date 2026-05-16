# TODO (step 07): imagen unica sin separacion de etapas, ejecuta como root.
# Lee el paso 07 en .tutorial/steps/07-container-security.md
# para convertirla en una imagen multi-stage con usuario no privilegiado.
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

COPY . .

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "server.js"]
