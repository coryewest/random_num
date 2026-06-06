# Stage 1: Build the app
FROM registry.access.redhat.com/hi/python:latest-builder AS builder
USER 0
WORKDIR /app
# Install Flask and Gunicorn into a virtual environment
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install flask gunicorn
# Stage 2: Final production image
FROM registry.access.redhat.com/hi/python:latest
WORKDIR /app
# Copy only the virtual environment and your code to the clean image
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Copy the entire app directory so `templates/` is preserved at /app/templates
COPY app/ ./
# Tell the system this app runs on port 5000
EXPOSE 5000
# Use Gunicorn to run the app
STOPSIGNAL SIGINT
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]