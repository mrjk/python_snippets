#!/usr/bin/python3

# Source: https://stackoverflow.com/questions/11760578/argparse-arguments-nesting

import argparse

parser = argparse.ArgumentParser(description='Deployment tool')
subparsers = parser.add_subparsers()

add_p = subparsers.add_parser('add')
add_p.add_argument("name")
add_p.add_argument("--web_port")

upg_p = subparsers.add_parser('upgrade')
upg_p.add_argument("name")


args = parser.parse_args()
