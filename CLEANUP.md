Commands to stop and remove the test environment created with `docker-compose.test.yml`:

```bash
# Stop services and remove containers, networks, volumes
docker compose -f docker-compose.test.yml down -v
```

This will stop the `pg` and `app` services and remove anonymous volumes created by the compose run.
