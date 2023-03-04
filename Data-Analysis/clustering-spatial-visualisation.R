library('tidyverse')
library('sf')
library('units')
library('tmap')
library('Matrix')
tmap_mode("view")


##### Data Analysis

## read raw winter wheat data
data_2021 <- st_read("raw-data/lccm-2021_4836013/lccm-2021_4836013.gdb/")

## read raw county boundaries data
Counties <- st_read('raw-data/Counties_and_Unitary_Authorities_(December_2022)_UK_BFC.shp')

## extract 10km2 area near Cambridgeshire
ww_2021_aoi <- st_crop(data_2021,xmin=505000,xmax=515000,ymin=260000,ymax=270000)

## larger area
#ww_2021_aoi <- st_crop(data_2021,xmin=485000,xmax=535000,ymin=240000,ymax=290000)

ww_2021_aoi <- filter(data_2021,is.element(gid,as.list(ww_2021_aoi$gid)))

## Network Analysis

## find centroid of each field
centroids <- st_centroid(ww_2021_aoi$SHAPE) 

## compute distance matrix 
distance_matrix <- st_distance(centroids)
distance_matrix <- drop_units(distance_matrix)

## convert to weighted adjacency matrix J
J <- (1/(1+distance_matrix^3))^(1/3)
diag(J) <- 0
tol <- 0.03  #tolerance for sparse matrix
J[J<max(J)*tol] <- 0
J<- Matrix(J,sparse=TRUE)

## compute clustering coefficient - this becomes the colour of fields.
J3 <- J %*% J %*% J
k <- 2*rowSums(J)/3+sum(J)/3
clustering_coef <- diag(J3)/k
ww_2021_aoi$clustering_coef <- clustering_coef/max(clustering_coef)

## plot using tmap
tm_shape(ww_2021_aoi)+
  tm_polygons(col='clustering_coef',style='cont')+
  tm_borders(col='black')

  tm_shape(County_levels)+
  tm_fill(col='name',alpha=0.2)+
  tm_scale_bar()





## get list of satellite image names and combine to one virtual raster
image_dir <- 'raw-data/satellite-imagery/Cambridgeshire10km2/'
image_names <- list.files('raw-data/satellite-imagery/Cambridgeshire10km2/',pattern='*.jpg',full.names = TRUE)
r <- vrt(image_names,overwrite=TRUE)

plotRGB(r)
