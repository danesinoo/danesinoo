#è estratta una card casuale dal deck, viene tornata la card
import random
def draw_card(deck):
    return deck.pop(random.randint(0, len(deck) - 1))

#conta quante volte il value di una card si ripetono tra le carte in hand e le
#carte sul board, restituisce una tupla (number ripetizione del value che si
#ripete di più, number di ripetizoni del value che si ripete di meno, value che
#si ripete di più, value che si ripete di meno)
def coppia(tuplee, sett):
    hand_values = list((x[0] for x in tuplee))
    values = hand_values + [x[0] for x in sett]

    pairs = tuple()
    for value in set(hand_values): #prendo in considerazione solo i values in hand
#gli altri sono in comune tra tutte le carte e non serve prenderli in considerazione
#set() non permette ripetizioni e dunque in questo modo evito di contare due volte
#lo stesso valuee (il player potrebbe avere una coppia in hand)
        pairs = pairs + (values.count(value), value)

    if len(pairs) == 2: #se il player ha in hand una coppia il risultato non si ripete
        return (pairs[0], 1, pairs[1])#viene restituita una tupla
#del tipo (umero ripetizione del value che si ripete di più, 1, value) in modo
#da valere meno di una doppia coppia nel qual caso ce ne sia una, ma come una coppia
#sola, per esempio. Lo stesso discorso vale per il tris.

    elif pairs[0] > pairs[2]:#invece di usare sort(), ordino io la tupla
        return (pairs[0], pairs[2], pairs[1], pairs[3])

    else: return (pairs[2], pairs[0], pairs[3], pairs[1])

#controlla se è presente colore tra la hand ed il board. se è questo il caso
#restituisce una tupla confrontabile con la funzione coppia: in modo tale che valga
#più di un tris, ma meno di un full. Inoltre vengono aggiunte le carte della hand,
#così è possibile un confronto tra players che hanno colore.
def sorte(dasa):#questa funzion mi è utile perchè mi permette di risparmyre diverse righe
    dasa.sort( reverse = True)#è come sort ma non torna None, ma la lista ordinata
    return dasa #vd quando sono formate le hands dei players
def flush(tuplee, sett):
    hand_suits = list((x[1] for x in tuplee))
    suits = hand_suits + [x[1] for x in sett]

    for suit in set(hand_suits):
        number_suits = suits.count(suit)#colore vale più di tris, ma meno di full
#tramite coppia() un tris da come risultato una tuple (3, 1, e la hand), invece
#un full risulta essere (3, 2, e la hand). In conclusione bisogna che la tupla
#che ha colore stia in mezzo tra questi due values, io ho scelto (3, 1.9, e la hand)
#la hand non ha bisogno dei suits: non influiscono per il conteggio dei points
        if number_suits > 4:
            straight_reale = straight((x for x in sett.update(tuplee) if x[1] == suit))
            if straight_reale > 2: return (5, ) + straight_reale[3:]
            else: return (3, 1.9,) + tuple([x[0] for x in tuplee])

        else: return (0, )

#restituisce una tupla compresa tra tris e flush, il value più alto della straight
#le due carte nella hand
def straight(tuplee, sett):
    hand_values = list((x[0] for x in tuplee))
    values = sorte(hand_values + [x[0] for x in sett])

    for value in values[:3]:
        if value - 4 in values and value - 3 in values:
            if value - 2 in values and value - 1 in values:
#vale lo stesso discorso fatto per colore, però questa volta la tupla risultante
#deve essere compresa tra (3, 1) e (3, 1.9), io ho sccelto (3, 1.8, card più alta
#della straight, la hand) gli ultimi tre values servono per un confronto tra le scale.
# la hand ha due values, uno per ciascuna card
                return (3, 1.8, value) + tuple(hand_values)
                pass

    if 13 and 5 and 4 and 3 and 2 in values:#l'asso è il 13, però può essere anche
        return (3, 1.8, 5) + tuple(hand_values) #l'1
        pass

    else: return (0, )
#questa funzione calcola i points della hand che viene inserita rispetto al board
def points(hand1, board):
    points = sorte([coppia(hand1, board),flush(hand1, board),straight(hand1, board)])

    return points

print("Le carte possono essere iserite solo nel seguente modo:")
print("il value della my_first_card uno spazio e il suit della card.")
print("L'asso ha value 13 e dunque la card con value più basso risulta essere il 2.")
print("I suits vanno da 1 a 4")

my_first_card=input('inserisci la first card: ').split(' ')
my_second_card=input('Inserisci la second card: ').split(' ')

my_first_card=(int(my_first_card[0]), int(my_first_card[1]))
my_second_card= (int(my_second_card[0]), int(my_second_card[1]))
my_hand= {my_first_card, my_second_card}
#la my hand è un un set con due tuple: ciscuna indica una card

players = int(input('Enter the number of players: '))

if players > 22:
    print('Sorry, could not understand')
    quit()

wins= 0
played_matches=0

while played_matches<1000000:

    deck=[(x,y) for x in range(2,14) for y in range(1,5)] #non uso mai un ciclo for
    deck.remove(my_first_card)#invece devo estrarre carte in points casuali
    deck.remove(my_second_card)#vedi draw_card()

    played_matches = played_matches + 1
    hands_players = set() #si tratta di un set di una tuple che contiene le carte dei players
    board = set()  #set di tuple/ carte poste al centro del board (5)

    for player in range(players): #il set hands_players contiene le hands di tutti i players
        hands_players.add(tuple(sorte([draw_card(deck), draw_card(deck)])))
        #genera una tupla di tuple(non si può mettere un set in un set)
    for i in range(5):
        board.add(draw_card(deck))
        #carte in comune a tutti i players, genera un set di tuple/ carte

    [coppia(my_hand, board), flush(my_hand, board), straight(my_hand, board)].sort()

    winning_hand=[(0, )] #qui viene fatto un confronto tra le hands dei players
    for hand_player in hands_players:#alla fine confrontiamo la hand che è più
        challenger = points(hand_player, board)#forte con la nostra
        if winning_hand < challenger:
            winning_hand = challenger

    if points(my_hand, board) > winning_hand: #se la nostra hand vale di più
        wins = wins + 1#aggiungiamo una vittoria

print('wins: %d \n partite giocate: %d' %{'number': wins, played_matches})
