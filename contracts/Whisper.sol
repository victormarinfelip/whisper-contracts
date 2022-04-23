// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.9;

import "./SafeMath.sol";


contract Whisper {

    using SafeMath for uint256;

    struct Message {
        uint256 id;
        address from;
        address to;
        uint timestamp;
        string short_message;
        string arweave_add;
        uint256 thread;
    }

    // mapping receiver -> list of all messages
    mapping(address => Message[]) private personal_messages;
    // To better reference messages
    mapping(uint256 => Message[]) private message_database;
    // Mapping of addresses to names
    mapping(address => string) private phonebook;
    // Mapping of address to registered
    mapping(address => bool) private registered;

    // Will also be used to ID messages
    uint256 public total_messages = 1;

    modifier isRegistered() {
        require(registered[msg.sender]);
        _;
    }

    function send_msg(address target, string memory short, string memory arweave, uint256 thread) public isRegistered {
        total_messages += 1;
        if (thread == 1) {
            thread = total_messages;
        }
        Message memory newMessage = Message({
            id: total_messages,
            from: msg.sender,
            to: target,
            timestamp: block.timestamp,
            short_message: short,
            arweave_add: arweave,
            thread: thread
        });
        personal_messages[target].push(newMessage);
        message_database[total_messages].push(newMessage);
    }

    function get_msgs() public view returns (Message[] memory) {
        return personal_messages[msg.sender];
    }

    function get_parent(uint256 id) public view returns (Message[] memory) {
        return message_database[id];
    }

    function register(string memory your_name) public {
        phonebook[msg.sender] = your_name;
        registered[msg.sender] = true;
    }

    function get_name(address addr) public view returns (string memory) {
        return phonebook[addr];
    }

    function get_my_name() public view returns (string memory) {
        return phonebook[msg.sender];
    }

    function iam_registered() public view returns (bool) {
        return registered[msg.sender];
    }
}



