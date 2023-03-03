library('tidyverse')
library('sf')
library('terra')

## read raw data
data_2021 <- st_read("raw-data/lccm-2021_4836013/lccm-2021_4836013.gdb/")
data_2020 <- st_read("raw-data/lccm-2020_4836012/lccm-2020_4836012.gdb/")
data_2019<- st_read("raw-data/lccm-2019_4836011/lccm-2019_4836011.gdb/")


## extract and plot 10km2 area in Cambridgeshire
ww_2021_cam <- st_crop(data_2021,xmin=505000,xmax=515000,ymin=260000,ymax=270000)
ww_2020_cam <- st_crop(data_2020,xmin=505000,xmax=515000,ymin=260000,ymax=270000)
ww_2019_cam<- st_crop(data_2019,xmin=505000,xmax=515000,ymin=260000,ymax=270000)



## get list of satellite image names and combine to one raster
image_dir <- 'raw-data/satellite-imagery/Cambridgeshire10km2/'
image_names <- list.files('raw-data/satellite-imagery/Cambridgeshire10km2/',pattern='*.jpg',full.names = TRUE)
r <- vrt(image_names,overwrite=TRUE)

## plotting
par(mfrow=c(1,3))
plotRGB(r)
plot(ww_2020_cam,add=TRUE,col='lightblue')
plotRGB(r)
plot(ww_2021_cam,add=TRUE,col='lightyellow')
plotRGB(r)
plot(ww_2019_cam,add=TRUE,col='lightgreen')




