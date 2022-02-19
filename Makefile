# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(patsubst %/,%,$(dir $(mkfile_path)))

# include .env
# export $(shell sed 's/=.*//' .env)

help: ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# ========== Poetry stuff ========== #
shell: ## Activate Poetry shell
	poetry shell

install_poetry: ## Install Poetry
	curl -sSL https://install.python-poetry.org | python3 -

version: ## Check Poetry version
	poetry --version

# ========== Build ========== #

build: ## Build package
	poetry build

# ========== Utils ========== #

clear: ## Clear repository
	rm -rf "${current_dir}/subject"

fill: ## Fill subject directory
	mkdir -p "${current_dir}/subject/node_modules"
	touch "${current_dir}/subject/node_modules/enemy.txt"
	mkdir -p "${current_dir}/subject/sub/node_modules"
	touch "${current_dir}/subject/sub/node_modules/enemy.txt"
	mkdir -p "${current_dir}/subject/sub2/node_modules"
	touch "${current_dir}/subject/sub2/node_modules/enemy.txt"
	mkdir -p "${current_dir}/subject/sub/3/node_modules"
	touch "${current_dir}/subject/sub/3/node_modules/enemy.txt"
	mkdir -p "${current_dir}/subject/sub/2/1/4/node_modules"
	touch "${current_dir}/subject/sub/2/1/4/node_modules/enemy.txt"

# ========== Package ========== #

scan: ## Scan directories
	nested-rimraf --help
