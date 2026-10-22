"""
ExamOpt — Socket Wire Protocol & Frame Marshaller
Milestone 7: Distributed Socket Programming
SRM Institute of Science and Technology, Tiruchirappalli

Implements 4-byte length-prefixed framing over TCP stream with UTF-8 JSON serialization.
Protects against TCP packet fragmentation and buffer boundary truncation.
"""
import socket
import struct
import json
from typing import Dict, Any, Optional

HEADER_FORMAT = "!I"  # 4-byte unsigned integer (big-endian)
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def send_json_message(sock: socket.socket, message_dict: Dict[str, Any]) -> None:
    """
    Serializes a dictionary to JSON, encodes to UTF-8, prepends 4-byte length header,
    and sends the entire frame across the socket.
    """
    json_bytes = json.dumps(message_dict).encode("utf-8")
    length = len(json_bytes)
    header = struct.pack(HEADER_FORMAT, length)
    sock.sendall(header + json_bytes)


def recv_json_message(sock: socket.socket, timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
    """
    Reads the 4-byte length prefix header, reads exactly that many payload bytes,
    and deserializes the JSON payload. Returns None if connection closed gracefully.
    """
    if timeout is not None:
        sock.settimeout(timeout)

    header_bytes = _recv_exact(sock, HEADER_SIZE)
    if not header_bytes:
        return None

    length = struct.unpack(HEADER_FORMAT, header_bytes)[0]
    payload_bytes = _recv_exact(sock, length)
    if not payload_bytes:
        raise ConnectionResetError("Connection lost while reading message payload")

    return json.loads(payload_bytes.decode("utf-8"))


def _recv_exact(sock: socket.socket, num_bytes: int) -> Optional[bytes]:
    """Helper that repeatedly reads from socket until exactly num_bytes are accumulated."""
    buffer = bytearray()
    while len(buffer) < num_bytes:
        chunk = sock.recv(num_bytes - len(buffer))
        if not chunk:
            if len(buffer) == 0:
                return None
            raise ConnectionResetError("Incomplete payload received before socket closure")
        buffer.extend(chunk)
    return bytes(buffer)
