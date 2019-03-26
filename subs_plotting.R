library(dplyr)
library(ggalluvial)
library(googleVis)

setwd("C:/Users/adwar/Documents/vassar_soccer/")
subs = read.csv(file = "subs.csv", 
                stringsAsFactors = F
                )




dat <- subs %>% filter(trimws(Sub.In) == 'Kevin Baliat') %>% group_by(Sub.In, Sub.Out) %>% tally()
sk1 <- gvisSankey(dat, from="Sub.Out", to="Sub.In", weight="n")
plot(sk1)

subs_in <- function(player_in){
  
  dat <- subs %>% filter(Sub.In == player_in) %>% group_by(Sub.In, Sub.Out) %>% tally()
   p_in <- gvisSankey(dat, from="Sub.In", to="Sub.Out", weight="n")
   file_name = paste0('C:/Users/adwar/Documents/vassar_soccer/player_in_sankey/', player_in, '.html')
  return(print(p_in, file=file_name))
   
} 


for (i in unique(subs$Sub.In)) {
  subs_in(i)
}

subs_out <- function(player_in){
  
  dat <- subs %>% filter(Sub.Out == player_in) %>% group_by(Sub.In, Sub.Out) %>% tally()
  p_in <- gvisSankey(dat, from="Sub.Out", to="Sub.In", weight="n")
  file_name = paste0('C:/Users/adwar/Documents/vassar_soccer/player_out_sankey/', player_in, '.html')
  return(print(p_in, file=file_name))
  
}

for (i in unique(subs$Sub.Out)) {
  subs_out(i)
}
