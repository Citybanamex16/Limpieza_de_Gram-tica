import nltk
from nltk import CFG

# 1. Tu Gramática 100% LL(1)
grammar = CFG.fromstring("""
    # SÍMBOLO INICIAL
    S -> Oracion | Frase_Imp | SP_Cadena

    # MÓDULO 1: Frases Imperativas
    Frase_Imp -> Imp_Base Frase_Imp_Prima
    Frase_Imp_Prima -> conj Frase_Imp Frase_Imp_Prima | 
    Imp_Base -> v_imp Imp_Base_Prima
    Imp_Base_Prima -> adv | sust | 

    # MÓDULO 2: Preposicional
    SP_Cadena -> prep sust SP_Resto | 
    SP_Resto -> SP_Cadena | sust | 

    # MÓDULO 3: Oraciones Completas
    Pred -> v_trans Obj | Atrib v_cop | v_cop Atrib
    Oracion_Base -> Suj Oracion_Base_Prima
    Oracion_Base_Prima -> v_int | Pred
    Oracion -> Oracion_Base Oracion_Prima
    Oracion_Prima -> Oracion_Base Oracion_Prima | 

    # MÓDULO 4: Definiciones
    Suj -> sust Suj_Tail | v_inf | Frase_Imp
    Suj_Tail -> SP_Cadena
    Obj -> Suj
    Atrib -> Suj

   # DICCIONARIO LÉXICO CORREGIDO
    v_imp -> 'veni' | 'vince' | 'memento' | 'carpe' | 'divide' | 'festina' | 'age' | 'impera'
    sust -> 'diem' | 'vino' | 'veritas' | 'nihilo' | 'astra' | 'amor' | 'omnia' | 'verba' | 'nihil' | 'urbe' | 'condita' | 'humanum' | 'scripta' | 'aspera' | 'mori' | 'quod' | 'agis'
    prep -> 'in' | 'ex' | 'per' | 'ad' | 'ab'
    v_trans -> 'vincit' | 'tenet'
    v_int -> 'volant' | 'manent'
    v_cop -> 'est'
    v_inf -> 'errare'
    conj -> 'et' | 'ergo'
    adv -> 'lente'
""")

# 2. Creamos el Parser
parser = nltk.ChartParser(grammar)

# 3. Lista de oraciones "Modo Difícil"
frases_de_prueba = [
    "Age quod agis",
    "Festina lente",
    "Divide et impera",
    "In vino veritas",
    "Ex nihilo nihil",
    "Ab urbe condita",
    "Amor vincit omnia",
    "Errare humanum est",
    "Verba volant, scripta manent",
    "Per aspera ad astra",
    "Carpe diem",
    "Memento mori"
]

print("--- INICIANDO PRUEBA DE ESTRÉS LL(1) ---\n")

# 4. Motor de análisis
for frase in frases_de_prueba:
    print(f"Analizando: '{frase.upper()}'")
    
    # Limpiamos signos de puntuación antes de tokenizar
    frase_limpia = frase.replace(',', '').lower()
    tokens = frase_limpia.split()
    
    arboles_generados = list(parser.parse(tokens))
    
    if len(arboles_generados) == 0:
         print("-> [RECHAZADO] Error sintáctico: La frase excede la gramática actual.\n")
    else:
        for tree in arboles_generados:
            tree.pretty_print()
            # tree.draw() # <--- Descomenta para ver la interfaz gráfica
        print("-" * 40)