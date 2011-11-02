# Set line styles
set style line 1 lt 1 pt 7 lw 1 lc rgb "red"
set style line 2 lt 1 pt 7 lw 1 lc rgb "blue"
set style line 3 lt 1 lw 2 lc rgb "green"
set style line 4 lt 2 lw 1 lc rgb "orange"

# Set the parameters for x
set log y
set log x
set xrange [1:2000]
# set xtics (1,2,5,10,25,50,100,250,500,1000,2500,10000,25000,50000)
set xlabel "Number of entries in the data store"

set pointsize 0.5

########################################################################
# Read and write times
########################################################################
set ylabel 'Operation time in seconds'
#set yrange [-0.2:0.2]
set key left
set terminal postscript enhanced color lw 1 "Times-Roman" 8
set size 0.45,0.35
set output 'time.eps'
plot\
	'averages.dat' using 1:4 title 'Write' w p ls 1,\
	'averages.dat' using 1:3 title 'Read' w p ls 2
set terminal png nocrop enhanced size 600,350
set output 'time.png'
set size 1,1
plot\
	'averages.dat' using 1:4 title 'Write' w p ls 1,\
	'averages.dat' using 1:3 title 'Read' w p ls 2


########################################################################
# Space used
########################################################################
set ylabel 'Space used in MB'
#set yrange [0:50]
unset key
set terminal postscript enhanced color lw 1 "Times-Roman" 8
set size 0.45,0.35
set output 'space.eps'
plot\
	'averages.dat' u 1:($2/1024) w p ls 1
set terminal png nocrop enhanced size 600,350
set output 'space.png'
set size 1,1
plot\
	'averages.dat' u 1:($2/1024) w p ls 1
