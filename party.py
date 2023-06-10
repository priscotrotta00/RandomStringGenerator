from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import os

class Party():
    __slots__ = {'chosen_hash', 'private_key', 'public_key', 'public_key_sign' ,'signed_public_keys', 'public_keys_set_signs', 'contribute', 'randomness', 'commit', 'signed_commit'
                 'signed_committed_contributes', 'signed_opening', 'signed_openings', 'game_contributes', 'random_string'}

    def __init__(self):
        """
        Crea un oggetto partecipante alla partita. Non distingue tra giocatore e server
        """
        self.signed_public_keys = dict()                # dizionario con chiave: PK e valore: sign(PK) di ciascun giocatore
        self.public_keys_set_signs = dict()                         # dizionario con chiave: PK e valore: sign(set)
        self.signed_committed_contributes = dict()      # dizionario con chiave: PK e valore: (commit,sign(commmit)) 
        self.signed_openings = dict()                   # dizionario con chiave: PK e valore: (opening,sign(opening))     dove
                                                        #                                      opening = (contributo, randomness, set dei commit ricevuti)
        self.game_contributes = dict()                  # dizionario con chiave: PK e valore: contributo di ciascun partecipante
        self.chosen_hash = hashes.SHA256()


    def generate_keys(self):
        """
        Genera la coppia chiave privata - chiave pubblica
        """
        self.private_key = ec.generate_private_key(ec.SECP384R1())
        self.public_key = self.private_key.public_key()


    def sign_message(self, msg):
        """
        Firma il messaggio
        """
        return self.private_key.sign(msg, ec.ECDSA(self.chosen_hash)) 
    

    def verify_sign(self, public_key, sign, msg):
        """
        Verifica la correttezza della firma
        """
        public_key.verify(sign, msg, ec.ECDSA(self.chosen_hash))
    

    def sign_public_key(self):
        """
        Genera la coppia (chiave pubblica, firma) 
        """
        sign = self.sign_message(self.encode(self.public_key))
        return (self.public_key,sign)


    def check_signed_public_keys(self):
        """
        Controlla le firme delle chiavi pubbliche ricevute
        """
        for public_key,sign in self.signed_public_keys.items():
            self.verify_sign(public_key,sign,self.encode(public_key)) 


    def create_encoded_signed_public_keys_set(self):
        """
        Crea il set contenente le public key ricevute e le firme associate codificato in bytes
        """
        encoded_set = b''
        for public_key,sign in self.signed_public_keys.items():
            encoded_set = encoded_set + self.encode(public_key) + sign
        return encoded_set
    

    def sign_public_keys_set(self):
        """
        Firma il set contenente le public key ricevute e le firme associate già codificato in bytes
        """
        encoded_set = self.create_encoded_signed_public_keys_set()
        return self.sign_message(encoded_set)


    def check_public_keys_set_signs(self):
        """
        Controlla le firme dei set di contenenti le chiavi pubbliche ricevuti
        """
        set = self.create_encoded_signed_public_keys_set()

        # e verifica la correttezza delle firme per tutti set ricevuti
        for public_key,sign in self.public_keys_set_signs.items():
            self.verify_sign(public_key,sign,set) 


    def generate_contribute(self):
        """
        Genera i contributi per la generazione della stringa casuale
        """
        self.contribute = os.urandom(256)
        self.game_contributes[self.public_key] = self.contribute
        return self.contribute


    def sign_commit(self):
        """
        Firma il commit codificato in bytes del contributo generato
        """
        sign = self.sign_message(self.commit.encode(encoding='utf-8'))
        return (self.commit, sign)


    def check_signed_committed_contributes(self):
        """
        Controlla le coppie (contributo commitatto, firma) ricevute
        """
        for public_key,(commit,sign) in self.signed_committed_contributes.items():
            self.verify_sign(public_key,sign,commit.encode())  


    def create_encoded_opening(self):
        """
        Crea l'apertura (contributo || randomness || set dei commit ricevuti) codificato in bytes
        """
        encoded_opening = self.contribute + self.randomness        
        for public_key,(commit,sign) in self.signed_committed_contributes.items():                               # dove sign rappresenta la firma del commmit 
            encoded_opening = encoded_opening + self.encode(public_key) + commit.encode(encoding='utf-8')        # inserisco solo il commit, senza firma
        return encoded_opening


    def sign_opening(self):
        """
        Firma l'apertura codificata in bytes della tripla (contributo || randomness || set dei commit ricevuti)
        """
        encoded_opening = self.create_encoded_opening()
        sign = self.sign_message(encoded_opening)
        return (encoded_opening, sign)
    

    def check_signed_openings(self):
        """
        Controlla le firme delle aperture codificate in bytes costituite dalla tripla (contributo || randomness || set dei commit ricevuti)
        """
        for public_key,((contribute, randomness, commits_set),sign) in self.signed_openings.items():
            encoded_opening = contribute + randomness
            for PK,commit in commits_set.items():                                         
                encoded_opening = encoded_opening + self.encode(PK) + commit.encode(encoding='utf-8')
            self.verify_sign(public_key,sign,encoded_opening) 


    def encode(self, msg):
        """
        Codifica il messaggio in bytes
        """
        return msg.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    

    def __bitwise_xor_bytes(self, a, b):
        """
        Effettua lo XOR bytes a bytes
        """
        result_int = int.from_bytes(a, byteorder="big") ^ int.from_bytes(b, byteorder="big")
        return result_int.to_bytes(max(len(a), len(b)), byteorder="big")


    def compute_random_string(self):
        """
        Calcola la random string
        """
        random_string = b''
        for public_key,contribute in self.game_contributes.items():
            random_string = self.__bitwise_xor_bytes(random_string,contribute)
        self.random_string = random_string
        return self.random_string


    # Metodi get

    def get_public_key(self):
        return self.public_key
    
    def get_signed_public_keys(self):
        return self.signed_public_keys
    
    def get_public_keys_set_signs(self):
        return self.public_keys_set_signs
    
    def get_contribute(self):
        return self.contribute
    
    def get_randomness(self):
        return self.randomness
    
    def get_commit(self):
        return self.commit
    
    def get_signed_committed_contributes(self):
        return self.signed_committed_contributes
    
    def get_signed_openings(self):
        return self.signed_openings
    
    def get_game_contributes(self):
        return self.game_contributes
    
    def get_random_string(self):
        return self.random_string