# INICIO Código para rescatar los parámetros del script 
# librería necesaria para rescatar los parámetros formateados
# y generar la opción --help
library(optparse)

option1 <- make_option(
  c("--temp"),
  type = "numeric",
  default = 200,
  help = "Temperatura inicial"
)

option2 <- make_option(
  c("--max_iter_global"),
  type = "numeric",
  default = 1000,
  help = "Número máximo de iteraciones a nivel global"
)

option3 <- make_option(
  c("--max_iter_temp"),
  type = "numeric",
  default = 20,
  help = "Número máximo de iteraciones por temperatura"
)

option4 <- make_option(
  c("--alpha"),
  type = "numeric",
  default = 0.8,
  help = "Parámetro alfa del esquema de enfriamiento geométrico"
)

option5 <- make_option(
  c("--delta"),
  type = "numeric",
  default = 5,
  help = "Parámetro delta del esquema de enfriamiento lineal"
)

option6 <- make_option(
  c("--temp_func"),
  type = "numeric",
  default = 0,
  help = "Esquema de enfriamiento"
)

option7 <- make_option(
  c("--neighbour_func"),
  type = "numeric",
  default = 4,
  help = "Función de vecindario"
)

option8 <- make_option(
  c("--instance"),
  type = "character",
  default = "/Instances/bur26a.dat",
  help = "Ruta de la instancia del problema QAP"
)

opts <- list(option1, option2, option3, option4, option5, option6, option7, option8)

parser <- OptionParser(
  usage = "Uso: Rscript Lab3-irace.R --temp VALOR_INT --max_iter_global VALOR_INT --max_iter_temp VALOR_INT --alpha VALOR_DOUBLE --delta VALOR_DOUBLE --temp_func VALOR_INT --neighbour_func VALOR_INT --instance VALOR_STRING", 
  option_list = opts
)

arguments <- parse_args(parser)
# FIN Código para rescatar los parámetros del script 

# Lectura de dataset
readQAP<-function(name){ 
  a <- read.delim(name,header=FALSE, sep ="")
  n<-as.integer(a[1,1])
  fl<-a[2:(n+1),1:n]
  dis<-a[(n+2):(n+n+1),1:n]
  d <- list(n=n, f= fl, d = dis)
  return(d)
}

# Función objetivo
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

# operadores de vecindario
swap<-function(sol,i,j){
  piv<-sol[i]
  sol[i]<-sol[j]
  sol[j]<-piv
  return(sol)
}

insert<-function(sol,i,j){
  ele<-sol[i]
  a<-sol[-i]
  sol<-append(a,ele,after=j)
  return(sol)
}

reverse<-function(sol,i,j){
  a<-sol[i:j]
  a<-rev(a)
  b<-sol[-(i:j)]
  sol<-append(b,a,after=i)
  return(sol)
}

permute<-function(sol){
  sol<-swap(sol,sample(1:length(sol),1),sample(1:length(sol),1))
  sol<-insert(sol,sample(1:length(sol),1),sample(1:length(sol),1))
  sol<-reverse(sol,1,length(sol)-1)
  return(sol)
}

#leer instancia, crear y evaluar una solucion inicial
instancia<-readQAP(arguments$instance)

# INICIO Simulated Annealing (Laboratorio 2 - Metaheurísticas - 21-09-2023)
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
        new_sol<-insert(sol,sample(1:length(sol),1),sample(1:length(sol),1))
      }else if(neighbour_func==1){
        new_sol<-reverse(sol,sample(1:length(sol),1),sample(1:length(sol),1))
      }else if(neighbour_func==2){
        new_sol<-permute(sol)
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
      temp<-temp-delta
    }else{
      temp<-temp/log(iters_global)
    }
  }
  #png(file="/home/seba/irace_example/tuning/Results/Simulated_Annealing.png",width=600, height=350)
  #plot(x,y, type="l", col="green", lwd=3, xlab="iteraciones", ylab="fitness", main="Simulated Annealing")
  #dev.off()
  output<-c(best_f, list(best_sol))
  return(output)
}
# FIN Simulated Annealing (Laboratorio 2 - Metaheurísticas - 21-09-2023)

# INICIO parámetros de Simulated Annealing
temp<-arguments$temp							#temperatura inicial
max_iter_global<-arguments$max_iter_global 		#máximo de iteraciones global
max_iter_temp<-arguments$max_iter_temp   	  	#máximo de iteraciones por temperatura
alpha<-arguments$alpha            				#alfa del esquema geométrico por defecto
delta<-arguments$delta              			#delta para otro esquema (por ejemplo lineal)
temp_func<-arguments$temp_func          		#esquema de enfriamiento
neighbour_func<-arguments$neighbour_func     	#operador de vecindad
# FIN parámetros de Simulated Annealing

best_f<-0
output<-simulated_annealing(temp,max_iter_global,max_iter_temp,alpha,delta,temp_func,neighbour_func)
best_f<-as.integer(output[1])

# Output del fitness para ser usado por Irace.
# Aquí debe ir concatenado el tiempo de ejecución además 
# en caso que se requiera añadir la restricción 
# de tiempo en Irace
cat(best_f, "\n")

