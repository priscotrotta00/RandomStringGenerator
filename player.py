from party import Party
from commitment_scheme import CommitmentScheme

class Player(Party):

    def __init__(self):
        super().__init__()


    def send_signed_public_key(self):
        """
        Invia al server la coppia (chiave pubblica, firma chiave pubblica)
        """
        (public_key,sign) = self.sign_public_key()
        self.public_key_sign = sign
        return (public_key,sign)
    
    
    def receive_signed_public_keys(self, signed_public_keys):
        """
        Riceve dal server le coppie (chiave pubblica, firma chiave pubblica)
        """
        if(self.public_key not in signed_public_keys):
            print("La chiave pubblica di un player non è presente all'interno di uno dei set di chiavi pubbliche firmate ricevuti dal server")
            exit()
        for public_key,signed_public_key in signed_public_keys.items():
            if(public_key == self.public_key):
                if(signed_public_key != self.public_key_sign):
                    print("La coppia (public_key, firma) ricevuta da un player è diversa da quella da lui generata")
                    exit()
            self.signed_public_keys[public_key]=signed_public_key
 

    def send_public_keys_set_sign(self):
        """
        Invia al server la coppia (chiave pubblica - firma del set di chiavi pubbliche)
        """
        set_sign = self.sign_public_keys_set()
        return (self.public_key, set_sign)


    def receive_public_keys_set_signs(self, set_signs):
        """
        Riceve dal server le coppie (chiave pubblica, firma del set di chiavi pubbliche)
        """
        if(self.public_key not in set_signs):
            print("La chiave pubblica di un player non è presente all'interno di uno dei set delle firme di set di chiavi pubbliche ricevuti dal server")
            exit()
        for public_key,set_sign in set_signs.items():   #per ogni chiave pubblica è associata la firma che ha ottenuto a partire dal proprio set di chiavi pubbliche
            self.public_keys_set_signs[public_key]=set_sign    


    def send_signed_committed_contribute(self):
        """
        Invia al server la coppia (contributo commitatto, firma)
        """
        (self.randomness, self.commit) = CommitmentScheme.commit(self.contribute)
        self.signed_commit = self.sign_commit()
        return (self.public_key, self.signed_commit) 
    

    def receive_signed_committed_contributes(self, signed_committed_contributes):
        """
        Riceve dal server le coppie (contributo commitatto, firma)
        """
        if(self.public_key not in signed_committed_contributes):
            print("La chiave pubblica di un player non è presente all'interno del set dei contributi committati ricevuto dal server")
            exit()
        for public_key,(commit,signed_commit) in signed_committed_contributes.items():
            if(public_key == self.public_key):
                if((commit,signed_commit) != self.signed_commit):
                    print("La coppia (commit, firma) ricevuta da un player è diversa da quella da lui generata")
                    exit()
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
        self.signed_opening = (opening, sign_opening)
        return (self.public_key, opening, sign_opening)


    def receive_signed_openings(self, signed_openings):
        """
        Riceve dai giocatori le triple (chiave pubblica - opening - sign(opening)).
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        if(self.public_key not in signed_openings):
            print("La chiave pubblica di un player non è presente all'interno del set delle aperture dei commit ricevuto dal server")
            exit()
        for public_key,(opening,sign) in signed_openings.items():
            if(public_key == self.public_key):
                if((opening,sign) != self.signed_opening):
                    print("La coppia (opening, sign) ricevuta da un player è diversa da quella da lui generata")
                    exit()

            self.signed_openings[public_key]=(opening,sign)
            contribute = opening[0]
            self.game_contributes[public_key] = contribute