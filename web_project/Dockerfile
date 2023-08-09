# Use the official MySQL image as base
FROM mysql:latest

# Set environment variables for MySQL
ENV MYSQL_ROOT_PASSWORD=yotam
ENV MYSQL_DATABASE=users

# Copy the init.sql file to the Docker entrypoint directory
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306
