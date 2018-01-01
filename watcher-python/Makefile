VERSION := 0.0.1

APP_PKG := dist/app.tar
APP_BASE_DIR := py

DOCKER_IMG := johnwang412/watcher-python


### Package
package-app:
	tar -cvf ${APP_PKG} ${APP_BASE_DIR}
docker-img: package-app
	docker build . -f Dockerfile.node -t ${DOCKER_IMG}:${VERSION}
	docker tag ${DOCKER_IMG}:${VERSION} ${DOCKER_IMG}:latest
	docker image prune -f
	docker images --quiet --filter "dangling=true" | xargs docker rmi -f


### Clean
package-app-clean:
	rm ${APP_PKG}
python-clean:
	find . -name "*.pyc" -type f -delete
