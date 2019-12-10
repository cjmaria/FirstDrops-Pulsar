clean:
	rm -rf target

build-image: clean
	mvn compile
	mvn package
	cp target/firstdrops-pulsar-*.jar ./docker/
	docker build docker/ -t firstdrops-pulsar:latest

push-image: build-image
	$(shell aws ecr get-login --no-include-email --region us-east-1)
	docker tag firstdrops-pulsar:latest 495547744624.dkr.ecr.us-east-1.amazonaws.com/firstdrops-pulsar:latest
	docker push 495547744624.dkr.ecr.us-east-1.amazonaws.com/firstdrops-pulsar:latest
	
build-image-clean: clean
	mvn compile
	mvn package
	cp target/firstdrops-pulsar-*.jar ./docker/
	docker build --no-cache docker/ -t firstdrops-pulsar:latest

