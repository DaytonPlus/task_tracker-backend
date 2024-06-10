public int cuantasAltamenteVulnerable(Lista<Computadora> lista) {
	int cant = 0;
	int maxConexiones;
	
	for(Computadora c : lista) {
	  maxConexiones = 4;
	  int pos = computadoras.indexOf(c);
	  for(int i=0;i<conexiones[pos].size() && maxConexiones > 0;i++) {
	    if(conexiones[pos][i]) maxConexiones--;
	  }
	  if(!maxConexiones) cant++;
	}
	
	return cant;
}

public List<Computadora> adyacentesA(Computadora c) {
  List<Computadora> lista = new LinkedList<>();
  int pos = computadoras.indexOf(c);
  if(pos==-1) return null;
  
  for(int i=0;i<conexiones[pos].size();i++) {
    if(conexiones[pos][i]) lista.add(computadoras[i]);
  }
  return lista;
}