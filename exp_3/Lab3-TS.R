readQAP<-function(name){ 
  a <- read.delim(name,header=FALSE, sep ="")
  n<-as.integer(a[1,1])
  fl<-a[2:(n+1),1:n]
  dis<-a[(n+2):(n+n+1),1:n]
  d <- list(n=n, f= fl, d = dis)
  return(d)
}

evaluarQAP<-function(sol, f, d){
  
  acum<-0
  n<-length(sol)
  for(i in 1:n){
    for(j in 1:n){
      acum = acum + f[i,j]*d[sol[i],sol[j]]   
    }
  }
  return(acum)
}

swap<-function(sol,i,j){
  piv<-sol[i]
  sol[i]<-sol[j]
  sol[j]<-piv
  return(sol)
}

#leer instancia, crear y evaluar una solucion inicial
instancia<-readQAP("instancia.dat")
sol<-c(1:instancia$n)
print(sol)
fitness<-evaluarQAP(sol,instancia$f,instancia$d)
fitness

### Simulated Annealing (Laboratorio 2 - Metaheurísticas - 21-09-2023)
simulated_annealing<-function(temp,max_iter_global,max_iter_temp,alpha,delta,temp_func,neighbour_func){
  x<-list()
  y<-list()
  fitness=100000000000
  sol <- sample(1:instancia$n,instancia$n,replace=F)
  fitness<-evaluarQAP(sol,instancia$f,instancia$d)
  best_f<-fitness
  best_sol<-sol
  iters_global<-0
  x<-append(x,iters_global)
  y<-append(y,fitness)
  while(max_iter_global>iters_global){
    iters_temp<-0
    while(max_iter_temp>iters_temp){
      new_sol<-NULL
      if(neighbour_func==0){
        # Aquí va el 1er operador de vecindad
      }else if(neighbour_func==1){
        # Aquí va el 2do operador de vecindad
      }else if(neighbour_func==2){
        # Aquí va el 3er operador de vecindad
      }else{
        new_sol<-swap(sol,sample(1:length(sol),1),sample(1:length(sol),1))
      }
      new_fitness<-evaluarQAP(new_sol,instancia$f,instancia$d)
      dif<-new_fitness-fitness
      if(dif<=0){
        sol<-new_sol
        fitness<-new_fitness
        if(best_f>new_fitness){
          best_sol<-new_sol
          best_f<-new_fitness
        }
      }else{
        prob=exp(-dif/temp)
        if(sample(0:1,1)<prob){
          sol<-new_sol
          fitness<-new_fitness
        }
      }
      iters_temp<-iters_temp+1
      iters_global<-iters_global+1
      x<-append(x,iters_global)
      y<-append(y,fitness)
    }
    if(temp_func==0){
      temp<-temp*alpha
    }else if(temp_func==1){
      # Aquí va el 1er esquema de enfriamiento
    }else{
      # Aquí va el 2do esquema de enfriamiento
    }
  }
  png(file="Simulated_Annealing.png",width=600, height=350)
  plot(x,y, type="l", col="green", lwd=3, xlab="iteraciones", ylab="fitness", main="Simulated Annealing")
  dev.off()
  output<-c(best_f, list(best_sol))
  return(output)
}

library(tictoc)

# INICIO parámetros a modificar de SA
temp<-200             #temperatura inicial
max_iter_global<-1000 #máximo de iteraciones global
max_iter_temp<-20     #máximo de iteraciones por temperatura
alpha<-0.8            #alfa del esquema geométrico por defecto
delta<-5              #delta para otro esquema (por ejemplo lineal)
temp_func<-0          #esquema de enfriamiento
neighbour_func<-4     #operador de vecindad
# FIN parámetros a modificar de SA

