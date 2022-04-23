#!/usr/bin/python3

from brownie import Whisper, accounts


def main():
    return Whisper.deploy({'from': accounts[0]})
