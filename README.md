#Blackjack

This is your classic blackjack game, with standard blackjack rules.

You can play with up to three people Vs. a cpu-dealer.  The dealer plays by the standard 
casino dealer rules (if you know of anything thats not, please let me know).  

Each player can be on their own separate computer/device as long as it can run python and 
connect to your local network.


###Configure

Blackjack uses pygames, if you don't already have pygames installed, you can get a copy [here](http://www.pygame.org/news.html).

Have someone run the dealer.py file.  Which ever person is running the dealer file, you are
going to need that person's machines internal ip address.  Once you know that address,
then everyone adds that in on line # in the client file in between the parenthesis:

    reactor.connectTCP('THAT ADDRESS HERE', 6000 BlackClient(c))
 
Then everyone runs the client.py file. 
