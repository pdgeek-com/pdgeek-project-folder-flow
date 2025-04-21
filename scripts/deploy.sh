#!/bin/bash
# Shell script to import solution using Power Platform CLI
pac auth create --url https://yourorg.crm.dynamics.com
pac solution import --path ./ --publisher-name "PD Geek" --overwrite
