FROM node:22-slim

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Expose the Next.js default dev port
EXPOSE 3000

# Run the dev server
CMD ["npm", "run", "dev"]