tic("Simulated Annealing")
num_runs<-5
best_f<-0
best_sol<-list()
output<-simulated_annealing(temp,max_iter_global,max_iter_temp,alpha,delta,temp_func,neighbour_func)
sum_bf=as.integer(output[1])
best_f<-as.integer(output[1])
best_sol<-output[2]
sols<-list(output[2])
for(i in 1:(num_runs-1)){
  output=simulated_annealing(temp,max_iter_global,max_iter_temp,alpha,delta,temp_func,neighbour_func)
  sum_bf=sum_bf+as.integer(output[1])
  sols<-append(sols, list(output[2]))
  if(as.integer(output[1])<best_f){
    best_f<-as.integer(output[1])
    best_sol<-output[2]
  }
}
toc()

mean=sum_bf/num_runs
print(mean)
print(best_f)
print(best_sol)

###############################################################################
###############################################################################
# AGREGAR A CONTINUACIÓN SU CÓDIGO TABU SEARCH
# REUSANDO EL CÓDIGO NECESARIO DE LA AYUDANTÍA ANTERIOR
###############################################################################
###############################################################################

readQAP<-function(name){ 
  a <- read.delim(name,header=FALSE, sep ="")
  n<-as.integer(a[1,1])
  fl<-a[2:(n+1),1:n]
  dis<-a[(n+2):(n+n+1),1:n]
  d <- list(n=n, f= fl, d = dis)
  return(d)
}

evaluarQAP<-function(sol, f, d){
  
  acum<-0
  n<-length(sol)
  for(i in 1:n){
    for(j in 1:n){
      acum = acum + f[i,j]*d[sol[i],sol[j]]   
    }
  }
  return(acum)
}

# Calcular costoo total de asignación
calcular_costoo <- function(solucion, matriz_flujo, matriz_distancia) {
  costoo_total <- sum(matriz_flujo * matriz_distancia[solucion, solucion])
  return(costoo_total)
}

# Explorar vecindario y encontrar el mejor movimiento
explorar_vecindario <- function(solucion, matriz_flujo, matriz_distancia) {
  n <- length(solucion)
  best_costoo <- Inf
  best_mov <- NULL
  
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      new_solucion <- solucion
      new_solucion[c(i, j)] <- new_solucion[c(j, i)]
      costo <- calcular_costoo(new_solucion, matriz_flujo, matriz_distancia)
      if (costo < best_costoo) {
        best_costoo <- costo
        best_mov <- list(from = i, to = j)
      }
    }
  }
  
  return(list(solucion = solucion, costo = best_costoo, mov = best_mov))
}

# Realizar la búsqueda tabú
tabu_search <- function(matriz_flujo, matriz_distancia, max_iteraciones, tabu_tenure) {
  n <- nrow(matriz_flujo)
  soluction_actual <- sample(1:n)
  best_solucion <- soluction_actual
  best_costoo <- calcular_costoo(soluction_actual, matriz_flujo, matriz_distancia)
  tabu_list <- list()
  
  for (iter in 1:max_iteraciones) {
    vecindario <- explorar_vecindario(soluction_actual, matriz_flujo, matriz_distancia)
    soluction_actual <- vecindario$solucion
    costo_actual <- vecindario$costo
    
    if (costo_actual < best_costoo) {
      best_solucion <- soluction_actual
      best_costoo <- costo_actual
    }
    
    # Agregar el movimiento actual a la lista tabú
    tabu_list <- c(tabu_list, vecindario$mov)
    
    # Eliminar movimientos antiguos de la lista tabú
    if (length(tabu_list) > tabu_tenure) {
      tabu_list <- tabu_list[-1]
    }
  }
  
  return(list(solucion = best_solucion, costo = best_costoo))
}

# Generar matrices de flujos y distancias aleatorias para el ejemplo
set.seed(123)
max_iteraciones <- 100  # Número máximo de iteraciones
tabu_tenure <- 15  # Tamaño de la lista tabú
instancia <- readQAP("instancia.dat")
matriz_flujo <- instancia$f
matriz_distancia <- instancia$d

tic("Tabu Search")
result <- tabu_search(matriz_flujo, matriz_distancia, max_iteraciones, tabu_tenure)
toc()
cat("Mejor solución encontrada:", result$solucion, "\n")
fitness<-evaluarQAP(result$solucion,instancia$f,instancia$d)
fitness



















