from party import Party
from commitment_scheme import CommitmentScheme

class Player(Party):

    def __init__(self):
        super().__init__()


    def send_signed_public_key(self):
        """
        Invia al server la coppia (chiave pubblica, firma chiave pubblica)
        """
        return self.sign_public_key()
    
    
    def receive_signed_public_keys(self, signed_public_keys):
        """
        Riceve dal server le coppie (chiave pubblica, firma chiave pubblica)
        """
        for public_key,public_key_sign in signed_public_keys.items():
            if(public_key == self.public_key):
                if(public_key_sign != self.signed_public_keys[self.public_key]):
                    print('La firma della chiave pubblica ricevuta da un partecipante non corrisponde con quella da lui generata')
                    exit()
            else:
                self.signed_public_keys[public_key] = public_key_sign
 

    def send_public_keys_set_sign(self):
        """
        Invia al server la coppia (chiave pubblica - firma del set di chiavi pubbliche)
        """
        set_sign = self.sign_public_keys_set()
        return (self.public_key, set_sign)


    def receive_public_keys_set_signs(self, public_keys_set_signs):
        """
        Riceve dal server le coppie (chiave pubblica, firma del set di chiavi pubbliche)
        """
        for public_key,public_keys_set_sign in public_keys_set_signs.items():   #per ogni chiave pubblica è associata la firma che ha ottenuto a partire dal proprio set di chiavi pubbliche
            if(public_key == self.public_key):
                if(public_keys_set_sign != self.public_keys_set_signs[self.public_key]):
                    print('La firma del set di chiavi pubbliche ricevuta da un partecipante non corrisponde con quella da lui generata')
                    exit()
            else:
                self.public_keys_set_signs[public_key] = public_keys_set_sign   


    def send_signed_committed_contribute(self):
        """
        Invia al server la coppia (contributo commitatto, firma)
        """
        (self.randomness, self.commit) = CommitmentScheme.commit(self.contribute)
        signed_commit = self.sign_commit()
        return (self.public_key, signed_commit) 
    

    def receive_signed_committed_contributes(self, signed_committed_contributes):
        """
        Riceve dal server le coppie (contributo commitatto, firma)
        """
        for public_key,(commit,signed_commit) in signed_committed_contributes.items():
            self.signed_committed_contributes[public_key]=(commit,signed_commit)

    
    def send_signed_opening(self):
        """
        Invia al server la tripla (chiave pubblica - opening - sign(opening)).
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        (encoded_opening, sign_opening) = self.sign_opening()
        commits_set = dict()        # dizionario con chiave: PK e valore: commit associato
        for public_key,(commit,sign) in self.signed_committed_contributes.items():
            commits_set[public_key] = commit
        opening = (self.contribute, self.randomness, commits_set)
        return (self.public_key, opening, sign_opening)


    def receive_signed_openings(self, signed_openings):
        """
        Riceve dai giocatori le triple (chiave pubblica - opening - sign(opening)).
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        for public_key,(opening,sign) in signed_openings.items():
            self.signed_openings[public_key]=(opening,sign)
            contribute = opening[0]
            self.game_contributes[public_key] = contribute