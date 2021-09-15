# This is a very simple way to achieve this, in reality this would be done using the model registry
cp -r data-science/models demo-api/app/
docker-compose up -d --no-deps --build demo-api # Can this be improved using a mounted directory??