# random_num

Flask app to run the random_num.py script within a web page.

## Podman: Build, Run, and Persistence

Quick examples for building and running the app with Podman and keeping persistent data during maintenance.

- Build the image:

```bash
podman build -t random_num:latest -f Containerfile .
```

- Run for development (bind-mount `templates/` and `excluded_numbers.txt` from the host so edits take effect immediately):

```bash
mkdir -p ./data
mkdir -p ./data
: > ./data/excluded_numbers.txt
podman run --rm -p 5000:5000 \
	-v $(pwd)/data:/data:Z \
	-v $(pwd)/app/templates:/app/templates:Z \
	-e EXCLUDE_FILE=/data/excluded_numbers.txt \
	random_num:latest
```

- Run with a named volume for persistent data (keeps `excluded_numbers.txt` across container restarts):

```bash
podman volume create random_num_data
podman run --rm -p 5000:5000 \
	-v random_num_data:/app/data:Z \
	-e EXCLUDE_PATH=/app/data/excluded_numbers.txt \
	random_num:latest
```

Note: the app now uses `/tmp/excluded_numbers.txt` by default, but the bind-mount example above uses `/data/excluded_numbers.txt` so the file is writable and easy to edit from the host.

- Copy files out/in for maintenance:

```bash
# copy from container to host
podman cp <container>:/data/excluded_numbers.txt ./data/excluded_numbers.txt
# edit locally, then copy back
podman cp ./data/excluded_numbers.txt <container>:/data/excluded_numbers.txt
```

- SELinux and permissions:
  - On RHEL-like hosts use the `:Z` (or `:z`) mount option to relabel files for container access.
  - Ensure the container process UID can write the mounted files (adjust host ownership or use a volume).

Recommendation:

- For quick edits and template changes during development, bind-mount `templates/` and `excluded_numbers.txt` from the host.
- For production, prefer a named volume for `excluded_numbers.txt` or migrate to a small database (SQLite/Postgres) and keep templates in source control and deployed with image builds.
