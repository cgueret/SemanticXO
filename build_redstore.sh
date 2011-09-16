#!/bin/bash

# Define the versions to compile
REDSTORE="redstore-git"
RAPTOR="raptor2-2.0.4"
RASQAL="rasqal-0.9.27"
REDLAND="redland-1.0.14"
BDB="5.2.28"

# Common stuff
GET="wget --quiet"
DIRECTORY=$(pwd)
WORKDIR="/tmp"
TARGET="${WORKDIR}/build"
mkdir -p ${TARGET}/lib/pkgconfig
export PKG_CONFIG_PATH="/usr/lib32/pkgconfig"
export CC="gcc  -m32"
export CXX="g++ -m32"
export CARCH="i686"
export CHOST="i686-unknown-linux-gnu"
export CFLAGS="-march=i686 -mtune=generic -O2 -pipe"
export CXXFLAGS="-march=i686 -mtune=generic -O2 -pipe"
export PKG_CONFIG_PATH="${TARGET}/lib/pkgconfig:$PKG_CONFIG_PATH"
LD_LIBRARY_PATH="/usr/lib32:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH

# Download and compile one of the dependencies
function compile_redland() {
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
	./configure --prefix=${TARGET} --disable-static $@ >/dev/null
	echo "Compile $item"
	make >/dev/null
	echo "Install $item"
	make install >/dev/null
	cd ${DIRECTORY}
}

# Compile BDB
cd ${WORKDIR}
if [ ! -f bdb.tgz ]; then
	echo "Download BDB"
	${GET} http://download.oracle.com/berkeley-db/db-${BDB}.tar.gz --output-document=bdb.tgz 
fi
tar xzf bdb.tgz
cd db-${BDB}/build_unix
../dist/configure --prefix=${TARGET} --enable-compat185 --enable-shared --disable-static --enable-cxx --enable-dbm
make LIBSO_LIBS=-lpthread >/dev/null
make install >/dev/null 
cd ${DIRECTORY}

# Compile all the redland dependencies
compile_redland ${RAPTOR} 
compile_redland ${RASQAL} 
compile_redland ${REDLAND} --disable-modular --with-postgresql=no --with-virtuoso=no --with-mysql=no --with-sqlite=no --with-bdb-lib=${TARGET}/lib

# Download and compile redstore
cd ${WORKDIR}
if [ ! -d ${REDSTORE} ]; then
	git clone git://github.com/njh/redstore.git ${REDSTORE}
fi
cd ${REDSTORE}
git pull origin
if [ ! -f configure ]; then
	./autogen.sh
fi
./configure --prefix=${TARGET} >/dev/null
make >/dev/null
make install >/dev/null
cd ${DIRECTORY}

# Copy all the needed pieces
pwd
cp ${TARGET}/bin/redstore ${DIRECTORY}/redstore
cp ${TARGET}/lib/libraptor2.so.0.0.0 ${DIRECTORY}/libraptor2.so.0
cp ${TARGET}/lib/librasqal.so.3.0.0 ${DIRECTORY}/librasqal.so.3
cp ${TARGET}/lib/librdf.so.0.0.0 ${DIRECTORY}/librdf.so.0
cp ${TARGET}/lib/libdb-5.2.so ${DIRECTORY}/libdb-5.2.so

