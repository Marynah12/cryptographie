#programme de la machine enigma
#Anne Pacou décembre 2022

# Marina Flament

#------------------------------------------------importations et constantes------------------------------------------
from numpy import empty, object,copy

#les rotors
ROUE=empty([3,26], dtype=object)
ROUE[0] = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
ROUE[1] = ["G","W","Q","R","U","E","Y","N","O","J","A","K","Z","L","S","B","I","V","C","X","D","H","F","M","P","T"]
ROUE[2] = ["I","L","A","W","X","B","Q","C","E","M","O","R","V","Y","N","H","F","G","J","K","P","T","D","S","Z","U"]

#le tableau de connexion par défaut
CONNEXION = empty([2,26], dtype=object)
CONNEXION[0] = copy(ROUE[0])
CONNEXION[1] = ["S","B","P","V","Y","F","Q","W","K","J","I","Z","N","M","T","C","G","R","A","O","U","D","H","X","E","L"]
#tableau de connexion AS, EY,IK, OT, CP, GQ, LZ, DV, HW, MN 

# Le tableau inversé
REVERSE = ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S', 'R', 'Q', 'P', 'O', 'N', 'M', 'L', 'K', 'J', 'I',
 'H', 'G', 'F', 'E', 'D', 'C', 'B', 'A']

#----------------------------------------------------Sous-programmes-------------------------------
def index(lettre: str,tableau : list[str]):
    """fabrication de la même fonction que dans la bibliothèque, donne l'indice d'une valeur données

    Args:
        lettre (str): la lettre
        tableau (list[str]): la tableau avec les lettres

    Returns:
        int: l'emplacement de la lettre dans le tableau
    """
    for i in range(len(tableau)):
        if tableau[i] == lettre:
            return i
    return -1

def reglage():
    """réglage du tableau de connexion et des roues

    Returns:
        tuple: vecteur à 3 éléments qui indique la position des roues les unes / aux autres, tableau de connexion
    """
    code=input("Donner la suite de lettre qui correspond aux roues ")
    indice=[0,0,0]
    for i in range(3):
        indice[i]=index(code[i], ROUE[i])
    indice=[0,(indice[1]-indice[0])%26,(indice[2]-indice[0])%26]
    
    fini = False
    print(indice)
    
    choix = input("OK, maintenant occupons nous du tableau de connexion. Utiliser celui par défaut (taper 1), ou le choisir vous-même (taper 2)? ")
    if choix == "1":
        tableau_connexion=CONNEXION
    else :
        tableau_connexion=empty([2,26], dtype=object)
        for i in range(26):
            tableau_connexion[0][i]=chr(65+i)
            tableau_connexion[1][i]=chr(65+i)
        while fini == False:
            print(tableau_connexion[0])
            print(tableau_connexion[1])
            couple=input("Donnez le couple de lettres associées du tableau de connexion, 0 pour arrêter ")
            if couple == "0":
                fini = True
            else:
                position1=index(couple[0],ROUE[0] )
                position2=index(couple[1], ROUE[0])
                tableau_connexion[1][position1] = ROUE[0][position2]
                tableau_connexion[1][position2] = ROUE[0][position1]
    return indice, tableau_connexion



def cycle_enigma(lettre : str, indice :list[int], tableau : list[str]):
    """permet le cryptage enigma, 

    Args:
        lettre (str): la lettre à crypter
        indice (list[int]): le tableau indiquant la position des roues
        tableau (list[str]): le tableau de connexion choisi

    Returns:
        str: le caractère crypté
    """
    place = index(lettre, tableau[0])
    nvlle_lettre = tableau[1][place]
    index_new_lettre = index(nvlle_lettre, ROUE[0])
    print("\nLettre après la connexion : " + nvlle_lettre)
    index_roue1 = (indice[2]+index_new_lettre)%26
    print("Index de la lettre : " + str(index_new_lettre))
    print("Index après les 3 roues : " + str(index_roue1))
    roue1 = ROUE[2][index_roue1]
    print("Lettre après les 3 roues : " + roue1)
    index_reversed = index(roue1, ROUE[0])
    lettre_reversed = REVERSE[index_reversed]
    print("Réflecteur de la lettre : " + lettre_reversed)
    index_lettre_inverse = index(lettre_reversed, ROUE[2])
    print("Index de la lettre : " + str(index_lettre_inverse))
    index_roue2 = (index_lettre_inverse - indice[2])%26
    print("Index de la lettre après les 3 roues : " + str(index_roue2))
    roue2 = ROUE[0][index_roue2]
    print("Lettre après les 3 roues : " + roue2)
    lettre_finale = tableau[1][index_roue2]
    print("Après le tableau de connexion : " + lettre_finale)
    print("Nous avons au final : " + lettre_finale)
    return lettre_finale


#------------------------------------------------------programme principal----------------------------------------------

#Avec tableau de connexion AS, EY,IK, OT, CP, GQ, LZ, DV, HW, MN et réflecteur A=Z, B=Y
#le mot DEPWWP donne QUINZE avec D-V-I-R-G-Q et ARB roues
if __name__ == '__main__':
    indice_dep, table=reglage()
    mot = input("Donnez le mot que vous souhaitez crypter ")
    resultat = ""
    for lettre in mot:
        resultat = resultat + cycle_enigma(lettre, indice_dep, table)
        indice_dep[2] = indice_dep[2] - 1
    print("\nLe mot crypté est : " + resultat)   