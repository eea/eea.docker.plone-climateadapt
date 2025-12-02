#!/usr/bin/env fish

# List all Docker images with the <none> tag, extract their IDs, and remove them
for image_id in (docker images --filter "dangling=true" -q)
    echo "Removing image: $image_id"
    docker rmi -f $image_id
end

echo "Done! All <none> images have been removed."