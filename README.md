# Generación y Limpieza de Gramática Libre de Contexto en Latín

**Carlos Delgado Contreras — A01712819**  
Implementación de Métodos Computacionales

> ⚠️ **Este archivo es un resumen del proyecto.**  
> La argumentación completa, el proceso de limpieza paso a paso y las evidencias visuales se encuentran en el documento: `Evidencia_Generación_y_Limpieza_de_Gramática.pdf`

---

## Descripción

Este proyecto diseña y valida una Gramática Libre de Contexto (CFG) para un subconjunto del **latín clásico**, específicamente aforismos y frases célebres. Se parte de una gramática intencionalmenete ambigua y con recursión izquierda (`Codex_Inpurus`) y se la transforma en una gramática limpia compatible con un parser **LL(1)** (`Puritas_Grammaticae`).

El latín fue elegido por su riqueza gramatical y su orden de palabras libre, lo que lo convierte en un escenario ideal para demostrar los problemas de ambigüedad y las técnicas de limpieza formal.

---

## Estructura del Lenguaje

El latín clásico presenta tres características que hacen complejo su modelado como CFG:

- **Sustantivación:** Los verbos en infinitivo y frases enteras pueden actuar como sujetos.
- **Elipsis del verbo *sum*:** El verbo copulativo suele omitirse, requiriendo el uso de la cadena vacía (ε).
- **Morfología sobre sintaxis:** La función gramatical la determina la terminación de la palabra, no su posición.

El proyecto delimita su alcance a tres estructuras fundamentales: **Sintagmas Imperativos**, **Cadenas Preposicionales** y **Oraciones Completas**.

---

## Módulos de la Gramática

La gramática se organiza en 4 módulos:

| Módulo | Descripción | Ejemplo |
|---|---|---|
| 1 - Frases Imperativas | Verbos en imperativo con objetos o adverbios | *Divide et impera* |
| 2 - Cadenas Preposicionales | Preposición + sustantivo, extensibles recursivamente | *Per aspera ad astra* |
| 3 - Oraciones Completas | Sujeto + Predicado (transitivo, copulativo, intransitivo) | *Amor vincit omnia* |
| 4 - Definiciones de Función | Roles abstractos: Sujeto, Objeto, Atributo | *Errare humanum est* |

---

## Los dos scripts: Codex vs Puritas

### `Codex_Inpurus.py` — La gramática con pecados capitales (18 reglas)

La gramática original. Contiene intencionalmente:

- **Recursión izquierda directa** en 5 de sus 18 reglas (genera bucles infinitos en un parser LL).
- **Alta ambigüedad** por prefijos idénticos en múltiples producciones.
- Usa un `ChartParser` que puede encontrar **todas** las interpretaciones posibles de una cadena, demostrando el caos generado por la gramática sucia.

### `Puritas_Grammaticae.py` — La gramática limpia LL(1) (15 reglas)

La gramática resultante tras aplicar tres técnicas de limpieza:

1. **Estratificación Jerárquica** — Se definen niveles estrictos: terminales atómicos → bloques funcionales → raíz global. Elimina los ciclos de definición mutua.
2. **Eliminación de Recursión Izquierda** — Usando la identidad algebraica `A → Aα | β` → `A → βA'`, `A' → αA' | ε`.
3. **Factorización por Prefijo** — Se extrae el prefijo común a un nuevo no-terminal para garantizar una sola ruta de derivación por token.

El resultado es una gramática determinista que procesa cada frase en **tiempo lineal**.

---

## Frases de Prueba

Ambos scripts corren exactamente el mismo conjunto de 12 frases con el mismo diccionario unificado:

```
Age quod agis        Festina lente         Divide et impera
In vino veritas      Ex nihilo nihil       Ab urbe condita
Amor vincit omnia    Errare humanum est    Verba volant, scripta manent
Per aspera ad astra  Carpe diem            Memento mori
```

---

## Resultados Notables

- **`Age quod agis`** es **rechazada** por ambas gramáticas. La razón: *quod agis* es una oración subordinada de relativo, una estructura que requeriría un módulo adicional que ninguna gramática incluye actualmente.
- **`Per aspera ad astra`** produce **1 árbol en Codex** pero **2 en Puritas**. Paradójicamente, la gramática limpia es más ambigua aquí: sus dos caminos a la cadena vacía (ε) generan un remanente de ambigüedad en `SP_Cadena`. La gramática sucia, por su rigidez de recursión izquierda, fuerza una única ruta de procesamiento.
- **`Divide et impera`** produce **2 árboles en Codex** y **1 en Puritas**, demostrando el éxito de la factorización.

---

## Jerarquía de Chomsky

Ambas gramáticas son **Gramáticas Libres de Contexto (Tipo 2)**. Lo que las diferencia es la eficiencia algorítmica:

- **Codex Inpurus** requiere backtracking exhaustivo por su ambigüedad.
- **Puritas Grammaticae** es un subconjunto **LL(1)**: procesamiento determinista en tiempo lineal con un autómata de pila.

El latín requiere necesariamente ser Tipo 2 (y no Tipo 3 / Regular) porque la sustantivación implica anidamiento recursivo, lo que exige memoria en forma de stack.

---

## Cómo Ejecutar

### Requisitos

```bash
pip install nltk
```

### Ejecutar la gramática sucia (Codex)

```bash
python Codex_Inpurus.py
```

Muestra para cada frase cuántos árboles de derivación se generan y los primeros 2. Un número mayor a 1 evidencia **ambigüedad**.

### Ejecutar la gramática limpia (Puritas)

```bash
python Puritas_Grammaticae.py
```

Muestra un único árbol de derivación por frase aceptada, o un mensaje de **rechazo** si la frase excede la gramática. Si deseas visualizar el árbol gráficamente, descomenta la línea `# tree.draw()` en el script.

---

## Diccionario Unificado

Ambos scripts comparten el mismo léxico:

| Categoría | Palabras |
|---|---|
| `v_imp` | veni, vince, memento, carpe, divide, festina, age, impera |
| `sust` | diem, vino, veritas, nihilo, astra, amor, omnia, verba, nihil, urbe, condita, humanum, scripta, aspera, mori, quod, agis |
| `prep` | in, ex, per, ad, ab |
| `v_trans` | vincit, tenet |
| `v_int` | volant, manent |
| `v_cop` | est |
| `v_inf` | errare, mori |
| `conj` | et, ergo |
| `adv` | lente |

---

## Referencia

Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.). Pearson Education.
