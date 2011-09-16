#!/bin/sh

# Name of archives
setup_bundle=semanticxo.tgz
remove_bundle=genuinexo.tgz

# Source function library
. /etc/rc.d/init.d/functions

# Install the triple store on the XO and replace the Journal data store
setup()
{
	if [ ! -f $setup_bundle ]; then
		echo $"Failed to locate setup bundle !"
		failure
		echo
	fi

	echo -n $"Create remove bundle"
	tar -pczf $remove_bundle /usr/lib/python2.7/site-packages/carquinyol > /dev/null 2>&1
	success
	echo

	echo -n $"Remove current journal implementation"
	rm -r /usr/lib/python2.7/site-packages/carquinyol
	success
	echo

	echo -n $"Unpack SemanticXO bundle"
	tar -xvzf $setup_bundle --no-same-owner -C / > /dev/null
	success
	echo

	echo -n $"Set autoboot triple store"
	ln -s /etc/init.d/redstoredaemon /etc/rc.d/rc5.d/S50redstore
	ln -s /etc/init.d/redstoredaemon /etc/rc.d/rc5.d/K50redstore
	chmod a+x /etc/init.d/redstoredaemon
	chmod a+x /opt/redstore/redstore
	chmod a+x /opt/redstore/wrapper.sh
	success
	echo
}

# Remove everything that was installed
remove()
{
	if [ ! -f $remove_bundle ]; then
		echo $"Failed to locate remove bundle !"
		failure
		echo
	fi

	echo -n $"Remove SemanticXO files"
	rm -r /opt/redstore
	rm -r /usr/lib/python2.7/site-packages/carquinyol
	rm -r /usr/lib/python2.7/site-packages/rdflib
	rm -r /usr/lib/python2.7/site-packages/semanticxo
	rm -r /var/lib/redstore
	rm /etc/rc.d/rc5.d/S50redstore
	rm /etc/rc.d/rc5.d/K50redstore
	rm /etc/init.d/redstoredaemon
	success
	echo

	echo -n $"Unpack remove bundle"
	tar -xvzf $remove_bundle --no-same-owner -C / > /dev/null
	success
	echo
}


# Handle command line parameter
case "$1" in
	setup)
		setup
		;;
	remove)
		remove
		;;
	*)
		echo $"Usage: $0 {setup|remove}"
		;;
esac
exit $RETVAL

