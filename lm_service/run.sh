echo "|-- Stopping container"
docker container stop lm_api_run
docker container rm lm_api_run
echo "|-- Running container"
docker compose up -d --build