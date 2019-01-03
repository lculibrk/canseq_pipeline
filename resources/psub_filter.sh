#!/bin/bash
### This is an internal file, do not touch
perl -pe 's/\// /' $1 | awk '{print $1}'