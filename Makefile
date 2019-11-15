clean:
	rm -rf target

build-image: clean
	mvn package
	cp target/firstdrops-pulsar-*.jar ./docker/
	docker build docker/ -t firstdrops-pulsar

publish-image: build-image
	docker push firstdrops-pulsar

