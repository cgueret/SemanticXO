#!/bin/bash

# Define the versions to compile
REDSTORE="redstore-0.5.2"
RAPTOR="raptor2-2.0.4"
RASQAL="rasqal-0.9.27"
REDLAND="redland-1.0.14"

# Common stuff
GET="wget --quiet"
DIRECTORY=$(cd `dirname $0` && pwd)
WORKDIR="/tmp"
TARGET="${WORKDIR}/build"
mkdir -p ${TARGET}/lib/pkgconfig
export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"
export CC="gcc -m32"
export CXX="g++ -m32"
export CARCH="i686"
export CHOST="i686-unknown-linux-gnu"
export CFLAGS="-march=i686 -mtune=generic -O2 -pipe"
export CXXFLAGS="-march=i686 -mtune=generic -O2 -pipe"
export PKG_CONFIG_PATH="${TARGET}/lib/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="/usr/lib32:$LD_LIBRARY_PATH"

# Download and compile one of the dependencies
function compile() {
	item=$1
	shift
	if [ ! -f ${WORKDIR}/$item.tgz ]; then
		echo "Download $item"
		${GET} http://download.librdf.org/source/$item.tar.gz --output-document=${WORKDIR}/$item.tgz 
	fi
	cd ${WORKDIR}
	tar xzf $item.tgz
	cd $item
	echo "Configure $item"
	./configure --prefix=${TARGET} $@ >/dev/null
	echo "Compile $item"
	make >/dev/null
	echo "Install $item"
	make install >/dev/null
	cd ${DIRECTORY}
}

# Compile all the dependencies
compile ${RAPTOR}
compile ${RASQAL}
compile ${REDLAND} --enable-storages=sqlite --disable-modular --with-postgresql=no --with-virtuoso=no --with-mysql=no

# Download and compile redstore
if [ ! -f redstore.tgz ]; then
	${GET} http://www.aelius.com/njh/redstore/${REDSTORE}.tar.gz --output-document=${WORKDIR}/redstore.tgz
fi
cd ${WORKDIR}
tar xzf redstore.tgz
cd ${REDSTORE}
./configure --prefix=${TARGET} >/dev/null
make >/dev/null
make install >/dev/null
cd ${DIRECTORY}

# Copy all the needed pieces
cp ${TARGET}/bin/redstore ${DIRECTORY}/redstored
cp ${TARGET}/lib/libraptor2.so.0.0.0 ${DIRECTORY}
cp ${TARGET}/lib/librasqal.so.3.0.0 ${DIRECTORY}
cp ${TARGET}/lib/librdf.so.0.0.0 ${DIRECTORY}

