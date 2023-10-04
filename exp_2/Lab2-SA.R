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

invertir_elementos <- function(vector, i) {
  if (i >= 1 && i <= length(vector)) {
    vector[1:i] <- rev(vector[1:i])
    return(vector)
  } else {
    cat("La posición i está fuera del rango del vector.\n")
    return(NULL)
  }
}




#leer instancia, crear y evaluar una solucion inicial
instancia<-readQAP("bur26a.dat")
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
        # new_sol<-swap(sol,sample(1:length(sol),1),sample(1:length(sol),1))
        new_sol<-invertir_elementos(sol,sample(1:length(sol),1))
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

