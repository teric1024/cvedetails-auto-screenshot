FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

# Copy all the files
COPY . .

RUN npm run build

CMD [ "npm", "run", "start" ]