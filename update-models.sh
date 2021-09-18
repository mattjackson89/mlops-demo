#!/usr/bin/env bash

# This is a very simple way to achieve this, in reality this would be done using the model registry

#!/usr/bin/env bash

VERSION=${1:-v1}

# Copy the models 
cp -r data-science/models demo-api/app/

# Promote -v to latest 
rm -rf demo-api/app/models/latest
echo demo-api/app/models/"$VERSION"
cp -r demo-api/app/models/"$VERSION" demo-api/app/models/latest
