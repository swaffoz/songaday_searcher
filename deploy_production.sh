#!/bin/bash

ansible-playbook ./deploy/deploy.yml --private-key=~/.ssh/id_rsa -u freebsd -i ./deploy/hosts -vvv