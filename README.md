# Encrypted-communication
A Python implementation of a server and clients that communicate with eachother through the server encrypting and decrypting messages

# Client-server communication
The creation of, and connection between the server and clients is realized through the usage of the socket and threading libraries<br/>
Communication was made to be possible between two clients, with either one initializing it.<br/>
The clients are presented with a number of commands available to them and must choose one to type as Command-Line Input (like send or exit).
If the server is running, then, assuming they choose send, they will then be asked to name a recepient and what message they'd like to transmit.<br/>
If the recepient exists, they will receive the message. Otherwise, the server will display an error, but keep running.<br/>

# Encryption
- Solitaire algorithm
- Blum-Blum-Shub algorithm<br/>
I implemented two different encryption algorithms for this project. The choice of which one to use, and their seeds, can be read from the contents of config files.<br/>
I also created and encodeStream and decodeStream function, which take an algorithm type, a seed, and a message as inputs, returning the encoded or decoded message as output based on the given parameters.<br/>
It is also possible to test the algorithms without client-server communication with the last few lines of crypto2.py (the server), below the permanently running while loop that keeps the server running.<br/>

