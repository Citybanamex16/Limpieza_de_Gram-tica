import nltk
from nltk import CFG

# CODEX INPURUS: La gramática con pecados capitales
grammar_inpurus = CFG.fromstring("""
    S -> Oracion | Frase_Imp | SP_Cadena

    # Módulo 1: Imperativos (Ambigüedad Crítica)
    Frase_Imp -> Frase_Imp conj Frase_Imp
    Frase_Imp -> Frase_Imp conj v_imp
    Frase_Imp -> v_imp sust
    Frase_Imp -> v_imp adv
    Frase_Imp -> v_imp
    Frase_Imp -> v_imp v_inf

    # Módulo 2: Estructuras Preposicionales (El "Generador de Caos")
    # Al tener recursión izquierda Y vacío, el parser genera ramas infinitas
    SP_Cadena -> SP_Cadena prep sust
    SP_Cadena -> SP_Cadena sust
    SP_Cadena -> 

    # Módulo 3: Oraciones Completas (Recursión de Prefijo)
    Oracion -> Oracion Oracion
    Oracion -> Suj Pred
    Oracion -> Suj v_int

    Pred -> v_trans Obj
    Pred -> Atrib v_cop
    Pred -> v_cop Atrib

    # Módulo 4: Definiciones (Ciclos de Muerte)
    Suj -> sust | v_inf | Oracion | Frase_Imp | SP_Cadena
    Obj -> Suj
    Atrib -> Suj

    # DICCIONARIO UNIFICADO (igual que Puritas_Grammaticae)
    v_imp -> 'veni' | 'vince' | 'memento' | 'carpe' | 'divide' | 'festina' | 'age' | 'impera'
    v_trans -> 'vincit' | 'tenet'
    v_int -> 'volant' | 'manent'
    v_cop -> 'est'
    v_inf -> 'errare' | 'mori'
    sust -> 'diem' | 'vino' | 'veritas' | 'nihilo' | 'astra' | 'amor' | 'omnia' | 'verba' | 'nihil' | 'urbe' | 'condita' | 'humanum' | 'scripta' | 'aspera' | 'mori' | 'quod' | 'agis'
    prep -> 'in' | 'ex' | 'per' | 'ad' | 'ab'
    conj -> 'et' | 'ergo'
    adv -> 'lente'
""")

# El ChartParser es capaz de encontrar TODAS las interpretaciones posibles
parser = nltk.ChartParser(grammar_inpurus)

frases_caos = [
    "Age quod agis",
    "Festina lente",
    "Divide et impera",
    "In vino veritas",
    "Ex nihilo nihil",
    "Ab urbe condita",
    "Amor vincit omnia",
    "Errare humanum est",
    "Verba volant scripta manent",
    "Per aspera ad astra",
    "Carpe diem",
    "Memento mori"
]

print("--- DEMOSTRACIÓN DE AMBIGÜEDAD Y RECURSIÓN IZQUIERDA ---\n")

for frase in frases_caos:
    print(f"\n ANALIZANDO: '{frase.upper()}'")
    frase_limpia = frase.replace(',', '').lower()
    tokens = frase_limpia.split()
    
    try:
        arboles = list(parser.parse(tokens))
        print(f"Ambiguedad Detectada: ¡Se encontraron {len(arboles)} interpretaciones para esta frase!")
        
        # Solo mostramos los primeros 2 para no inundar la terminal
        for i, tree in enumerate(arboles[:2]):
            print(f"\nInterpretación posible #{i+1}:")
            tree.pretty_print()
            
        if len(arboles) > 2:
            print(f"{len(arboles) - 2} árboles más que no tienen sentido.")
            
    except Exception as e:
        print(f"El sistema colapsó: {e}")
    
    print("-" * 50)