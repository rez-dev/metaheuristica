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
instancia<-readQAP("bur26a.dat")
sol<-c(1:instancia$n)
print(sol)
fitness<-evaluarQAP(sol,instancia$f,instancia$d)
fitness

#generar solución aleatoria y evaluar
sol <- sample(1:instancia$n,instancia$n,replace=F)
print(sol)
fitness<-evaluarQAP(sol,instancia$f,instancia$d)
fitness

#generar 100 soluciones aleatorias y graficar
rm(fitness)
sol <- sample(1:instancia$n,instancia$n,replace=F)
fitness<-evaluarQAP(sol,instancia$f,instancia$d)
best_f<-fitness
for(i in 1:99){
  sol <- sample(1:instancia$n,instancia$n,replace=F)
  current_f<-evaluarQAP(sol,instancia$f,instancia$d)
  fitness<-c(fitness,current_f)
  if(best_f>current_f){
    best_f<-current_f
  }
}
print(best_f)
plot(fitness,main="100 soluciones aleatorias", xlab = "Solutions")

#si ordenamos estas soluciones aleatorias...

plot(sort(fitness, decreasing=TRUE),main="100 soluciones aleatorias", xlab = "Solutions", ylab = "Fitness")

#generar 100 soluciones aleatorias y graficar (SWAP)
rm(fitness)
sol <- sample(1:instancia$n,instancia$n,replace=F)
#print(sol)
fitness<-evaluarQAP(sol,instancia$f,instancia$d)
best_f<-fitness
best_sol<-sol
for(i in 1:99){
  sol <- swap(sol,sample(1:length(sol),1),sample(1:length(sol),1))
  current_f<-evaluarQAP(sol,instancia$f,instancia$d)
  fitness<-c(fitness,current_f)
  if(best_f>current_f){
    best_f<-current_f
    best_sol<-sol
  }
}
print(best_f)
print(best_sol)
plot(fitness,main="100 soluciones SWAP", xlab = "Solutions")
