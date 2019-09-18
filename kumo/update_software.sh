#!/bin/bash

pushd /home/pi/dndpdx

# From comment on https://stackoverflow.com/questions/3258243/check-if-pull-needed-in-git#targetText=First%20use%20git%20remote%20update,and%20remote%20are%20the%20same.

git remote update
LAST_UPDATE=$(git show --no-notes --format=format:"%H" master | head -n 1)
LAST_COMMIT=$(git show --no-notes --format=format:"%H" origin/master | head -n 1)

if [ $LAST_COMMIT != $LAST_UPDATE ]; then
	echo "Pulling..."
	git pull

	sudo systemctl restart api
	sudo systemctl restart nginx

	pushd kumo/app
	ng build --prod
	popd
fi

popd
