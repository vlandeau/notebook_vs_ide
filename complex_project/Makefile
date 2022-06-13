# Development targets

install:
	$(MAKE) -C lambdas install

# Main targets
check:
	$(MAKE) -C lambdas check
	$(MAKE) -C infrastructure tf-fmt-check

package:
	$(MAKE) -C lambdas package

plan:
	$(MAKE) -C infrastructure tf-validate
	$(MAKE) -C infrastructure tf-plan

deploy:
	$(MAKE) -C infrastructure jenkins-tf-apply

sync-raw-data-local-to-s3:
	aws s3 sync workdir/landing/raw s3://bootcamp-2021-01-data/landing/raw

sync-raw-data-s3-to-local:
	aws s3 sync s3://bootcamp-2021-01-data/landing/raw workdir/landing/raw

generate-example:
	mkdir -p workdir/landing/raw/sample_dataset/version_1
	echo "id,value" > workdir/landing/raw/sample_dataset/version_1/example.csv
	echo "1,toto" >> workdir/landing/raw/sample_dataset/version_1/example.csv
	echo "2,titi" >> workdir/landing/raw/sample_dataset/version_1/example.csv
