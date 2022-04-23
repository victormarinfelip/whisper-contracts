#!/usr/bin/python3
from brownie.exceptions import VirtualMachineError
import pytest

def test_registers(accounts, whisper):
    whisper.register("paco", {'from': accounts[0]})
    print("hola")
    assert whisper.get_name(accounts[0], {'from': accounts[0]}) == "paco"
    assert whisper.get_my_name({'from': accounts[0]}) == "paco"

def test_write_message(accounts, whisper):
    whisper.register("paco", {'from': accounts[0]})
    msg = "hola que tal"
    target = accounts[1]
    arw = msg+msg
    thread = 1
    whisper.send_msg(target, msg, arw, thread, {"from": accounts[0]})
    # Now we get that msg
    messages = whisper.get_msgs({"from": accounts[1]})
    assert messages[0][4] == "hola que tal"
    assert messages[0][1] == accounts[0]
    assert messages[0][2] == accounts[1]

def test_needs_registry(accounts, whisper):
    msg = "hola que tal"
    target = accounts[1]
    arw = msg+msg
    thread = 1
    with pytest.raises(VirtualMachineError):
        whisper.send_msg(target, msg, arw, thread, {"from": accounts[0]})

def test_am_i_registered(accounts, whisper):
    assert whisper.iam_registered({"from": accounts[0]}) == False
    whisper.register("Whisperer", {"from": accounts[0]})
    assert whisper.iam_registered({"from": accounts[0]}) == True

def test_full_conversation(accounts, whisper):
    whisper.register("Bob", {'from': accounts[0]})
    whisper.register("Alice", {'from': accounts[1]})

    bob_msgs = ["Hi there", "I'm good and you?", "Fine!"]
    alice_msgs = ["Hey! how are you", "I'm good too", "Nice!"]

    reply_to_id = 1
    convo = []
    for msgb, msga in zip(bob_msgs, alice_msgs):
        # Bob sends his message
        whisper.send_msg(accounts[1], msgb, "",  reply_to_id, {"from": accounts[0]})
        # Alice gets her messages
        last_msg_for_alice = whisper.get_msgs({"from": accounts[1]})[-1]
        convo.append([whisper.get_my_name({"from": accounts[0]}), last_msg_for_alice[4]])
        # Alice answers
        reply_to_id = last_msg_for_alice[0]
        whisper.send_msg(accounts[0], msga, "",  reply_to_id, {"from": accounts[1]})
        # Bob gets his messages
        last_msg_for_bob = whisper.get_msgs({"from": accounts[0]})[-1]
        convo.append([whisper.get_my_name({"from": accounts[1]}), last_msg_for_bob[4]])
        reply_to_id = last_msg_for_bob[0]

    expected = []
    for msgb, msga in zip(bob_msgs, alice_msgs):
        expected.append(["Bob", msgb])
        expected.append(["Alice", msga])

    assert convo == expected

    # Finally we test that we can recover the whole conversation from the 'thread' parameter
    # Last message was for bob:
    s_convo = []
    for msgb, msga in zip(bob_msgs, alice_msgs):
        s_convo.append(msgb)
        s_convo.append(msga)

    s_convo.reverse()
    id_ = whisper.get_msgs({"from": accounts[0]})[-1][-1]
    for el in s_convo[1:]:
        parent = whisper.get_parent(id_)[0]
        assert parent[4] == el
        id_ = parent[-1]



