#!/usr/bin/python3

import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    # perform a chain rewind after completing each test, to ensure proper isolation
    pass


@pytest.fixture(scope="module")
def whisper(Whisper, accounts):
    return Whisper.deploy({'from': accounts[0]})
