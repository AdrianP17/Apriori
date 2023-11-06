def main():
  ID = []
  Producto = []
  Datos = []
  n = int(input("Ingrese el numero de datos a analizar: "))
  min_soporte = float(input("Ingrese el soporte minimo: "))
  min_confianza = float(input("Ingrese la confianza minima: "))
  #Almacenamiento de datos en los arreglos
  for i in range(0,n):
    id = int(input(f"{i+1}) Ingrese el ID del producto: "))
    nombre = str(input(f"Ingrese el nombre del producto: "))
    ID.append(id)
    Producto.append(nombre)
  ID_unicos = extraerID(ID)
  Producto_unicos = extraerProducto(Producto)
  ordenarDatos(n,Datos,ID,Producto)
  transacciones = filtrar_productos(ID,Producto,ID_unicos)
  itemset_2 = conjuntos_2en2(Producto_unicos) 
  itemset_3 = conjuntos_3en3(Producto_unicos)
  candidates2 = candidates_set(transacciones, itemset_2,min_soporte)
  candidates1 = candidates_item(transacciones, Producto_unicos,min_soporte)
  reglas1 = reglas(transacciones,candidates1,candidates2,min_soporte,min_confianza)
  if(reglas1 == []):
    print("No se ha encontrado ninguna regla con el soporte y confianza mínima, intente bajar ambos parámetros")
  else:
    print(reglas1)

def extraerID(ID):
  ID_unicos = []
  for k in ID:
    if (k not in ID_unicos):
      ID_unicos.append(k)
  return ID_unicos

def extraerProducto(Producto):
  Producto_unicos = []
  for k in Producto:
    if (k not in Producto_unicos):
      Producto_unicos.append(k)
  return (Producto_unicos)

def ordenarDatos(n,Datos,ID,Producto):
  for x in range(0,n):
    Datos.append([ID[x],Producto[x]])
  print(Datos)

def filtrar_productos(id, product, id_unicos):
  results = [[] for _ in range(len(id_unicos))]
  for i in range(len(id)):
    for j in range(len(id_unicos)):
      if id[i] == id_unicos[j]:
        results[j].append(product[i])
  return results

def conjuntos_2en2(A):
  subconjuntos_2 = []
  for i in A:
      for j in A:
          if i < j:
              subconjuntos_2.append({i, j})
  return subconjuntos_2
def conjuntos_3en3(A):
  subconjuntos_3 = []
  for i in A:
      for j in A:
          for k in A:
              if i < j < k:
                  subconjuntos_3.append({i, j, k})
  return subconjuntos_3

def candidates_set(transacciones, itemset, min_soporte):
    candidatos = []
    for x in itemset:
        count = 0
        for y in transacciones:
            if x.issubset(y):
                count += 1
        soporte = count / len(transacciones)
        if soporte >= min_soporte:
            candidatos.append((x))
    return candidatos
def candidates_item(transacciones, itemset, min_soporte):
    candidatos = []
    for x in itemset:
        count = 0
        for y in transacciones:
            if x in y:
                count += 1
        soporte = count / len(transacciones)
        if soporte >= min_soporte:
            candidatos.append({x})
    return candidatos
def soporte(transacciones, itemset):
    count = 0
    for t in transacciones:
        if set(itemset).issubset(t):
            count += 1
    return count / len(transacciones)
def confianza(transacciones, antecedente, consecuente):
  soporte_antecedente = soporte(transacciones, tuple(antecedente))
  soporte_consecuente = soporte(transacciones, tuple(consecuente))
  soporte_union = soporte(transacciones, tuple(antecedente.union(consecuente)))
  if soporte_antecedente == 0:
      return 0
  else:
      soporte_union = soporte(transacciones, antecedente.union(consecuente))
      return soporte_union / soporte_antecedente

def reglas(transacciones,candidates1,candidates2,min_soporte,min_confianza):
  reglas = []
  contador=0
  for x in candidates1:
    for y in candidates2:
      if(confianza(transacciones,x,y)>=min_confianza and soporte(transacciones,x.union(y))>=min_soporte and (not x.issubset(y))):
        contador+=1
        reglas.append(f"Regla {contador}: {x}>{y} Soporte: {soporte(transacciones,x.union(y))} Confianza: {confianza(transacciones,x,y)} Valido")
  for x in candidates2:
    for y in candidates1:
      if(confianza(transacciones,x,y)>=min_confianza and soporte(transacciones,x.union(y))>=min_soporte and (not y.issubset(x))):
        contador+=1
        reglas.append(f"Regla {contador}: {x}>{y} Soporte: {soporte(transacciones,x.union(y))} Confianza: {confianza(transacciones,x,y)} Valido")
  return reglas

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print ('Interrupted')
