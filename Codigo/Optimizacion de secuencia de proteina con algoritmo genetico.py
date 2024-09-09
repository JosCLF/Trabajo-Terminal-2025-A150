import random

# ============================================================================= PARAMETROS =================================================================
N_generaciones = 200
N_individuos = 100
longitud_de_la_secuencia = 50
letras_aminoacidos = 'ACDEFGHIKLMNPQRSTVWY'

# ============================================================================= GENERACION DE PROTEINA =================================================================
def generar_proteina(longitud):
    return ''.join(random.choices(letras_aminoacidos, k=longitud))

# ============================================================================= INICIALIZAR LA POBLACION =================================================================
def inicializar_poblacion(n_poblacion, longitud_de_la_cadena_proteina):
    return [generar_proteina(longitud_de_la_cadena_proteina) for _ in range(n_poblacion)]

# ============================================================================= EVALUACIONES =================================================================
def evaluar_interaccion_con_plantas(individuo):
    aminoacidos_interactivos = 'KRH'
    interaccion = sum(1 for aa in individuo if aa in aminoacidos_interactivos)
    return interaccion

def evaluar_estabilidad_en_suelo(individuo):
    aminoacidos_estables = 'ACFGILVWY'
    estabilidad = sum(1 for aa in individuo if aa in aminoacidos_estables)
    return estabilidad

def evaluar_estabilidad_y_hidrofobicidad(individuo):
    estabilidad = sum(1 for aa in individuo if aa in 'CSTPAG')
    hidrofobicidad = sum(1 for aa in individuo if aa in 'AILMFWV')
    evaluacion = 0.5 * estabilidad + 0.5 * hidrofobicidad
    return evaluacion

def evaluar_solubilidad(individuo):
    solubilidad = sum(1 for aa in individuo if aa in 'DEKR')
    return solubilidad

def evaluar_estabilidad_termica(individuo):
    estabilidad_termica = sum(1 for aa in individuo if aa in 'ACFGILVWY')
    return estabilidad_termica

def evaluar_propiedad_antifungica(individuo):
    antifungica = sum(1 for aa in individuo if aa in 'KR')
    return antifungica
# ============================================================================= RESTRICCIONES =================================================================

def evaluar_repetitividad(individuo):
    frecuencias = {aa: individuo.count(aa) for aa in letras_aminoacidos}
    
    longitud_secuencia = len(individuo)
    porcentaje_repetido = max(frecuencias.values()) / longitud_secuencia
    
    umbral_repeticion = 0.30
    if porcentaje_repetido > umbral_repeticion:
        penalizacion = (porcentaje_repetido - umbral_repeticion) * 1000 
        return -penalizacion  
    else:
        return 0  
# ============================================================================= FUNCION OBJETIVO FINAL =================================================================
def FO_completa(individuo):
    estabilidad_hidrofobicidad = evaluar_estabilidad_y_hidrofobicidad(individuo)
    solubilidad = evaluar_solubilidad(individuo)
    estabilidad_termica = evaluar_estabilidad_termica(individuo)
    antifungica = evaluar_propiedad_antifungica(individuo)
    interaccion_con_plantas = evaluar_interaccion_con_plantas(individuo)
    estabilidad_en_suelo = evaluar_estabilidad_en_suelo(individuo)

    penalizacion_repetitividad = evaluar_repetitividad(individuo)
    
    evaluacion_total = (0.2 * estabilidad_hidrofobicidad + 0.2 * solubilidad + 0.1 * estabilidad_termica + 0.1 * antifungica + 0.2
                         * interaccion_con_plantas + 0.2 * estabilidad_en_suelo + penalizacion_repetitividad)
    return evaluacion_total

# ============================================================================= EVALUAR LA POBLACION =================================================================
def evaluar_poblacion(poblacion):
    return [FO_completa(individuo) for individuo in poblacion]

# ============================================================================= SELECCION DE PADRES Y CRUCE =================================================================
def elegir_padres(poblacion, valor_FO):
    padres = random.choices(poblacion, weights=valor_FO, k=len(poblacion))
    return padres

def cruzamiento(padre1, padre2):
    punto_corte = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
    hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
    return hijo1, hijo2

def descendencia(padres):
    nueva_gen = []
    for i in range(0, len(padres), 2):
        hijo1, hijo2 = cruzamiento(padres[i], padres[i + 1])
        nueva_gen.extend([hijo1, hijo2])
    return nueva_gen

# ============================================================================= MUTACION =================================================================
def mutacion(proteina, probabilidad_mutacion=0.01):
    lista_proteinas = list(proteina)
    for i in range(len(lista_proteinas)):
        if random.random() < probabilidad_mutacion:
            lista_proteinas[i] = random.choice(letras_aminoacidos)
    return ''.join(lista_proteinas)


def mutar_poblacion(poblacion, probabilidad_mutacion=0.01):
    return [mutacion(individuo, probabilidad_mutacion) for individuo in poblacion]

# ============================================================================= NUEVA GEN ELITISMO =================================================================
def nueva_gen_elitismo(poblacion_antigua, poblacion_nueva, valores_FO):
    num_elite = int(0.1 * len(poblacion_antigua))
    elite_indices = sorted(range(len(valores_FO)), key=lambda i: valores_FO[i], reverse=True)[:num_elite]
    elite_individuals = [poblacion_antigua[i] for i in elite_indices]
    poblacion_nueva[-num_elite:] = elite_individuals
    return poblacion_nueva

# ============================================================================= ALGORITMO GENETICO =================================================================
def algortimo_genetico(num_poblacion, longitud_proteina, num_generaciones):
    poblacion = inicializar_poblacion(num_poblacion, longitud_proteina)
    
    mejor_valor_FO = float('-inf')
    mejor_individuo = None

    for generacion in range(num_generaciones):
        poblacion_evaluada = evaluar_poblacion(poblacion)
        
        mejor_valor_FO_actual = max(poblacion_evaluada)
        if mejor_valor_FO_actual > mejor_valor_FO:
            mejor_valor_FO = mejor_valor_FO_actual
            mejor_individuo = poblacion[poblacion_evaluada.index(mejor_valor_FO_actual)]
        
        padres_seleccionados = elegir_padres(poblacion, poblacion_evaluada)
        nueva_generacion = descendencia(padres_seleccionados)
        nueva_gen_mutada = mutar_poblacion(nueva_generacion)
        
        poblacion = nueva_gen_elitismo(poblacion, nueva_gen_mutada, poblacion_evaluada)

        print('generacion ', generacion,'mejor valor FO actual ', mejor_valor_FO_actual)
        
    return mejor_individuo

# ============================================================================= EJECUCION DEL ALGORITMO =================================================================
mejor_solucion = algortimo_genetico(N_individuos, longitud_de_la_secuencia, N_generaciones)
print('Mejor solucion: ', mejor_solucion)
