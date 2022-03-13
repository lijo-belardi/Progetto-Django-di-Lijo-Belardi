# Start2Django
## Descrizione
Il progetto consiste in un blog in grado di salvare
il contenuto pubblicato dagli utenti registrati all'interno di una blockchain.

### Specifiche del contenuto del progetto
1. Pagina per consentire la registrazione agli utenti;
2. Pagina, accessibile soltanto dagli utenti loggati, 
   dalla quale è possibile scrivere un post e guardare tutti i post degli altri utenti in ordine cronologico;
3. Pagina profilo dell'utente;
4. Endpoint che restituisce una risposta in JSON contenente le informazioni su tutti i post pubblicati nell’ultima ora;
5. Endpoint attraverso il quale, fornita una stringa tramite GET, restituisce un valore intero corrispondente al numero di volte in cui questa stringa è apparsa nei post pubblicati;
6. Sistema di controllo che proibisce l’inserimento di qualsiasi post contenente la parola ‘hack’;
7. Ssistema di logging per memorizzare l’ultimo IP che ha avuto accesso alla piattaforma per un certo utente, mostrando
   un messaggio di avvertimento quando questo è diverso dal precedente.