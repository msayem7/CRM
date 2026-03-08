# Node.js base image
FROM node:22-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY frontend/package*.json /app/

# Install dependencies
RUN npm install

# Copy frontend source code
COPY frontend /app

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
