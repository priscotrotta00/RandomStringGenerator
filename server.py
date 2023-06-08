from party import Party
from commitment_scheme import CommitmentScheme

class Server(Party):
    
    def __init__(self):
        super().__init__()
        super().generate_keys()


    def receive_signed_public_keys(self, signed_public_keys):
        """
        Riceve dai giocatori le coppie (chiave pubblica - firma chiave pubblica)
        """
        for (public_key,sign) in signed_public_keys:
            self.signed_public_keys[public_key] = sign


    def send_signed_public_keys(self):
        """
        Invia ai giocatori le coppie (chiave pubblica - firma chiave pubblica)
        """
        return self.get_signed_public_keys()
    

    def receive_public_keys_set_signs(self, public_keys_set_signs):     # il server riceve le coppie (PK,sign(set))
        """
        Riceve dai giocatori le firme dei set contenenti le public key ricevute e le firme associate già codificati in bytes
        """
        for (public_key,public_key_set_sign) in public_keys_set_signs:
            self.public_keys_set_signs[public_key] = public_key_set_sign


    def send_public_keys_set_signs(self):
        """
        Invia ai giocatori le firme dei set contenente le coppie (chiave pubblica, firma del set di chiavi pubbliche) 
        """
        return self.get_public_keys_set_signs()
    

    def receive_signed_committed_contributes(self, signed_committed_contributes):
        """
        Riceve dai giocatori le coppie (chiave pubblica - (contributo commitatto, firma))
        """
        for (public_key,(commit,sign)) in signed_committed_contributes:
            self.signed_committed_contributes[public_key] = (commit,sign)

        # ed aggiunge la propria coppia

        (self.randomness, self.commit) = CommitmentScheme.commit(self.contribute)
        (commit,sign) = self.sign_commit()
        self.signed_committed_contributes[self.public_key] = (commit,sign)


    def send_signed_committed_contributes(self):
        """
        Invia ai giocatori le coppie (chiave pubblica - (contributo commitatto, firma))
        """
        return self.get_signed_committed_contributes()
    

    def receive_signed_openings(self, signed_openings):
        """
        Riceve dai giocatori le triple (chiave pubblica - opening - sign(opening)).
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        for (public_key, opening, sign) in signed_openings:
            self.signed_openings[public_key] = (opening,sign)   # con opening = (contributo, randomness, set dei commit ricevuti)
            self.game_contributes[public_key] = opening[0]      # opening[0] corrisponde al contributo

        # ed aggiunge la propria

        (encoded_opening, sign_opening) = self.sign_opening()
        commits_set = dict()        # dizionario con chiave: PK e valore: commit associato
        for public_key,(commit,sign_commit) in self.signed_committed_contributes.items():
            commits_set[public_key] = commit
        opening = (self.contribute, self.randomness, commits_set)   # il set di commit non contiene la firme, ma solo la coppia (PK,commit)
        self.signed_openings[self.public_key] = (opening,sign_opening)
    

    def send_signed_openings(self):
        """
        Invia ai giocatori le triple (chiave pubblica - opening - sign(opening)).
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        return self.get_signed_openings()