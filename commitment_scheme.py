from typing import Tuple
from hashlib import sha256
import os

class CommitmentScheme:
    @staticmethod
    def commit(msg: str | bytes) -> Tuple[bytes, bytes]:
        """
        Crea il commitment della stringa msg
        """
        rand = os.urandom(256)
        msg: bytes = msg.encode() if isinstance(msg, str) else msg
        commit = sha256(rand + msg).hexdigest()
        return (rand, commit)
    
    @staticmethod
    def verify(msg: str | bytes, rand: bytes, commit: bytes) -> bool:
        """
        # Apertura del commitment
        """
        msg: bytes = msg.encode() if isinstance(msg, str) else msg
        return commit == sha256(rand + msg).hexdigest()
        