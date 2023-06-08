from cryptography.hazmat.primitives import serialization

class Table():
    __slots__ = {'__server', '__players', '__num_players'}

    def __init__(self, server):
        self.__server = server
        self.__players = []


    def add_player(self, player):
        """
        Aggiunge giocatori alla partita
        """
        self.__players.append(player)


    def generate_players_keys(self):
        """
        Ogni giocatore genera la propria coppia (chiave privata - chiave pubblica)
        """
        for player in self.__players:
            player.generate_keys()


    def send_signed_public_keys_to_server(self):
        """
        Invio delle coppie (chiave pubblica - firma chiave pubblica) dai giocatori al server
        """
        messages = []
        for player in self.__players:
            messages.append(player.send_signed_public_key())      #lista contenente per ogni giocatore (PK, sign(PK)) 
        self.__server.receive_signed_public_keys(messages)
        self.__server.check_signed_public_keys()


    def send_signed_public_keys_to_players(self):
        """
        Invio delle coppie (chiave pubblica - firma chiave pubblica) dal server ai giocatori
        """
        signed_public_keys = self.__server.send_signed_public_keys()
        for player in self.__players:
            player.receive_signed_public_keys(signed_public_keys)
            player.check_signed_public_keys


    def send_public_keys_set_signs_to_server(self):
        """
        Invio delle coppie (chiave pubblica - firma del set contenente le public key ricevute e le firme associate) dai giocatori al server
        """
        messages = []
        for player in self.__players:
            messages.append(player.send_public_keys_set_sign())    # ogni giocatore invia (PK,sign(set))
        self.__server.receive_public_keys_set_signs(messages)
        self.__server.check_public_keys_set_signs()
        

    def send_public_keys_set_signs_to_players(self):
        """
        Invio delle coppie (chiave pubblica - firma del set contenente le public key ricevute e le firme associate) dal server ai giocatori
        """
        public_keys_set_signs = self.__server.send_public_keys_set_signs()
        for player in self.__players:
            player.receive_public_keys_set_signs(public_keys_set_signs)
            player.check_public_keys_set_signs()

        
    def generate_contributes(self):
        """
        Ogni partecipante genera il proprio contributo
        """
        self.__server.generate_contribute()
        for player in self.__players:
            player.generate_contribute()
    

    def send_signed_committed_contributes_to_server(self):
        """
        Invio delle coppie (chiave pubblica - (contributo commitatto, firma)) dai giocatori al server
        """
        messages = []
        for player in self.__players:
            messages.append(player.send_signed_committed_contribute())      #lista contenente per ogni giocatore (PK, sign(PK)) 
        self.__server.receive_signed_committed_contributes(messages)
        self.__server.check_signed_committed_contributes()


    def send_signed_committed_contributes_to_players(self):
        """
        Invio delle coppie (chiave pubblica - (contributo commitatto, firma)) dal server ai giocatori
        """
        signed_committed_contributes = self.__server.send_signed_committed_contributes()
        for player in self.__players:
            player.receive_signed_committed_contributes(signed_committed_contributes)
            player.check_signed_committed_contributes()


    def send_signed_openings_to_server(self):
        """
        Invio delle triple (chiave pubblica - opening - sign(opening)) dai giocatori al server
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        messages = []
        for player in self.__players:
            messages.append(player.send_signed_opening())      
        self.__server.receive_signed_openings(messages)
        self.__server.check_signed_openings()


    def send_signed_openings_to_players(self):
        """
        Invio delle triple (chiave pubblica - opening - sign(opening)) dal server ai giocatori
        opening contiene (contributo, randomness, set dei commit ricevuti)
        """
        openings = self.__server.send_signed_openings()
        for player in self.__players:
            player.receive_signed_openings(openings)
            player.check_signed_openings()


    def compute_random_string(self):
        """
        Calcola la stringa casuale 
        """
        self.__server.compute_random_string()
        for player in self.__players:
            player.compute_random_string()
